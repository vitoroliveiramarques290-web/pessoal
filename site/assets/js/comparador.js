(function () {
  var $ = function (id) { return document.getElementById(id); };
  if (!$('svg')) return;
  var nf = function (x, d) { return x.toFixed(d).replace('.', ','); };
  var ids = ['touros', 'matrizes', 'ger', 'g', 'coef', 'f1', 'preco'];
  var YEARS = 30;

  function val() {
    return { m: +$('touros').value, f: +$('matrizes').value, L: +$('ger').value, g: +$('g').value, c: +$('coef').value, x: +$('f1').value, p: +$('preco').value };
  }
  function Ft(v, t) {
    var ne = 4 * v.m * v.f / (v.m + v.f), df = 1 / (2 * ne);
    return { df: df, F: 1 - Math.pow(1 - df, t / v.L) };
  }
  function net(v, t) { return v.g * t - v.c * Ft(v, t).F * 100; }

  function draw() {
    var v = val();
    $('o-touros').textContent = v.m; $('o-matrizes').textContent = v.f;
    $('o-ger').textContent = nf(v.L, 1) + ' anos'; $('o-g').textContent = nf(v.g, 1) + ' kg/ano'; $('o-preco').textContent = 'R$ ' + nf(v.p, 2);
    var a = Ft(v, 10);
    $('k-df').textContent = nf(a.df * 100, 2) + '%';
    $('k-f10').textContent = nf(a.F * 100, 1) + '%';
    $('k-f1').textContent = '+' + nf(v.x, 1) + ' kg';
    $('k-sel').textContent = nf(net(v, 10), 1) + ' kg';

    var W = 640, H = 340, L = 58, R = 16, T = 34, B = 44;
    var maxY = Math.max(v.x * 1.15, net(v, YEARS) * 1.1, 10), minY = Math.min(0, net(v, 3) - 1);
    var X = function (t) { return L + (W - L - R) * t / YEARS; };
    var Y = function (k) { return T + (H - T - B) * (1 - (k - minY) / (maxY - minY)); };
    var s = '', step = maxY > 60 ? 20 : maxY > 30 ? 10 : 5;
    for (var k = Math.ceil(minY / step) * step; k <= maxY; k += step) {
      s += '<line x1="' + L + '" x2="' + (W - R) + '" y1="' + Y(k) + '" y2="' + Y(k) + '" stroke="rgba(247,237,219,.12)"/><text x="' + (L - 8) + '" y="' + (Y(k) + 5) + '" fill="#a99d85" font-size="16" text-anchor="end">' + k + '</text>';
    }
    for (var t = 0; t <= YEARS; t += 5) s += '<text x="' + X(t) + '" y="' + (H - 20) + '" fill="#a99d85" font-size="16" text-anchor="middle">' + t + '</text>';
    s += '<text x="' + (W / 2) + '" y="' + (H - 2) + '" fill="#a99d85" font-size="14" text-anchor="middle">anos</text>';
    s += '<text x="' + L + '" y="16" fill="#a99d85" font-size="14">kg por bezerro</text>';
    s += '<line x1="' + X(0) + '" x2="' + X(YEARS) + '" y1="' + Y(v.x) + '" y2="' + Y(v.x) + '" stroke="#d4703c" stroke-width="2.5"/>';
    var pn = '', pc = '';
    for (var i = 0; i <= YEARS; i++) {
      pn += (i ? 'L' : 'M') + X(i) + ' ' + Y(net(v, i));
      pc += (i ? 'L' : 'M') + X(i) + ' ' + Y(v.c * Ft(v, i).F * 100);
    }
    s += '<path d="' + pc + '" fill="none" stroke="#efb04a" stroke-width="2" stroke-dasharray="5 4"/>';
    s += '<path d="' + pn + '" fill="none" stroke="#8fb56a" stroke-width="2.5"/>';
    var cross = null;
    for (var j = 1; j <= YEARS; j++) { if (net(v, j) >= v.x) { cross = j; break; } }
    if (cross) s += '<circle cx="' + X(cross) + '" cy="' + Y(v.x) + '" r="5" fill="#14110a" stroke="#f7eddb" stroke-width="2"/>';
    $('svg').innerHTML = s;

    var cost10 = v.c * a.F * 100;
    var msg = cross
      ? 'Com estes valores, o núcleo selecionado alcança o ganho do F1 em <b>' + cross + ' anos</b>. Até lá, <b>o cruzamento rende mais quilos por bezerro</b>. A partir daí o ganho do núcleo continua crescendo e o do F1 não.'
      : 'Com estes valores, o núcleo <b>não alcança o ganho do F1 em ' + YEARS + ' anos</b>. Só em quilos de desmame, <b>o cruzamento vence</b>. O argumento da consanguinidade passa a ser o objetivo da cliente (manter o Fumaça), a adaptação e a permanência do ganho.';
    msg += ' O custo da endogamia em 10 anos é de ' + nf(cost10, 1) + ' kg por bezerro (R$ ' + nf(cost10 * v.p, 0) + ').' + (v.m < 10 ? ' <b>Com poucos touros, F sobe rápido: aumente o número de reprodutores.</b>' : '');
    $('read').innerHTML = msg;
  }
  ids.forEach(function (i) { $(i).addEventListener('input', draw); });
  draw();

  function gam(g) { return g === 'AA' ? ['A', 'A'] : g === 'Aa' ? ['A', 'a'] : ['a', 'a']; }
  function mend() {
    var m = gam($('mae').value), p = gam($('pai').value), c = { AA: 0, Aa: 0, aa: 0 };
    m.forEach(function (x) { p.forEach(function (y) { c[(x === 'A' && y === 'A') ? 'AA' : (x === 'a' && y === 'a') ? 'aa' : 'Aa'] += 25; }); });
    var h = '';
    [['AA', 'AA'], ['Aa', 'Aa'], ['aa', 'aa (Fumaça)']].forEach(function (r) {
      h += '<div class="bar"><span>' + r[0] + '</span><div><i style="width:' + c[r[0]] + '%"></i></div><span>' + c[r[0]] + '%</span></div>';
    });
    $('bars').innerHTML = h;
    $('gen-note').textContent = c.aa === 100 ? 'aa x aa gera 100% de aa. Dois animais aa não precisam ser parentes para isso.' : c.aa === 0 ? 'Nenhuma cria Fumaça nesta combinação. É o que acontece ao cruzar com outra raça ou com animal convencional (AA).' : 'Probabilidade de ' + c.aa + '% de cria Fumaça nesta combinação.';
  }
  $('mae').addEventListener('input', mend); $('pai').addEventListener('input', mend); mend();
})();
