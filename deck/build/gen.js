const pptxgen = require("pptxgenjs");
const P = new pptxgen();
P.layout = "LAYOUT_WIDE";            // 13.3 x 7.5
P.author = "Rootflow Hydroponics";
P.title  = "Rootflow — Dossier de presentación";

const OSC="13301C", VERDE="1F4D2B", BROTE="8FBF6A", BLANCO="FFFFFF",
      TXT="1F2421", MUT="6E7B72", SUAVE="EEF4EA", LINEA="D8E3D5";
const HF="Cambria", BF="Calibri";
const W=13.3, M=0.7;

const pie = (s, oscuro=false) => s.addText(
  [{text:"ROOTFLOW HYDROPONICS", options:{bold:true}},
   {text:"   ·   MADRID   ·   rootflow.es"}],
  {x:M, y:6.95, w:W-2*M, h:0.3, fontSize:8, fontFace:BF,
   color: oscuro?"7A8C80":MUT, isTextBox:true, margin:0, charSpacing:1});

function base(eyebrow, titulo, oscuro=false, tam=34){
  const s=P.addSlide();
  s.background={color: oscuro?OSC:BLANCO};
  if(eyebrow) s.addText(eyebrow.toUpperCase(),{x:M,y:0.45,w:W-2*M,h:0.28,fontSize:10,bold:true,
    color: oscuro?BROTE:BROTE, fontFace:BF, charSpacing:3, isTextBox:true, margin:0});
  if(titulo) s.addText(titulo,{x:M,y:0.8,w:W-2*M,h:0.85,fontSize:tam,bold:true,
    color: oscuro?BLANCO:VERDE, fontFace:HF, isTextBox:true, margin:0});
  pie(s,oscuro);
  return s;
}

// tarjeta con tinte suave (sin barras ni franjas)
function tarjeta(s,x,y,w,h,{titulo,cuerpo,num,icono}){
  s.addShape(P.ShapeType.roundRect,{x,y,w,h,fill:{color:SUAVE},line:{color:LINEA,width:1},rectRadius:0.09});
  let ty=y+0.28;
  if(num!==undefined){
    s.addShape(P.ShapeType.ellipse,{x:x+0.3,y:y+0.26,w:0.46,h:0.46,fill:{color:VERDE},line:{color:VERDE,width:0}});
    s.addText(String(num),{x:x+0.3,y:y+0.26,w:0.46,h:0.46,fontSize:15,bold:true,color:BLANCO,
      align:"center",valign:"middle",fontFace:BF,isTextBox:true,margin:0});
  }
  if(icono!==undefined){
    s.addShape(P.ShapeType.ellipse,{x:x+0.3,y:y+0.26,w:0.46,h:0.46,fill:{color:BROTE},line:{color:BROTE,width:0}});
    s.addText(icono,{x:x+0.3,y:y+0.26,w:0.46,h:0.46,fontSize:15,bold:true,color:VERDE,
      align:"center",valign:"middle",fontFace:BF,isTextBox:true,margin:0});
  }
  const dx = (num!==undefined||icono!==undefined) ? 0.92 : 0.3;
  s.addText(titulo,{x:x+dx,y:ty,w:w-dx-0.3,h:0.42,fontSize:15,bold:true,color:VERDE,fontFace:BF,
    isTextBox:true,margin:0,valign:"middle"});
  s.addText(cuerpo,{x:x+0.3,y:ty+0.5,w:w-0.6,h:h-(ty-y)-0.72,fontSize:11.5,color:TXT,fontFace:BF,
    isTextBox:true,margin:0,lineSpacingMultiple:1.15});
}

// bloque de estadística grande
function stat(s,x,y,w,valor,etiqueta,{oscuro=false,size=32}={}){
  s.addText(valor,{x,y,w,h:0.62,fontSize:size,bold:true,color: oscuro?BROTE:VERDE,fontFace:HF,
    isTextBox:true,margin:0,align:"left"});
  s.addText(etiqueta.toUpperCase(),{x,y:y+0.6,w,h:0.34,fontSize:8.5,color: oscuro?"9BAFA1":MUT,
    fontFace:BF,charSpacing:1.6,isTextBox:true,margin:0});
}

/* ─────────── 1 · PORTADA ─────────── */
{
 const s=P.addSlide(); s.background={color:OSC};
 s.addShape(P.ShapeType.ellipse,{x:9.9,y:-1.5,w:6,h:6,fill:{color:VERDE},line:{width:0}});
 s.addShape(P.ShapeType.ellipse,{x:11.3,y:4.4,w:3.4,h:3.4,fill:{color:"1A3D24"},line:{width:0}});
 s.addText("DOSSIER DE PRESENTACIÓN",{x:M,y:1.55,w:8,h:0.3,fontSize:10.5,bold:true,color:BROTE,
   fontFace:BF,charSpacing:3.4,isTextBox:true,margin:0});
 s.addText("Microbrotes vivos,\ncultivados en Madrid.",{x:M,y:2.1,w:8.6,h:2.1,fontSize:50,bold:true,
   color:BLANCO,fontFace:HF,isTextBox:true,margin:0,lineSpacingMultiple:1.02});
 s.addText("Hidroponía de precisión · Cosecha viva bajo pedido · KM 0",
   {x:M,y:4.35,w:8.6,h:0.4,fontSize:14,color:BROTE,fontFace:BF,isTextBox:true,margin:0});
 s.addText("SEPTIEMBRE 2026",{x:M,y:5.9,w:5,h:0.3,fontSize:9.5,bold:true,color:"7A8C80",
   fontFace:BF,charSpacing:2.6,isTextBox:true,margin:0});
 s.addNotes("Deck de inversores. Estructura: entrada en capital del 10 % por 100.000 €.");
}

/* ─────────── 2 · QUIÉNES SOMOS ─────────── */
{
 const s=base("Sobre nosotros","Cultivamos como artesanos.\nOperamos como una empresa.");
 s.addText("Rootflow Hydroponics nace en Madrid en 2026 con una idea simple: que la cocina profesional reciba el microbrote vivo, en su mejor momento, horas después del corte.\n\nCultivamos con hidroponía LED de precisión y cosechamos solo bajo pedido, para distribución, mayoristas y restauración. Sin stock, sin merma y siempre a medida.",
  {x:M,y:2.5,w:6.4,h:2.6,fontSize:13,color:TXT,fontFace:BF,isTextBox:true,margin:0,lineSpacingMultiple:1.3});
 const bx=7.7, bw=2.4;
 [["KM 0","Producido en Madrid"],["+14","Variedades en producción"],
  ["24-48 h","De cosecha a entrega"],["100 %","Adaptado al cliente"]].forEach((d,i)=>{
   const x=bx+(i%2)*(bw+0.5), y=2.45+Math.floor(i/2)*1.45;
   stat(s,x,y,bw,d[0],d[1],{size:26});
 });
 s.addText("Producto vivo, gourmet, de cercanía.",{x:M,y:5.6,w:7,h:0.4,fontSize:13,italic:true,
   color:VERDE,fontFace:HF,isTextBox:true,margin:0});
}

/* ─────────── 3 · EL SECTOR ─────────── */
{
 const s=base("Contexto de mercado","Categoría joven, crecimiento a doble dígito.",false,30);
 s.addText("El microbrote ya no es una rareza de alta cocina: es una categoría global de ~3.000 M$ que duplicará su tamaño esta década, y Europa lidera el mercado.",
  {x:M,y:1.78,w:11.9,h:0.6,fontSize:13,color:TXT,fontFace:BF,isTextBox:true,margin:0});
 [["~3.000 M$","Mercado global 2025"],["× 2","Tamaño previsto 2031"],
  ["+11 %","Crecimiento anual (CAGR)"],["~36 %","Cuota de Europa"]].forEach((d,i)=>{
   stat(s,M+i*3.0,2.55,2.8,d[0],d[1],{size:29});
 });
 [["S","Salud","El microbrote concentra hasta 40 veces más nutrientes que la hortaliza adulta."],
  ["P","Proximidad","Consumidor y restauración premian el producto local, fresco y sostenible."],
  ["T","Tecnología","El cultivo vertical indoor es el formato que más crece (12,5 % anual)."]]
 .forEach((d,i)=>tarjeta(s,M+i*4.0,3.95,3.7,1.75,{icono:d[0],titulo:d[1],cuerpo:d[2]}));
 s.addText("Rootflow opera en el cruce exacto de estas tendencias: microbrote premium, cultivo vertical y KM 0.",
  {x:M,y:5.95,w:11.9,h:0.35,fontSize:11.5,italic:true,color:VERDE,fontFace:HF,isTextBox:true,margin:0});
 s.addText("Fuentes: Mordor Intelligence, Microgreens Market Report (ene. 2026) · Grand View Research.",
  {x:M,y:6.3,w:11.9,h:0.3,fontSize:8,color:MUT,fontFace:BF,isTextBox:true,margin:0});
}

/* ─────────── 4 · EL EQUIPO ─────────── */
{
 const s=base("El equipo","Tres socios, tres frentes cubiertos.");
 [["PD","Pedro Domecq Vergara","Administración & Finanzas","ADE (ICADE). Trayectoria en consultoría estratégica y Fusiones & Adquisiciones. Gestión financiera, administración y estructura societaria."],
  ["NB","Nicolás Bustamante Thams","Comercial & Hostelería","ADE (Richmond University). Desarrollo de negocio HORECA. Relación con restaurantes, distribuidores y apertura de mercado."],
  ["DG","Domingo de Guzmán Greus","Producción & Agrícola","Ingeniero Agrónomo (UPM). Formación en automatización con IA y Arduino. Cultivo, I+D de variedades y operativa de producción."]]
 .forEach((d,i)=>{
   const x=M+i*4.05;
   s.addShape(P.ShapeType.ellipse,{x,y:2.15,w:1.15,h:1.15,fill:{color:VERDE},line:{width:0}});
   s.addText(d[0],{x,y:2.15,w:1.15,h:1.15,fontSize:26,bold:true,color:BROTE,align:"center",
     valign:"middle",fontFace:HF,isTextBox:true,margin:0});
   s.addText(d[1],{x,y:3.5,w:3.7,h:0.5,fontSize:16,bold:true,color:VERDE,fontFace:HF,isTextBox:true,margin:0});
   s.addText(d[2].toUpperCase(),{x,y:4.0,w:3.7,h:0.3,fontSize:8.5,bold:true,color:BROTE,
     fontFace:BF,charSpacing:1.6,isTextBox:true,margin:0});
   s.addText(d[3],{x,y:4.38,w:3.7,h:1.7,fontSize:11.5,color:TXT,fontFace:BF,isTextBox:true,
     margin:0,lineSpacingMultiple:1.2});
 });
}

/* ─────────── 5 · PRODUCTO ─────────── */
{
 const s=base("Producto","Pocos gramos. Mucho valor.");
 s.addText("Microbrotes y flores comestibles de máxima frescura, cosechados en su punto exacto de sabor, aroma y color. Producto de bajo gramaje y altísimo valor: unos pocos gramos cambian un plato y la percepción de toda una carta.",
  {x:M,y:2.3,w:6.2,h:1.7,fontSize:13,color:TXT,fontFace:BF,isTextBox:true,margin:0,lineSpacingMultiple:1.3});
 [["14 + 5","variedades en producción, y cinco más en desarrollo"],
  ["5-100 g","cualquier gramaje: bandeja viva, granel o monodosis"],
  ["6-10 días","de vida útil según variedad, gracias al corte en vivo"]]
 .forEach((d,i)=>{
   const y=2.35+i*1.25;
   s.addText(d[0],{x:7.5,y,w:2.1,h:0.55,fontSize:24,bold:true,color:VERDE,fontFace:HF,isTextBox:true,margin:0});
   s.addText(d[1],{x:9.7,y:y+0.1,w:2.9,h:0.8,fontSize:11.5,color:TXT,fontFace:BF,isTextBox:true,
     margin:0,lineSpacingMultiple:1.15});
 });
}

/* ─────────── 6 · PROPUESTA DE VALOR ─────────── */
{
 const s=base("Propuesta de valor","Producto gourmet de cercanía, sin atajos.");
 [["I","KM 0 real","Cultivado y entregado en Madrid. Una frescura que el producto importado o de larga distribución no puede igualar."],
  ["II","Estructura ágil","Decisiones rápidas y producción a medida: la agilidad propia de un equipo pequeño y especializado."],
  ["III","Origen directo","Trato directo con quien cultiva: respuesta inmediata, transparencia y control real del origen."],
  ["IV","Cosecha viva","El producto llega vivo y sigue creciendo. Aroma, color y textura intactos hasta el emplatado."]]
 .forEach((d,i)=>tarjeta(s,M+(i%2)*6.05,2.1+Math.floor(i/2)*2.2,5.85,1.95,
   {icono:d[0],titulo:d[1],cuerpo:d[2]}));
}

/* ─────────── 7 · LA GAMA ─────────── */
{
 const s=base("La gama","14 variedades. Y las que pida el mercado.");
 const v=["Cilantro","Hinojo","Rábano rojo","Guisante","Remolacha amarilla","Albahaca genovesa",
   "Cebollino chino","Rábano daikon","Albahaca morada","Remolacha roja","Cebolla Barbra",
   "Mostaza Red Giant","Rábano pink","Amaranto rojo"];
 v.forEach((n,i)=>{
   const col=Math.floor(i/5), fila=i%5;
   const x=M+col*4.05, y=2.15+fila*0.66;
   s.addText(String(i+1).padStart(2,"0"),{x,y,w:0.42,h:0.42,fontSize:11,bold:true,color:BROTE,
     fontFace:BF,isTextBox:true,margin:0,valign:"middle"});
   s.addText(n,{x:x+0.45,y,w:3.3,h:0.42,fontSize:13,color:TXT,fontFace:BF,isTextBox:true,
     margin:0,valign:"middle"});
 });
 s.addText("+ flores comestibles",{x:M+2*4.05,y:2.15+4*0.66,w:3.7,h:0.42,fontSize:13,bold:true,
   color:VERDE,fontFace:BF,isTextBox:true,margin:0,valign:"middle"});
 s.addText("+5 variedades en desarrollo para una micromezcla co-desarrollada: la gama crece con cada cliente.",
  {x:M,y:5.85,w:11.9,h:0.4,fontSize:12,italic:true,color:VERDE,fontFace:HF,isTextBox:true,margin:0});
}

/* ─────────── 8 · MODELO ─────────── */
{
 const s=base("Modelo","Cosecha viva, cero stock.");
 [["Bajo pedido","Cortamos cuando nos lo pides. Producimos exactamente lo que se va a consumir: cero stock, cero merma, máxima frescura."],
  ["Hidroponía LED","Cultivo sin tierra y sin pesticidas, en condiciones controladas. Misma calidad y mismo calibre, las 52 semanas del año."],
  ["Flexibilidad total","De 5 a 100 g; bandeja viva, granel o monodosis. Formato, punto de corte y mezclas a medida de cada cliente."],
  ["Marca blanca","Tu etiqueta sobre nuestro producto. El distribuidor pone la marca; nosotros, la calidad y la constancia."]]
 .forEach((d,i)=>tarjeta(s,M+i*3.05,2.4,2.85,2.9,{titulo:d[0],cuerpo:d[1]}));
}

/* ─────────── 9 · PROCESO ─────────── */
{
 const s=base("Proceso","Del pedido a la mesa, en seis pasos.");
 [["Pedido","El cliente define variedad, formato y fecha. Producimos contra demanda real, no contra previsión."],
  ["Siembra","Bandeja a bandeja, sobre sustrato limpio y con densidad calibrada por variedad."],
  ["Oscuridad","Germinación en blackout (3-7 días) para lograr un brote uniforme y vigoroso."],
  ["Luz","Crecimiento bajo LED, con riego y clima controlados (2-13 días según variedad)."],
  ["Cosecha","Corte en vivo en el punto justo, o entrega en bandeja viva, sin cortar."],
  ["Entrega","En 24-48 h en Madrid, etiquetado a medida y con trazabilidad por lote."]]
 .forEach((d,i)=>tarjeta(s,M+(i%3)*4.05,2.1+Math.floor(i/3)*2.0,3.75,1.75,
   {num:i+1,titulo:d[0],cuerpo:d[1]}));
 s.addText("Todo el ciclo queda registrado en nuestro ERP: cada bandeja es trazable de la semilla a la entrega.",
  {x:M,y:6.25,w:11.9,h:0.35,fontSize:11.5,italic:true,color:VERDE,fontFace:HF,isTextBox:true,margin:0});
}

/* ─────────── 10 · OPERACIÓN ─────────── */
{
 const s=base("Operación","Sabemos cuánto producimos, al gramo.");
 s.addText("Cada variedad tiene su ciclo —germinación en oscuridad y crecimiento en luz— y un rendimiento por bandeja que medimos y registramos. Esa disciplina nos permite comprometer volúmenes y fechas con fiabilidad.",
  {x:M,y:1.78,w:11.9,h:0.6,fontSize:12.5,color:TXT,fontFace:BF,isTextBox:true,margin:0});
 const filas=[
  [{text:"VARIEDAD",options:{bold:true}},{text:"CICLO",options:{bold:true}},{text:"ROTACIÓN",options:{bold:true}},{text:"RENDIMIENTO",options:{bold:true}}],
  ["Rábano · ciclo corto","3 + 2 días","15 ciclos/mes","210 g / bandeja"],
  ["Cilantro · ciclo medio","6 + 9 días","3 ciclos/mes","135 g / bandeja"],
  ["Albahaca · ciclo largo","6 + 12 días","2,3 ciclos/mes","100 g / bandeja"]];
 s.addTable(filas,{x:M,y:2.6,w:11.9,colW:[4.0,2.6,2.6,2.7],rowH:0.48,fontSize:12,fontFace:BF,
   color:TXT,border:{type:"solid",color:LINEA,pt:1},fill:{color:BLANCO},valign:"middle",
   margin:[0,0.14,0,0.14]});
 s.addText("Estimación sobre 112 bandejas en luz simultánea (4 racks) · mix comercial: 40 % ciclo corto, 40 % medio, 20 % largo.",
  {x:M,y:4.68,w:11.9,h:0.3,fontSize:9.5,color:MUT,fontFace:BF,isTextBox:true,margin:0});
 s.addShape(P.ShapeType.roundRect,{x:M,y:5.15,w:11.9,h:1.1,fill:{color:SUAVE},line:{color:LINEA,width:1},rectRadius:0.09});
 s.addText([{text:"Capacidad actual: ",options:{bold:true,color:VERDE}},
   {text:"~160 kg/mes con mix comercial de variedades · pico de ~350 kg/mes en monocultivo de ciclo corto.",options:{color:TXT}}],
  {x:M+0.35,y:5.15,w:11.2,h:1.1,fontSize:13,fontFace:BF,isTextBox:true,margin:0,valign:"middle"});
}

/* ─────────── 11 · TECNOLOGÍA ─────────── */
{
 const s=base("Tecnología","Un ERP a medida, construido desde cero.");
 s.addText("No adaptamos un software genérico: hemos construido nuestro propio ERP. Pedidos, producción, trazabilidad y facturación viven en un único sistema diseñado para cómo trabajamos.\n\nY el siguiente paso ya está dibujado: cuando la nave incorpore sensórica de clima y riego, esos datos se volcarán directamente al sistema.",
  {x:M,y:2.3,w:6.0,h:2.4,fontSize:12.5,color:TXT,fontFace:BF,isTextBox:true,margin:0,lineSpacingMultiple:1.3});
 s.addText("React · Supabase · datos en tiempo real",{x:M,y:4.9,w:6.0,h:0.4,fontSize:12,italic:true,
   color:VERDE,fontFace:HF,isTextBox:true,margin:0});
 ["Pedidos, clientes y facturación en un único flujo",
  "Planificación de producción y trazabilidad por lote",
  "Stock estimado y rendimiento real por variedad",
  "Preparado para conectar la sensórica de la nave"].forEach((t,i)=>{
   const y=2.3+i*0.78;
   s.addShape(P.ShapeType.ellipse,{x:7.4,y:y+0.06,w:0.34,h:0.34,fill:{color:BROTE},line:{width:0}});
   s.addText("✓",{x:7.4,y:y+0.06,w:0.34,h:0.34,fontSize:12,bold:true,color:VERDE,align:"center",
     valign:"middle",fontFace:BF,isTextBox:true,margin:0});
   s.addText(t,{x:7.9,y,w:4.7,h:0.48,fontSize:12.5,color:TXT,fontFace:BF,isTextBox:true,margin:0,valign:"middle"});
 });
 s.addText("Hoy gestiona el negocio; mañana, también el cultivo.",{x:7.4,y:5.45,w:5.2,h:0.4,
   fontSize:12,italic:true,color:VERDE,fontFace:HF,isTextBox:true,margin:0});
}

/* ─────────── 12 · TRACCIÓN ─────────── */
{
 const s=base("Tracción","Pequeños, pero ya facturando.");
 s.addText("Operamos desde un local de 58 m² en Madrid con cuatro racks en producción continua. Una base compacta y eficiente que ya genera ingresos recurrentes.",
  {x:M,y:1.8,w:11.9,h:0.55,fontSize:13,color:TXT,fontFace:BF,isTextBox:true,margin:0});
 [["58 m²","Local actual"],["4","Racks en continuo"],["2","Clientes facturando"]]
  .forEach((d,i)=>stat(s,M+i*3.1,2.6,2.9,d[0],d[1],{size:38}));
 tarjeta(s,M,4.0,5.85,2.0,{titulo:"Clientes activos",
   cuerpo:"Dos distribuidores con pedido semanal recurrente, uno de ellos con acuerdo de consignación en marcha en Mercamadrid."});
 tarjeta(s,M+6.05,4.0,5.85,2.0,{titulo:"Ya co-desarrollamos",
   cuerpo:"Una micromezcla exclusiva para uno de nuestros distribuidores, que incorpora 5 variedades nuevas a la gama. El co-desarrollo no es una promesa: ya lo estamos haciendo."});
}

/* ─────────── 13 · HOJA DE RUTA ─────────── */
{
 const s=base("Hoja de ruta","De la idea al grupo, en seis hitos.");
 [["00","Constituir","Hecho","Sociedad creada y planta de 58 m² operativa."],
  ["01","Validar","Hecho","MVP validado y 2 distribuidores recurrentes."],
  ["02","Financiar","En curso","Break-even, cartera estable y ronda cerrada."],
  ["03","Escalar","Próximo","Nave en marcha, 2 grandes clientes y 1er empleado."],
  ["04","Diversificar","Próximo","Nuevas líneas y adquisiciones con caja estable."],
  ["05","Consolidar","Próximo","Grupo o holding con Rootflow como OpCo."]]
 .forEach((d,i)=>{
   const x=M+i*2.02, hecho=d[2]!=="Próximo";
   s.addShape(P.ShapeType.ellipse,{x,y:2.35,w:0.62,h:0.62,
     fill:{color: hecho?VERDE:SUAVE},line:{color: hecho?VERDE:LINEA,width:1.5}});
   s.addText(d[0],{x,y:2.35,w:0.62,h:0.62,fontSize:12,bold:true,color: hecho?BROTE:MUT,
     align:"center",valign:"middle",fontFace:BF,isTextBox:true,margin:0});
   s.addText(d[2].toUpperCase(),{x,y:3.12,w:1.85,h:0.26,fontSize:8,bold:true,
     color: d[2]==="En curso"?BROTE:MUT,fontFace:BF,charSpacing:1.2,isTextBox:true,margin:0});
   s.addText(d[1],{x,y:3.4,w:1.85,h:0.4,fontSize:15,bold:true,color:VERDE,fontFace:HF,isTextBox:true,margin:0});
   s.addText(d[3],{x,y:3.85,w:1.85,h:1.6,fontSize:10.5,color:TXT,fontFace:BF,isTextBox:true,
     margin:0,lineSpacingMultiple:1.15});
 });
 s.addText("El conocimiento ya está adquirido: producto, clientes, ERP y operación validados antes de pedir un euro.",
  {x:M,y:5.8,w:11.9,h:0.4,fontSize:12,italic:true,color:VERDE,fontFace:HF,isTextBox:true,margin:0});
}

/* ─────────── 14 · EL SALTO ─────────── */
{
 const s=base("Hoja de ruta · hito 3","El salto: de 58 m² a una nave de 350 m².");
 s.addText("En 3-6 meses trasladamos la producción a una nave de 350 m² en el sur de Madrid. Tres racks de gran formato suman 2.880 posiciones de luz y llevan la superficie de cultivo a 432 m².\n\nCon el mismo mix de variedades que hoy, la capacidad pasa de ~160 a ~2.900 kg al mes: volumen suficiente para servir distribución a escala manteniendo el modelo de cosecha viva bajo pedido.",
  {x:M,y:2.25,w:6.2,h:2.5,fontSize:12.5,color:TXT,fontFace:BF,isTextBox:true,margin:0,lineSpacingMultiple:1.3});
 s.addText("Nave en alquiler para no inmovilizar capital.",{x:M,y:4.9,w:6.2,h:0.4,fontSize:12,
   italic:true,color:VERDE,fontFace:HF,isTextBox:true,margin:0});
 [["350 m²","Nave · sur de Madrid"],["432 m²","Superficie de cultivo"],
  ["× 18","Capacidad vs. hoy"],["~2.900 kg","Al mes · mismo mix"]].forEach((d,i)=>{
   stat(s,7.5+(i%2)*2.6,2.3+Math.floor(i/2)*1.5,2.5,d[0],d[1],{size:27});
 });
 s.addText("Concebida para automatizarse por fases: sensórica y control de clima y riego, con datos en tiempo real integrados en el ERP.",
  {x:M,y:5.95,w:11.9,h:0.35,fontSize:11.5,italic:true,color:VERDE,fontFace:HF,isTextBox:true,margin:0});
}

/* ─────────── 15 · LA RONDA  (ACTUALIZADO) ─────────── */
{
 const s=base("La ronda","Buscamos 100.000 € para dar el salto.");
 // capital stack
 s.addText("CAPITAL STACK",{x:M,y:1.85,w:6.0,h:0.28,fontSize:9,bold:true,color:BROTE,fontFace:BF,
   charSpacing:2,isTextBox:true,margin:0});
 const stack=[["Inversor privado · propuesta","100.000 €"],["ENISA AgroInnpulso · en tramitación","100.000 €"],
   [{text:"Total levantado",options:{bold:true}},{text:"200.000 €",options:{bold:true}}]];
 s.addTable(stack,{x:M,y:2.2,w:6.0,colW:[4.0,2.0],rowH:0.45,fontSize:12,fontFace:BF,color:TXT,
   border:{type:"solid",color:LINEA,pt:1},fill:{color:BLANCO},valign:"middle",margin:[0,0.12,0,0.12]});
 s.addText("Cubre la necesidad de 161.278 € del plan · cobertura 1,24×",
  {x:M,y:3.62,w:6.0,h:0.3,fontSize:10.5,color:MUT,fontFace:BF,isTextBox:true,margin:0});
 // retorno
 s.addText("RETORNO PARA EL INVERSOR · ESCENARIO BASE",{x:7.1,y:1.85,w:5.5,h:0.28,fontSize:9,bold:true,
   color:BROTE,fontFace:BF,charSpacing:2,isTextBox:true,margin:0});
 [["35 %","TIR anual"],["3,3×","MOIC"],["Año 4","Horizonte de salida"]]
  .forEach((d,i)=>stat(s,7.1+i*1.9,2.2,1.8,d[0],d[1],{size:30}));
 // condiciones
 s.addShape(P.ShapeType.roundRect,{x:M,y:4.15,w:11.9,h:1.5,fill:{color:SUAVE},line:{color:LINEA,width:1},rectRadius:0.09});
 s.addText("CONDICIONES · TRAMO INVERSOR",{x:M+0.35,y:4.32,w:11.2,h:0.28,fontSize:9,bold:true,
   color:VERDE,fontFace:BF,charSpacing:2,isTextBox:true,margin:0});
 s.addText("Entrada en capital: 10 % de la sociedad por 100.000 € · derecho de salida pactado a partir del año 4 · suelo de protección de 1,5× sobre lo invertido · sin aval personal · los fundadores conservan el 90 % y el control.",
  {x:M+0.35,y:4.62,w:11.2,h:0.95,fontSize:12.5,color:TXT,fontFace:BF,isTextBox:true,margin:0,lineSpacingMultiple:1.2});
 s.addText("ENISA exige fondos propios iguales o superiores al préstamo. El tramo privado entra como capital precisamente para cumplirlo: cada euro del inversor desbloquea otro euro público.",
  {x:M,y:5.8,w:11.9,h:0.5,fontSize:11.5,italic:true,color:VERDE,fontFace:HF,isTextBox:true,margin:0});
 s.addText("Colchón de seguridad: caja mínima de 30.000 €, DSCR de 11,4× en los años 2-7 y circulante financiado con póliza de crédito, no con la ronda.",
  {x:M,y:6.32,w:11.9,h:0.3,fontSize:9.5,color:MUT,fontFace:BF,isTextBox:true,margin:0});
 s.addNotes("Estructura V15: capital 10 % por 100.000 €, salida desde el año 4, suelo 1,5×. Verificado con el modelo financiero V15.");
}

/* ─────────── 16 · PROYECCIÓN ─────────── */
{
 const s=base("Inversión","Del arranque al régimen pleno.");
 s.addText("El Año 1 va en pérdidas (EBITDA −52 k€): es la nave llenándose y la plantilla entrando antes que los ingresos. A partir de ahí la facturación sube cliente a cliente hasta el régimen: ~1,30 M€ y un 35 % de margen EBITDA.",
  {x:M,y:1.8,w:11.9,h:0.55,fontSize:12.5,color:TXT,fontFace:BF,isTextBox:true,margin:0});
 s.addChart(P.ChartType.bar,
  [{name:"Ingresos (€)",labels:["Año 1","Año 2","Año 3","Año 4","Régimen"],
    values:[183000,686000,1033000,1274000,1303000]}],
  {x:M,y:2.5,w:6.6,h:3.5,barDir:"col",chartColors:[VERDE],
   showTitle:false,showLegend:false,showValue:true,dataLabelPosition:"outEnd",
   dataLabelFormatCode:'#,##0,"k"',dataLabelFontSize:9,dataLabelColor:TXT,dataLabelFontFace:BF,
   catAxisLabelColor:MUT,catAxisLabelFontSize:10,catAxisLabelFontFace:BF,
   valAxisLabelColor:MUT,valAxisLabelFontSize:9,valAxisLabelFontFace:BF,valAxisHidden:true,
   valGridLine:{style:"none"},catGridLine:{style:"none"},barGapWidthPct:45});
 const t=[
  [{text:"CONCEPTO",options:{bold:true}},{text:"AÑO 1",options:{bold:true}},{text:"AÑO 3",options:{bold:true}},{text:"RÉGIMEN",options:{bold:true}}],
  ["Ingresos","183 k€","1,03 M€","1,30 M€"],
  ["EBITDA","−52 k€","350 k€","460 k€"],
  ["Margen EBITDA","−28 %","34 %","35 %"]];
 s.addTable(t,{x:7.5,y:2.7,w:5.1,colW:[1.8,1.1,1.1,1.1],rowH:0.5,fontSize:11,fontFace:BF,color:TXT,
   border:{type:"solid",color:LINEA,pt:1},fill:{color:BLANCO},valign:"middle",margin:[0,0.1,0,0.1]});
 s.addText("Apalancamiento operativo: las palancas —minutos por bandeja, precio y coste— llevan el margen EBITDA en régimen del 11 % (conservador) al 50 % (optimista).",
  {x:7.5,y:4.9,w:5.1,h:1.0,fontSize:11.5,italic:true,color:VERDE,fontFace:HF,isTextBox:true,
   margin:0,lineSpacingMultiple:1.2});
 s.addText("Escenario base del modelo financiero V15 · régimen pleno en el año 5 · cifras sin IVA.",
  {x:M,y:6.25,w:11.9,h:0.3,fontSize:9,color:MUT,fontFace:BF,isTextBox:true,margin:0});
}

/* ─────────── 17 · ESCENARIOS  (ACTUALIZADO) ─────────── */
{
 const s=base("Escenarios","Un modelo, tres casos.");
 s.addText("El Base es el plan de negocio. Cambiar una sola palanca —los minutos por bandeja, el precio o la automatización— recalcula plantilla, EBITDA, caja y retorno del inversor.",
  {x:M,y:1.8,w:11.9,h:0.55,fontSize:12.5,color:TXT,fontFace:BF,isTextBox:true,margin:0});
 const casos=[
  ["CONSERVADOR","10,7 %","1,50×","0,79 M€","1,03 M€","115 k€ · 11%",false],
  ["BASE","35,1 %","3,33×","3,33 M€","1,30 M€","460 k€ · 35%",true],
  ["OPTIMISTA","53,2 %","5,51×","5,51 M€","1,52 M€","757 k€ · 50%",false]];
 casos.forEach((c,i)=>{
   const x=M+i*4.05, w=3.75, dest=c[6];
   s.addShape(P.ShapeType.roundRect,{x,y:2.45,w,h:3.5,fill:{color: dest?VERDE:SUAVE},
     line:{color: dest?VERDE:LINEA,width:1},rectRadius:0.09});
   s.addText(c[0],{x:x+0.3,y:2.65,w:w-0.6,h:0.3,fontSize:9.5,bold:true,color: dest?BROTE:MUT,
     fontFace:BF,charSpacing:2,isTextBox:true,margin:0});
   s.addText(c[1],{x:x+0.3,y:2.98,w:w-0.6,h:0.72,fontSize:38,bold:true,color: dest?BLANCO:VERDE,
     fontFace:HF,isTextBox:true,margin:0});
   s.addText("TIR DEL INVERSOR",{x:x+0.3,y:3.68,w:w-0.6,h:0.26,fontSize:8,color: dest?"9BAFA1":MUT,
     fontFace:BF,charSpacing:1.4,isTextBox:true,margin:0});
   [["MOIC",c[2]],["Valor del equity a la salida",c[3]],["Ingresos · régimen",c[4]],["EBITDA régimen",c[5]]]
    .forEach((d,j)=>{
     const y=4.05+j*0.47;
     s.addText(d[0],{x:x+0.3,y,w:1.85,h:0.4,fontSize:9.5,color: dest?"9BAFA1":MUT,fontFace:BF,
       isTextBox:true,margin:0,valign:"middle"});
     s.addText(d[1],{x:x+2.1,y,w:1.35,h:0.4,fontSize:11,bold:true,color: dest?BLANCO:TXT,fontFace:BF,
       isTextBox:true,margin:0,align:"right",valign:"middle"});
   });
 });
 s.addText("En el caso conservador el suelo de protección de 1,5× garantiza al inversor 150.000 € sobre los 100.000 € aportados: recupera su dinero con rentabilidad aunque el plan se quede corto.",
  {x:M,y:6.1,w:11.9,h:0.45,fontSize:11.5,italic:true,color:VERDE,fontFace:HF,isTextBox:true,margin:0});
}

/* ─────────── 18 · PALANCAS ─────────── */
{
 const s=base("Palancas","Cuatro palancas de crecimiento.");
 [["I","Automatización","Sensórica y control de clima y riego recortan el coste de mano de obra —la mayor partida en cultivo vertical— y elevan la producción por m²."],
  ["II","Pricing","Hoy vendemos en el rango bajo del sector. Con marca y relación con chefs consolidadas, hay recorrido de subida hacia precios premium."],
  ["III","Mix premium","Más peso de flores comestibles y variedades de alto valor por kilo: sube el ticket medio sin subir el coste de producción."],
  ["IV","Nuevas líneas","Cada rack adicional escala sobre una estructura de costes fija. La misma base sostiene nuevas líneas y áreas de negocio."]]
 .forEach((d,i)=>tarjeta(s,M+(i%2)*6.05,2.1+Math.floor(i/2)*2.2,5.85,1.95,
   {icono:d[0],titulo:d[1],cuerpo:d[2]}));
}

/* ─────────── 19 · ESTRUCTURA  (REESCRITO) ─────────── */
{
 const s=base("Estructura","Entramos en capital porque ENISA lo exige.");
 [["I","Fondos propios ≥ préstamo","ENISA exige fondos propios iguales o superiores al importe solicitado. Un préstamo participativo privado es deuda: no computa. Para movilizar los 100.000 € públicos, el tramo privado tiene que ser capital."],
  ["II","Suelo de 1,5×","El inversor cobra el mayor de estos dos: su 10 % del valor de la compañía, o 1,5× lo aportado. Recupera con rentabilidad incluso en el escenario conservador."],
  ["III","Salida pactada desde el año 4","Sin dividendos hasta amortizar ENISA. El retorno llega por un derecho de salida acordado desde el inicio, no por un cupón."],
  ["IV","Los fundadores conservan el 90 %","Participación minoritaria sin derechos de veto sobre la operativa. El control no se toca."]]
 .forEach((d,i)=>tarjeta(s,M+(i%2)*6.05,2.05+Math.floor(i/2)*2.1,5.85,1.9,
   {icono:d[0],titulo:d[1],cuerpo:d[2]}));
 s.addText("Estructura firmada vía nota convertible y capitalizada antes de que ENISA formalice, tal y como exige su procedimiento.",
  {x:M,y:6.15,w:11.9,h:0.4,fontSize:11.5,italic:true,color:VERDE,fontFace:HF,isTextBox:true,margin:0});
}

/* ─────────── 20 · CONTACTO ─────────── */
{
 const s=P.addSlide(); s.background={color:OSC};
 s.addShape(P.ShapeType.ellipse,{x:-1.8,y:4.0,w:5.2,h:5.2,fill:{color:VERDE},line:{width:0}});
 s.addText("CONOZCÁMONOS",{x:M,y:2.0,w:8,h:0.3,fontSize:10.5,bold:true,color:BROTE,fontFace:BF,
   charSpacing:3.4,isTextBox:true,margin:0});
 s.addText("Hablemos.",{x:M,y:2.5,w:9,h:1.2,fontSize:56,bold:true,color:BLANCO,fontFace:HF,
   isTextBox:true,margin:0});
 s.addText("Nos encantaría explorar juntos cómo sumaros a este proyecto.",
  {x:M,y:3.8,w:9,h:0.45,fontSize:15,color:BROTE,fontFace:BF,isTextBox:true,margin:0});
 s.addText([{text:"Pedro Domecq",options:{bold:true,color:BLANCO,fontSize:16}},
   {text:"   ·   Rootflow Hydroponics, S.L.",options:{color:"9BAFA1",fontSize:13}}],
  {x:M,y:4.9,w:9,h:0.4,fontFace:BF,isTextBox:true,margin:0});
 s.addText("+34 638 16 19 90      ·      p.domecq@rootflow.es      ·      rootflow.es",
  {x:M,y:5.35,w:9.5,h:0.4,fontSize:13,color:BROTE,fontFace:BF,isTextBox:true,margin:0});
 pie(s,true);
}

P.writeFile({fileName:"Rootflow_Deck_Inversores_V15.pptx"}).then(f=>console.log("Escrito:",f));
