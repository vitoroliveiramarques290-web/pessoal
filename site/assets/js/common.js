(function () {
  var header = document.querySelector('.site-header');
  var toggle = document.querySelector('.nav-toggle');
  if (toggle) {
    toggle.addEventListener('click', function () {
      var open = document.body.classList.toggle('nav-open');
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
    document.querySelectorAll('.nav a').forEach(function (a) {
      a.addEventListener('click', function () { document.body.classList.remove('nav-open'); toggle.setAttribute('aria-expanded', 'false'); });
    });
  }
  function onScroll() { if (header) header.classList.toggle('solid', window.scrollY > 24); }
  addEventListener('scroll', onScroll, { passive: true });
  onScroll();
  var here = location.pathname.split('/').pop() || 'index.html';
  document.querySelectorAll('.nav a').forEach(function (a) {
    var h = a.getAttribute('href');
    if (h === here || (here === '' && h === 'index.html')) a.setAttribute('aria-current', 'page');
  });
})();
