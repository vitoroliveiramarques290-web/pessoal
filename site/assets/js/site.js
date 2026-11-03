/* Berdinazi & Mezenga — página única.
   Simulação ilustrativa: as premissas são editáveis e não são resultados observados em fazenda real.
   Fórmulas: Ne = 4·M·F/(M+F); ΔF = 1/(2·Ne); F(t) = 1 − (1 − ΔF)^t (t em gerações). */
(function () {
  'use strict';
  var root = document.documentElement;
  var reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (reduce) root.classList.add('rm');
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return [].slice.call((r || document).querySelectorAll(s)); };
  var nf = function (v, d) {
    return Number(v).toLocaleString('pt-BR', { minimumFractionDigits: d || 0, maximumFractionDigits: d || 0 });
  };
  var brl = function (v) { return 'R$ ' + nf(v, 0); };

  /* ---------- cabeçalho, menu e progresso ---------- */
  var header = $('.site-header');
  var toggle = $('.nav-toggle');
  toggle.addEventListener('click', function () {
    var open = document.body.classList.toggle('nav-open');
    toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
  });
  $$('.nav a').forEach(function (a) {
    a.addEventListener('click', function () {
      document.body.classList.remove('nav-open');
      toggle.setAttribute('aria-expanded', 'false');
    });
  });
  var bar = $('.progress i');
  function onScroll() {
    var max = root.scrollHeight - innerHeight;
    var p = max > 0 ? scrollY / max : 0;
    bar.style.transform = 'scaleX(' + Math.min(1, Math.max(0, p)) + ')';
    header.classList.toggle('solid', scrollY > 24);
    if (sticky) stickyTick();
  }
  addEventListener('scroll', onScroll, { passive: true });
  addEventListener('resize', onScroll);

  /* seção ativa no menu */
  var links = $$('.nav a');
  var linkFor = {};
  links.forEach(function (a) { linkFor[a.getAttribute('href').slice(1)] = a; });
  var navIO = new IntersectionObserver(function (es) {
    es.forEach(function (e) {
      if (!e.isIntersecting) return;
      links.forEach(function (l) { l.classList.remove('on'); l.removeAttribute('aria-current'); });
      var a = linkFor[e.target.id];
      if (a) { a.classList.add('on'); a.setAttribute('aria-current', 'true'); }
    });
  }, { rootMargin: '-45% 0px -50% 0px' });
  Object.keys(linkFor).forEach(function (id) { var s = document.getElementById(id); if (s) navIO.observe(s); });

  /* ---------- revelação, palavras e números ---------- */
  function splitWords(el) {
    var idx = 0;
    (function walk(node) {
      [].slice.call(node.childNodes).forEach(function (c) {
        if (c.nodeType === 3) {
          var frag = document.createDocumentFragment();
          c.textContent.split(/(\s+)/).forEach(function (part) {
            if (!part) return;
            if (/^\s+$/.test(part)) { frag.appendChild(document.createTextNode(part)); return; }
            var s = document.createElement('span');
            s.className = 'w';
            s.style.setProperty('--i', idx++);
            s.textContent = part;
            frag.appendChild(s);
          });
          node.replaceChild(frag, c);
        } else if (c.nodeType === 1) { walk(c); }
      });
    })(el);
  }
  if (!reduce) $$('.words').forEach(splitWords);

  function countUp(el) {
    var to = parseFloat(el.getAttribute('data-count'));
    var suf = el.getAttribute('data-suffix') || '';
    var dec = parseInt(el.getAttribute('data-dec') || '0', 10);
    if (reduce) { el.textContent = nf(to, dec) + suf; return; }
    var t0 = null, dur = 1100;
    (function step(t) {
      if (t0 === null) t0 = t;
      var k = Math.min(1, (t - t0) / dur);
      var e = 1 - Math.pow(1 - k, 3);
      el.textContent = nf(to * e, dec) + suf;
      if (k < 1) requestAnimationFrame(step);
    })(performance.now());
  }

  var revealIO = new IntersectionObserver(function (es) {
    es.forEach(function (e) {
      if (!e.isIntersecting) return;
      var t = e.target;
      t.classList.add('in');
      if (t.hasAttribute('data-count')) countUp(t);
      if (t.classList.contains('chart') && !t.dataset.played) {
        t.dataset.played = '1';
        t.classList.add('play');
        setTimeout(function () { t.classList.remove('play'); }, 1800);
      }
      revealIO.unobserve(t);
    });
  }, { threshold: 0.12, rootMargin: '0px 0px -6% 0px' });

  var toReveal = $$('.rv, .words, [data-count], .chart');
  if (reduce) {
    toReveal.forEach(function (el) {
      el.classList.add('in');
      if (el.hasAttribute('data-count')) countUp(el);
    });
  } else {
    toReveal.forEach(function (el) { revealIO.observe(el); });
  }

  /* ---------- raça e premissas ---------- */
  var BREEDS = {
    holandes: {
      base: 6500, h: 300,
      text: '<b>Holandês PO.</b> Maior potencial de leite por lactação entre as opções. Pontos de atenção: sensibilidade maior ao calor e ao carrapato <span class="dag">†</span> e risco de F alto em rebanho fechado com poucas linhagens. A base de 6.500 L e o ganho de heterose de 300 L são premissas ilustrativas.'
    },
    gir: {
      base: 2800, h: 300,
      text: '<b>Gir leiteiro PO.</b> Rusticidade e tolerância ao calor e ao carrapato <span class="dag">†</span>, com produção por lactação menor que a do Holandês. A base de 2.800 L é premissa ilustrativa; a heterose de 300 L precisa ser conferida para esse cruzamento.'
    },
    girolando: {
      base: 4500, h: 150,
      text: '<b>Girolando (a conferir).</b> É um grupo genético formado por cruzamento Holandês x Gir, não uma raça PO pura. Se ele for a base, parte da heterose já está no animal e o cruzamento entra como ponto de partida, não como ganho extra. Confirme antes de usar a premissa de 150 L.'
    }
  };
  var breedBtns = $$('[data-breed]');
  function setBreed(key) {
    var b = BREEDS[key];
    breedBtns.forEach(function (x) { x.setAttribute('aria-pressed', x.getAttribute('data-breed') === key ? 'true' : 'false'); });
    $('#raca-texto').innerHTML = b.text;
    $('#base').value = b.base;
    $('#f1').value = b.h;
    update();
  }
  breedBtns.forEach(function (x) { x.addEventListener('click', function () { setBreed(x.getAttribute('data-breed')); }); });

  /* ---------- modelo ---------- */
  function inputs() {
    return {
      M: +$('#touros').value,
      F: +$('#matrizes').value,
      iv: +$('#ger').value,
      G: +$('#g').value,
      C: +$('#coef').value,
      H: +$('#f1').value,
      base: +$('#base').value,
      price: +$('#preco').value
    };
  }
  function model(i) {
    var Ne = 4 * i.M * i.F / (i.M + i.F);
    var dF = 1 / (2 * Ne);
    var Fy = function (y) { return 1 - Math.pow(1 - dF, y / i.iv); };       // fração, no ano y
    var f1 = i.base + i.H;
    var po = function (y) { return i.base + i.G * y - i.C * 100 * Fy(y); };  // L por lactação
    var cross = null;
    for (var y = 0; y <= 10.0001; y += 0.1) { if (po(y) >= f1) { cross = y; break; } }
    return { Ne: Ne, dF: dF, Fy: Fy, f1: f1, po: po, cross: cross };
  }

  /* ---------- simulador ---------- */
  function fmtYear(y) { return nf(y, 1); }
  function update() {
    var i = inputs(), m = model(i);
    $('#o-touros').textContent = nf(i.M);
    $('#o-matrizes').textContent = nf(i.F);
    $('#o-ger').textContent = nf(i.iv, 1) + ' anos';
    $('#o-g').textContent = nf(i.G) + ' L/ano';
    $('#o-f1').textContent = nf(i.H) + ' L';
    $('#o-base').textContent = nf(i.base) + ' L';
    $('#o-preco').textContent = 'R$ ' + nf(i.price, 2);
    $('#k-df').textContent = nf(m.dF * 100, 2) + '%';
    $('#k-f10').textContent = nf(m.Fy(10) * 100, 1) + '%';
    $('#k-f1').textContent = '+' + nf(i.H) + ' L';
    $('#k-po10').textContent = nf(m.po(10)) + ' L';
    $('#k-cross').textContent = m.cross === null ? 'não cruza' : (m.cross === 0 ? 'desde o início' : 'ano ' + fmtYear(m.cross));

    var txt = 'Com <b>' + nf(i.M) + ' touros</b> e <b>' + nf(i.F) + ' matrizes</b>, o ΔF é <b>' + nf(m.dF * 100, 2) + '%</b> por geração. ';
    if (m.cross === null) {
      txt += 'Pelas premissas, o núcleo PO não alcança o F1 em 10 anos: o ganho de seleção não compensa a endogamia com estes valores.';
    } else if (m.cross === 0) {
      txt += 'Pelas premissas, o núcleo PO já começa no nível do F1. Com este ganho de heterose, o cruzamento não tem vantagem.';
    } else {
      txt += 'Pelas premissas, a linha do núcleo PO cruza a do F1 por volta do <b>ano ' + fmtYear(m.cross) + '</b>. Antes disso, o cruzamento rende mais; depois, o núcleo acumula. Mexa nos touros, no ganho genético ou na heterose e veja o ponto se mover.';
    }
    if (m.dF > 0.01) txt += ' <span class="chip bad">ΔF acima de 1%/geração</span> Referência FAO <span class="dag">†</span>: aumente touros ou matrizes.';
    $('#read').innerHTML = txt;

    var rows = [1, 3, 5, 10].map(function (y) {
      var F = m.Fy(y) * 100, po = m.po(y), diff = po - m.f1;
      var dfYear = (m.dF * 100);
      return '<tr><td>' + y + '</td><td class="num">' + nf(m.f1) + '</td><td class="num">' + nf(po) + '</td><td class="num">' + (diff >= 0 ? '+' : '') + nf(diff) + '</td><td class="num">' + nf(F, 2) + '%</td><td class="num">' + nf(dfYear, 2) + '%</td><td class="num">' + (diff * i.price * i.F >= 0 ? '+' : '') + brl(diff * i.price * i.F) + '</td></tr>';
    }).join('');
    $('#tbl-body').innerHTML = rows;
    $('#tbl-note').textContent = 'Diferença por rebanho = (L do núcleo PO − L do F1) × preço × matrizes. Não inclui reposição de touros e matrizes F1 nem diferença de preço de venda de animais.';

    renderC1(i);
    renderC3(i, m);
    if (sticky || reduce) renderC2(reduce ? 1 : lastP); else renderC2(lastP);
  }

  $$('.ctl input, .ctl select').forEach(function (el) {
    el.addEventListener('input', update);
    el.addEventListener('change', update);
  });

  /* ---------- gráficos SVG ---------- */
  var W = 640, H = 340, PL = 86, PR = 16, PT = 16, PB = 42;
  function sx(x, x0, x1) { return PL + (x - x0) / (x1 - x0) * (W - PL - PR); }
  function sy(y, y0, y1) { return H - PB - (y - y0) / (y1 - y0) * (H - PT - PB); }
  function niceStep(range) { return range >= 500 ? 100 : (range >= 200 ? 50 : 20); }
  function axes(x0, x1, xStep, y0, y1, yStep, xl, yl, yFmt) {
    var s = '';
    for (var y = Math.ceil(y0 / yStep) * yStep; y <= y1 + 1e-9; y += yStep) {
      s += '<line class="grid-l" x1="' + PL + '" x2="' + (W - PR) + '" y1="' + sy(y, y0, y1) + '" y2="' + sy(y, y0, y1) + '"/>';
      s += '<text x="' + (PL - 8) + '" y="' + (sy(y, y0, y1) + 4) + '" text-anchor="end">' + yFmt(y) + '</text>';
    }
    for (var x = x0; x <= x1 + 1e-9; x += xStep) {
      s += '<text x="' + sx(x, x0, x1) + '" y="' + (H - PB + 18) + '" text-anchor="middle">' + nf(x) + '</text>';
    }
    s += '<line class="ax" x1="' + PL + '" x2="' + PL + '" y1="' + PT + '" y2="' + (H - PB) + '"/>';
    s += '<line class="ax" x1="' + PL + '" x2="' + (W - PR) + '" y1="' + (H - PB) + '" y2="' + (H - PB) + '"/>';
    s += '<text class="lbl" x="' + ((PL + W - PR) / 2) + '" y="' + (H - 4) + '" text-anchor="middle">' + xl + '</text>';
    s += '<text class="lbl" transform="translate(16,' + ((PT + H - PB) / 2) + ') rotate(-90)" text-anchor="middle">' + yl + '</text>';
    return s;
  }
  function path(pts, x0, x1, y0, y1, extra) {
    var d = pts.map(function (p, k) { return (k ? 'L' : 'M') + sx(p[0], x0, x1).toFixed(1) + ' ' + sy(p[1], y0, y1).toFixed(1); }).join(' ');
    return '<path pathLength="1" d="' + d + '" ' + (extra || '') + '/>';
  }

  /* gráfico 1: F por geração, 3 cenários de touros */
  function renderC1(i) {
    var gens = [], x0 = 0, x1 = 10;
    for (var g = 0; g <= 10; g += 0.5) gens.push(g);
    var scen = [[5, 'clay'], [20, 'gold'], [60, 'moss']];
    var series = scen.map(function (s) {
      var Ne = 4 * s[0] * i.F / (s[0] + i.F), dF = 1 / (2 * Ne);
      return { M: s[0], cls: s[1], pts: gens.map(function (t) { return [t, 100 * (1 - Math.pow(1 - dF, t))]; }) };
    });
    var lim = gens.map(function (t) { return [t, 100 * (1 - Math.pow(0.99, t))]; });
    var ymax = Math.max(lim[lim.length - 1][1], Math.max.apply(null, series.map(function (s) { return s.pts[s.pts.length - 1][1]; })));
    var y1 = Math.max(5, Math.ceil(ymax / 5) * 5), y0 = 0;
    var s = axes(x0, x1, 1, y0, y1, 5, 'Gerações', 'F do rebanho (%)', function (v) { return nf(v) + '%'; });
    s += path(lim, x0, x1, y0, y1, 'class="ln ink dash"');
    series.forEach(function (sr) { s += path(sr.pts, x0, x1, y0, y1, 'class="ln ' + sr.cls + '"'); });
    $('#c1').innerHTML = s;
  }

  /* gráfico 3: custo da endogamia por ano (R$ por rebanho) */
  function renderC3(i, m) {
    var years = []; for (var y = 1; y <= 10; y++) years.push(y);
    var vals = years.map(function (y) { return i.C * 100 * m.Fy(y) * i.price * i.F; });
    var vmax = Math.max.apply(null, vals) * 1.12 || 1;
    var n = years.length, bw = (W - PL - PR) / n;
    var s = '';
    for (var k = 0; k <= 4; k++) {
      var v = vmax * k / 4, yy = H - PB - (H - PT - PB) * k / 4;
      s += '<line class="grid-l" x1="' + PL + '" x2="' + (W - PR) + '" y1="' + yy + '" y2="' + yy + '"/>';
      s += '<text x="' + (PL - 8) + '" y="' + (yy + 4) + '" text-anchor="end">' + brl(v) + '</text>';
    }
    years.forEach(function (yr, k) {
      var h = (H - PT - PB) * vals[k] / vmax, x = PL + k * bw + bw * 0.18;
      s += '<rect class="bar-r" x="' + x.toFixed(1) + '" y="' + (H - PB - h).toFixed(1) + '" width="' + (bw * 0.64).toFixed(1) + '" height="' + h.toFixed(1) + '" fill="#efb04a" opacity=".85"/>';
      s += '<text x="' + (PL + k * bw + bw / 2) + '" y="' + (H - PB + 18) + '" text-anchor="middle">' + yr + '</text>';
    });
    s += '<line class="ax" x1="' + PL + '" x2="' + PL + '" y1="' + PT + '" y2="' + (H - PB) + '"/>';
    s += '<line class="ax" x1="' + PL + '" x2="' + (W - PR) + '" y1="' + (H - PB) + '" y2="' + (H - PB) + '"/>';
    s += '<text class="lbl" x="' + ((PL + W - PR) / 2) + '" y="' + (H - 4) + '" text-anchor="middle">Ano</text>';
    $('#c3').innerHTML = s;
    var perCow = i.C * 100 * m.Fy(10);
    $('#c3-cap').innerHTML = 'No ano 10: <b>' + nf(perCow, 1) + ' L</b> por vaca na lactação, <b>' + brl(perCow * i.price) + '</b> por vaca e <b>' + brl(perCow * i.price * i.F) + '</b> por ano no rebanho de ' + nf(i.F) + ' matrizes.';
  }

  /* gráfico 2: leite por vaca, anos 0 a 10 (linha de F1 e núcleo PO), desenhado por rolagem */
  var lastP = 0;
  function renderC2(p) {
    lastP = p;
    var i = inputs(), m = model(i);
    var year = Math.max(0, Math.min(1, p)) * 10;
    var pts = [], pf = [];
    for (var y = 0; y <= 10.0001; y += 0.25) { pts.push([y, m.po(y)]); pf.push([y, m.f1]); }
    var all = pts.map(function (q) { return q[1]; }).concat([m.f1, i.base]);
    var ymin = Math.min.apply(null, all), ymax = Math.max.apply(null, all);
    var span = Math.max(1, ymax - ymin);
    var step = niceStep(span);
    var y0 = Math.floor((ymin - span * 0.05) / step) * step, y1 = Math.ceil((ymax + span * 0.05) / step) * step;
    var s = axes(0, 10, 1, y0, y1, step, 'Anos', 'L por lactação', function (v) { return nf(v); });
    var dash = 'stroke-dasharray="1" stroke-dashoffset="' + (1 - Math.max(0.0001, Math.min(1, p))).toFixed(4) + '"';
    s += path(pf, 0, 10, y0, y1, 'class="ln clay" ' + dash);
    s += path(pts, 0, 10, y0, y1, 'class="ln moss" ' + dash);
    if (m.cross !== null && m.cross > 0 && year >= m.cross) {
      s += '<line class="ax" x1="' + sx(m.cross, 0, 10) + '" x2="' + sx(m.cross, 0, 10) + '" y1="' + PT + '" y2="' + (H - PB) + '" stroke-dasharray="4 4" stroke="#efb04a"/>';
      s += '<text x="' + (sx(m.cross, 0, 10) + 6) + '" y="' + (PT + 14) + '" fill="#efb04a">cruzamento: ano ' + fmtYear(m.cross) + '</text>';
    }
    s += '<circle cx="' + sx(year, 0, 10) + '" cy="' + sy(m.po(year), y0, y1) + '" r="5" fill="#8fb56a"/>';
    s += '<circle cx="' + sx(year, 0, 10) + '" cy="' + sy(m.f1, y0, y1) + '" r="5" fill="#d4703c"/>';
    $('#c2').innerHTML = s;
    $('#c2-year').innerHTML = 'Ano <b>' + fmtYear(year) + '</b> · núcleo PO <b>' + nf(m.po(year)) + ' L</b> · F1 <b>' + nf(m.f1) + ' L</b>';
  }

  /* linha do tempo do gráfico 2 com a rolagem */
  var track = $('#c2-track');
  var sticky = !reduce && !!track;
  var stickyPrev = -1;
  function stickyTick() {
    var r = track.getBoundingClientRect();
    var total = track.offsetHeight - innerHeight;
    var p = total > 0 ? Math.min(1, Math.max(0, -r.top / total)) : 1;
    if (Math.abs(p - stickyPrev) > 0.002) { stickyPrev = p; renderC2(p); }
  }

  /* ---------- diagnóstico ---------- */
  var form = $('#diag-form');
  var result = $('#result');
  var lastText = '';
  var OBJ = { leite: 'Leite a custo baixo (núcleo PO como programa principal)', reprodutores: 'Vender reprodutores PO registrados', comercial: 'Leite comercial no curto prazo' };
  var GEN = { completa: 'completa', parcial: 'parcial', nenhuma: 'não há' };
  var SIM = { sim: 'sim', parcial: 'parcial', nao: 'não' };

  function minSires(F, neMin) {
    if (4 * F <= neMin) return null;
    return Math.ceil(neMin * F / (4 * F - neMin));
  }

  function runDiag() {
    var d = new FormData(form);
    var F = parseFloat(String(d.get('vacas')).replace(',', '.'));
    var M = parseFloat(String(d.get('touros')).replace(',', '.'));
    if (!(F >= 1) || !(M >= 1)) {
      result.innerHTML = '<div class="panelbox"><h3>Confira os números</h3><p class="muted">Informe pelo menos 1 vaca e 1 touro em uso para calcular.</p></div>';
      return;
    }
    var obj = String(d.get('objetivo')), gen = String(d.get('genealogia')), geno = String(d.get('genotipagem')), ctrl = String(d.get('controle'));
    var fm = String(d.get('fmedio') || '').trim();
    var Ne = 4 * M * F / (M + F), dF = 1 / (2 * Ne);
    var Fg = [1, 2, 3, 4, 5].map(function (t) { return 100 * (1 - Math.pow(1 - dF, t)); });
    var needM = minSires(F, 50);
    var alerts = [], missing = [];

    var strat;
    if (dF > 0.01) {
      strat = 'Antes de escolher o caminho, ajuste a estrutura de reprodução: o ΔF está acima da referência de 1% por geração (FAO <span class="dag">†</span>).';
      if (needM === null) alerts.push('Com ' + nf(F) + ' vacas, nenhum número de touros leva o ΔF a 1% por geração. É preciso mais fêmeas reprodutoras.');
      else alerts.push('Para ΔF de até 1% por geração com ' + nf(F) + ' vacas, use pelo menos <b>' + nf(needM) + ' touros</b>.');
    } else {
      strat = 'Com esta estrutura, o ΔF por geração fica dentro de 1% (referência FAO <span class="dag">†</span>). O caminho depende do objetivo.';
    }
    if (obj === 'leite') strat += ' Para leite a custo baixo, o indicado é um núcleo PO com consanguinidade planejada, cruzamento só em lote comercial aprovado pelo zootecnista.';
    if (obj === 'reprodutores') strat += ' Para vender reprodutores registrados, o núcleo PO é o programa principal: genealogia e registro são prioridade.';
    if (obj === 'comercial') strat += ' Para leite comercial de curto prazo, o cruzamento tende a render mais já no primeiro ciclo. Mantenha um núcleo PO se houver interesse em venda de genética.';

    if (gen === 'nenhuma') alerts.push('Sem genealogia não dá para estimar o F real. A conta acima usa só o número de animais.');
    if (gen === 'parcial') alerts.push('Genealogia parcial: o F estimado pode estar abaixo do real por causa de ancestrais desconhecidos.');
    if (geno !== 'sim') alerts.push('Sem genotipagem, o parentesco é estimado pelo pedigree. Pode haver diferença em relação ao parentesco medido no DNA <span class="dag">†</span>.');
    if (ctrl !== 'sim') alerts.push('Sem controle leiteiro completo, o ganho de produção não tem como ser medido. O simulador usa premissas.');
    if (fm !== '') alerts.push('F médio informado: ' + nf(parseFloat(fm.replace(',', '.')), 1) + '%. Compare com a meta de 1% por geração.');

    if (gen !== 'completa') missing.push('Genealogia completa (pai e mãe) dos animais em uso');
    if (geno !== 'sim') missing.push('Genotipagem, por amostragem se o orçamento for limitado');
    if (ctrl !== 'sim') missing.push('Controle leiteiro por vaca e por lactação');
    if (fm === '') missing.push('F médio do rebanho calculado pela genealogia');
    missing.push('Custo real de reposição e preço do leite recebido pela fazenda');

    var chip = dF <= 0.01 ? '<span class="chip ok">ΔF dentro da meta</span>' : '<span class="chip bad">ΔF acima da meta</span>';

    var rows = Fg.map(function (v, k) { return '<tr><td>' + (k + 1) + ' geração' + (k ? 'ões' : '') + '</td><td class="num">' + nf(v, 2) + '%</td></tr>'; }).join('');
    var html = '<div class="panelbox"><div style="margin-bottom:.4rem">' + chip + '</div><h3>Estratégia indicada</h3><p>' + strat + '</p><p class="small muted">Objetivo: ' + OBJ[obj] + '.</p></div>' +
      '<div class="kpis">' +
      '<div class="kpi k-gold"><b>' + nf(dF * 100, 2) + '%</b><span>ΔF por geração</span></div>' +
      '<div class="kpi k-ink"><b>' + nf(Ne, 1) + '</b><span>tamanho efetivo (Ne)</span></div>' +
      '<div class="kpi ' + (needM === null ? 'k-clay' : 'k-moss') + '"><b>' + (needM === null ? '–' : nf(needM)) + '</b><span>touros mínimos para ΔF ≤ 1%</span></div>' +
      '</div>' +
      '<div class="panelbox"><h3>F estimado nas próximas gerações</h3><div class="tablewrap" style="margin:.6rem 0 0"><table><thead><tr><th>Horizonte</th><th class="num">F acumulado</th></tr></thead><tbody>' + rows + '</tbody></table></div><p class="small muted" style="margin:.6rem 0 0">Assume ΔF constante e a mesma estrutura de reprodução em todas as gerações.</p></div>' +
      '<div class="panelbox"><h3>Alertas</h3>' + (alerts.length ? '<ul>' + alerts.map(function (a) { return '<li>' + a + '</li>'; }).join('') + '</ul>' : '<p class="muted">Nenhum alerta com os dados informados.</p>') + '</div>' +
      '<div class="panelbox"><h3>O que falta coletar</h3><ul>' + missing.map(function (a) { return '<li>' + a + '</li>'; }).join('') + '</ul></div>' +
      '<div class="actions"><button class="btn ghost small" type="button" data-act="copy">Copiar</button><button class="btn ghost small" type="button" data-act="baixar">Baixar .txt</button><button class="btn ghost small" type="button" data-act="imprimir">Imprimir</button></div>' +
      '<p class="small muted">Triagem orientativa por regras. Não substitui o zootecnista nem o geneticista. O resultado fica só nesta tela.</p>';
    result.innerHTML = html;

    var plain = 'Diagnóstico Berdinazi & Mezenga (triagem orientativa)\n' +
      'Vacas: ' + nf(F) + ' | Touros: ' + nf(M) + ' | Objetivo: ' + OBJ[obj] + '\n' +
      'ΔF por geração: ' + nf(dF * 100, 2) + '% | Ne: ' + nf(Ne, 1) + '\n' +
      'F acumulado (1 a 5 gerações): ' + Fg.map(function (v) { return nf(v, 2) + '%'; }).join(', ') + '\n' +
      'Estratégia: ' + strat.replace(/<[^>]+>/g, '') + '\n' +
      'Alertas: ' + (alerts.length ? alerts.map(function (a) { return a.replace(/<[^>]+>/g, ''); }).join(' | ') : 'nenhum') + '\n' +
      'Falta coletar: ' + missing.join('; ') + '\n';
    lastText = plain;
    result.scrollIntoView({ behavior: reduce ? 'auto' : 'smooth', block: 'start' });
  }

  form.addEventListener('submit', function (e) { e.preventDefault(); runDiag(); });
  $('#b-example').addEventListener('click', function () {
    form.elements.vacas.value = '120';
    form.elements.touros.value = '6';
    form.elements.genealogia.value = 'parcial';
    form.elements.genotipagem.value = 'nao';
    form.elements.controle.value = 'parcial';
    form.elements.fmedio.value = '';
    runDiag();
  });
  result.addEventListener('click', function (e) {
    var b = e.target.closest('[data-act]');
    if (!b || !lastText) return;
    var act = b.getAttribute('data-act');
    if (act === 'imprimir') { window.print(); return; }
    if (act === 'baixar') {
      var blob = new Blob([lastText], { type: 'text/plain;charset=utf-8' });
      var a = document.createElement('a');
      a.href = URL.createObjectURL(blob);
      a.download = 'diagnostico-berdinazi-mezenga.txt';
      document.body.appendChild(a); a.click(); a.remove();
      setTimeout(function () { URL.revokeObjectURL(a.href); }, 1000);
      return;
    }
    if (act === 'copy') {
      var done = function () { b.textContent = 'Copiado'; setTimeout(function () { b.textContent = 'Copiar'; }, 1500); };
      if (navigator.clipboard) navigator.clipboard.writeText(lastText).then(done, function () {});
    }
  });

  /* ---------- inicialização ---------- */
  setBreed('holandes');
  onScroll();
  renderC2(0);
  if (sticky) stickyTick();
})();
