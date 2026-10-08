#!/usr/bin/env node
// Rellena y envía formularios de contacto web para el agente de inversores.
//
// Uso (Playwright va instalado de forma global, de ahí NODE_PATH):
//   NODE_PATH=$(npm root -g) node formularios_web.js inspeccionar <url>
//   NODE_PATH=$(npm root -g) node formularios_web.js enviar <url> <mapa.json> <captura.png> [--prueba]
//
// inspeccionar: lista los formularios de la página con sus campos, los enlaces de contacto,
//   los emails publicados y si hay CAPTCHA. Salida en JSON.
// enviar: rellena los campos del mapa, pulsa enviar y dice si la web confirma el envío.
//   Con --prueba rellena y hace la captura, pero no envía.
//
// mapa.json:
//   {"formulario": 0,
//    "campos": [{"selector": "#nombre", "valor": "Pedro"},
//               {"selector": "select[name=motivo]", "opcion": "Otros"},
//               {"selector": "input[name=privacidad]", "marcar": true}],
//    "boton": "button[type=submit]"}            // opcional: si falta, el primer botón de envío del formulario

const { chromium } = require('playwright');
const fs = require('fs');

const OK = /gracias|enviad[oa]|recibid[oa]|hemos recibido|nos pondremos en contacto|en breve|thank|success|sent|mail_sent/i;
const MAL = /error|obligatori|required|inv[aá]lid|no se ha podido|failed|captcha|spam|mail_failed|validation_failed/i;

async function abrir(url) {
  const browser = await chromium.launch({
    headless: true,
    proxy: process.env.HTTPS_PROXY ? { server: process.env.HTTPS_PROXY } : undefined,
  });
  const ctx = await browser.newContext({ locale: 'es-ES', viewport: { width: 1280, height: 1800 } });
  const page = await ctx.newPage();
  await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 45000 });
  await page.waitForLoadState('networkidle', { timeout: 15000 }).catch(() => {});
  await quitarCookies(page);
  return { browser, page };
}

// Acepta el aviso de cookies si tapa la página. Solo pulsa botones de aceptar, nunca de configurar.
async function quitarCookies(page) {
  const re = /^(aceptar( todas?| todo| cookies)?|acepto|accept( all)?|allow all|permitir todas?|de acuerdo|entendido|ok)$/i;
  for (const frame of page.frames()) {
    const botones = frame.locator('button, a[role=button], input[type=button], input[type=submit]');
    const n = Math.min(await botones.count().catch(() => 0), 60);
    for (let i = 0; i < n; i++) {
      const b = botones.nth(i);
      const t = ((await b.innerText().catch(() => '')) || (await b.getAttribute('value').catch(() => '')) || '').trim();
      if (re.test(t) && (await b.isVisible().catch(() => false))) {
        await b.click({ timeout: 3000 }).catch(() => {});
        await page.waitForTimeout(800);
        return;
      }
    }
  }
}

// Casillas con estilo propio: si el clic normal no cambia el estado, se pulsa su etiqueta
// y, como último recurso, se marca por código avisando al formulario del cambio.
async function marcar(page, el, valor) {
  if (await el.setChecked(valor, { timeout: 5000 }).then(() => true).catch(() => false)) return;
  const id = await el.getAttribute('id');
  if (id) await page.locator(`label[for="${id}"]`).first().click({ timeout: 3000 }).catch(() => {});
  if ((await el.isChecked()) === valor) return;
  await el.evaluate((e, v) => {
    e.checked = v;
    e.dispatchEvent(new Event('input', { bubbles: true }));
    e.dispatchEvent(new Event('change', { bubbles: true }));
  }, valor);
  if ((await el.isChecked()) !== valor) throw new Error('No he podido marcar la casilla ' + (id || ''));
}

async function detectarCaptcha(page) {
  return page.evaluate(() => {
    const html = document.documentElement.innerHTML;
    const visibles = [...document.querySelectorAll('iframe')].map(f => f.src || '');
    const tipos = [];
    if (visibles.some(s => /recaptcha\/(api2|enterprise)\/anchor/.test(s)) || document.querySelector('.g-recaptcha:not([data-size=invisible])'))
      tipos.push('reCAPTCHA con casilla');
    else if (/recaptcha\/api\.js\?render=|grecaptcha\.execute|recaptcha\/enterprise\.js/.test(html))
      tipos.push('reCAPTCHA invisible (v3)');
    if (document.querySelector('.h-captcha') || visibles.some(s => /hcaptcha/.test(s))) tipos.push('hCaptcha');
    if (document.querySelector('.cf-turnstile') || visibles.some(s => /challenges\.cloudflare/.test(s))) tipos.push('Cloudflare Turnstile');
    return tipos;
  });
}

async function inspeccionar(url) {
  const { browser, page } = await abrir(url);
  const datos = await page.evaluate(() => {
    const etiqueta = el => {
      if (el.id) { const l = document.querySelector(`label[for="${CSS.escape(el.id)}"]`); if (l) return l.innerText.trim(); }
      const p = el.closest('label'); if (p) return p.innerText.trim();
      return (el.getAttribute('aria-label') || el.placeholder || '').trim();
    };
    const selector = (el, i) => {
      if (el.id) return `#${CSS.escape(el.id)}`;
      if (el.name) return `form:nth-of-type(${i + 1}) [name="${el.name}"]`;
      return null;
    };
    const forms = [...document.querySelectorAll('form')].map((f, i) => ({
      indice: i,
      accion: f.getAttribute('action') || '',
      visible: !!(f.offsetWidth || f.offsetHeight),
      campos: [...f.querySelectorAll('input, textarea, select')]
        .filter(e => !['hidden', 'submit', 'button', 'image', 'reset'].includes(e.type))
        .map(e => ({
          selector: selector(e, i), tipo: e.tagName === 'INPUT' ? e.type : e.tagName.toLowerCase(),
          nombre: e.name || '', etiqueta: etiqueta(e).slice(0, 150), obligatorio: e.required || e.getAttribute('aria-required') === 'true',
          opciones: e.tagName === 'SELECT' ? [...e.options].map(o => o.text.trim()).slice(0, 30) : undefined,
        })),
      botones: [...f.querySelectorAll('button, input[type=submit]')].map(b => (b.innerText || b.value || '').trim()).filter(Boolean),
    })).filter(f => f.campos.length);
    const enlaces = [...document.querySelectorAll('a[href]')]
      .filter(a => /contact|contacto|escr[ií]benos|hablemos/i.test(a.href + ' ' + a.innerText))
      .map(a => a.href).filter((v, i, s) => s.indexOf(v) === i).slice(0, 10);
    const emails = [...new Set([
      ...[...document.querySelectorAll('a[href^="mailto:"]')].map(a => a.href.slice(7).split('?')[0]),
      ...(document.body.innerText.match(/[\w.+-]+@[\w-]+\.[\w.-]+/g) || []),
    ])].slice(0, 10);
    return { titulo: document.title, formularios: forms, enlaces_contacto: enlaces, emails_publicados: emails };
  });
  datos.url = page.url();
  datos.captcha = await detectarCaptcha(page);
  await browser.close();
  console.log(JSON.stringify(datos, null, 2));
}

async function enviar(url, mapaPath, captura, prueba) {
  const mapa = JSON.parse(fs.readFileSync(mapaPath, 'utf8'));
  const { browser, page } = await abrir(url);
  const res = { url, enviado: false, veredicto: 'dudoso', respuestas: [], errores: [] };
  try {
    res.captcha = await detectarCaptcha(page);
    if (res.captcha.some(t => !/invisible/.test(t))) {
      res.veredicto = 'captcha';
      await page.screenshot({ path: captura, fullPage: true });
      return;
    }
    for (const c of mapa.campos) {
      const el = page.locator(c.selector).first();
      await el.scrollIntoViewIfNeeded({ timeout: 5000 }).catch(() => {});
      if (c.marcar !== undefined) await marcar(page, el, !!c.marcar);
      else if (c.opcion !== undefined) await el.selectOption({ label: c.opcion }, { timeout: 8000 })
        .catch(() => el.selectOption(c.opcion, { timeout: 8000 }));
      else await el.fill(String(c.valor), { timeout: 8000 });
    }
    const form = page.locator('form').nth(mapa.formulario ?? 0);
    const boton = mapa.boton ? page.locator(mapa.boton).first()
      : form.locator('button[type=submit], input[type=submit], button:not([type])').first();
    if (prueba) {
      res.veredicto = 'prueba';
      await page.screenshot({ path: captura, fullPage: true });
      return;
    }
    const urlAntes = page.url();
    page.on('response', async r => {
      if (r.request().method() !== 'POST') return;
      let cuerpo = '';
      try { if ((r.headers()['content-type'] || '').includes('json')) cuerpo = (await r.text()).slice(0, 300); } catch {}
      res.respuestas.push({ url: r.url().slice(0, 120), estado: r.status(), cuerpo });
    });
    await boton.click({ timeout: 10000 }).catch(() => boton.click({ force: true, timeout: 10000 }));
    res.enviado = true;
    await page.waitForLoadState('networkidle', { timeout: 15000 }).catch(() => {});
    await page.waitForTimeout(3000);
    const texto = await page.evaluate(() => document.body.innerText);
    const avisos = (texto.match(/[^\n]{0,80}(gracias|enviad[oa]|recibid[oa]|error|obligatori|inv[aá]lid|thank|success)[^\n]{0,80}/gi) || []).slice(0, 6);
    res.avisos = avisos;
    res.url_final = page.url();
    const jsonOk = res.respuestas.some(r => r.estado < 400 && OK.test(r.cuerpo) && !MAL.test(r.cuerpo));
    const jsonMal = res.respuestas.some(r => r.estado >= 400 || MAL.test(r.cuerpo));
    if (jsonOk || (avisos.some(a => OK.test(a)) && !avisos.some(a => MAL.test(a))) || (res.url_final !== urlAntes && OK.test(res.url_final)))
      res.veredicto = 'ok';
    else if (jsonMal || avisos.some(a => MAL.test(a))) res.veredicto = 'error';
    await page.screenshot({ path: captura, fullPage: true });
  } catch (e) {
    res.errores.push(String(e.message || e).split('\n')[0]);
    await page.screenshot({ path: captura, fullPage: true }).catch(() => {});
  } finally {
    await browser.close();
    console.log(JSON.stringify(res, null, 2));
  }
}

const [, , cmd, url, a, b, c] = process.argv;
if (cmd === 'inspeccionar' && url) inspeccionar(url).catch(e => { console.error(e.message); process.exit(1); });
else if (cmd === 'enviar' && url && a && b) enviar(url, a, b, c === '--prueba').catch(e => { console.error(e.message); process.exit(1); });
else { console.error('Uso: inspeccionar <url> | enviar <url> <mapa.json> <captura.png> [--prueba]'); process.exit(2); }
