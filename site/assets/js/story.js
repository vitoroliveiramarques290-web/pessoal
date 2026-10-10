(function () {
  var track = document.getElementById('story-track');
  if (!track) return;
  var reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  var layers = [].slice.call(track.querySelectorAll('.layer'));
  var chapters = [].slice.call(track.querySelectorAll('.chapter'));
  var N = chapters.length;
  var dotsBox = track.querySelector('.dots');
  var narrow = function () { return innerWidth <= innerHeight; };

  // layer: 0 aéreo, 1 nível do olho, 2 sede, 3 curral, 4 rosto
  var CH = [
    { l: 0, s: 1.00, o: [52, 46] },
    { l: 1, s: 1.00, o: [58, 44] },
    { l: 4, s: 1.05, o: [40, 45] },
    { l: 2, s: 1.00, o: [68, 54] },
    { l: 3, s: 1.35, o: [54, 100] }
  ];
  var END_WIDE = { l: 3, s: 1.30, o: [0, 45] };
  var END_NARROW = CH[4];

  function step() { return innerHeight * 1.1; }
  function top() { return track.getBoundingClientRect().top + scrollY; }
  var btns = chapters.map(function (_, i) {
    var b = document.createElement('button');
    b.type = 'button';
    b.setAttribute('aria-label', 'Capítulo ' + (i + 1));
    b.addEventListener('click', function () { scrollTo({ top: top() + i * step(), behavior: reduce ? 'auto' : 'smooth' }); });
    if (dotsBox) dotsBox.appendChild(b);
    return b;
  });

  var ease = function (t) { return t * t * (3 - 2 * t); };
  var lerp = function (a, b, t) { return a + (b - a) * t; };
  var clamp = function (x, a, b) { return Math.max(a, Math.min(b, x)); };
  var target = 0, c = 0, last = performance.now();

  function read() { target = clamp(-track.getBoundingClientRect().top / step(), 0, N - 1); }
  addEventListener('scroll', read, { passive: true });
  addEventListener('resize', read);
  read(); c = target;

  function draw() {
    CH[4] = narrow() ? END_NARROW : END_WIDE;
    var a = Math.min(Math.floor(c), N - 2), b = a + 1, f = ease(c - a);
    var A = CH[a], B = CH[b];
    layers.forEach(function (el, l) {
      var inA = A.l === l, inB = B.l === l, op, s, ox, oy, blur = 0;
      if (inA && inB) { op = 1; s = lerp(A.s, B.s, f); ox = lerp(A.o[0], B.o[0], f); oy = lerp(A.o[1], B.o[1], f); }
      else if (inA) { op = 1 - f; s = A.s * (1 + 0.07 * f); ox = A.o[0]; oy = A.o[1]; blur = 7 * f; }
      else if (inB) { op = f; s = B.s * (0.93 + 0.07 * f); ox = B.o[0]; oy = B.o[1]; blur = 7 * (1 - f); }
      else { el.style.opacity = 0; return; }
      var drift = 1 + 0.03 * (c - (inA ? a : b));
      el.style.opacity = op.toFixed(3);
      el.style.transformOrigin = ox.toFixed(1) + '% ' + oy.toFixed(1) + '%';
      el.style.transform = 'scale(' + (s * drift).toFixed(4) + ')';
      el.style.filter = blur > 0.05 ? 'blur(' + blur.toFixed(1) + 'px)' : 'none';
    });
    chapters.forEach(function (el, k) {
      var t = clamp(1 - Math.abs(c - k) * 2.6, 0, 1);
      el.style.opacity = t.toFixed(3);
      el.style.transform = 'translateY(' + ((c - k) * -26).toFixed(1) + 'px)';
      el.style.pointerEvents = t > 0.6 ? 'auto' : 'none';
      el.style.visibility = t < 0.01 ? 'hidden' : 'visible';
    });
    var on = Math.round(c);
    btns.forEach(function (bt, i) { bt.classList.toggle('on', i === on); });
  }

  function frame(now) {
    var dt = Math.min((now - last) / 1000, 1 / 30);
    last = now;
    var r = track.getBoundingClientRect();
    if (r.bottom > -50 && r.top < innerHeight + 50) {
      c = reduce ? target : c + (target - c) * (1 - Math.exp(-6 * dt));
      draw();
    }
    requestAnimationFrame(frame);
  }
  requestAnimationFrame(frame);
})();
