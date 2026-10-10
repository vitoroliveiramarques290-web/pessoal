(function () {
  var tabs = [].slice.call(document.querySelectorAll('[role=tab]'));
  if (!tabs.length) return;
  function show(id) {
    tabs.forEach(function (t) {
      var on = t.getAttribute('aria-controls') === id;
      t.setAttribute('aria-selected', on ? 'true' : 'false');
      t.tabIndex = on ? 0 : -1;
    });
    document.querySelectorAll('[role=tabpanel]').forEach(function (p) { p.hidden = p.id !== id; });
  }
  tabs.forEach(function (t, i) {
    t.addEventListener('click', function () { show(t.getAttribute('aria-controls')); });
    t.addEventListener('keydown', function (e) {
      if (e.key === 'ArrowRight' || e.key === 'ArrowLeft') {
        var n = tabs[(i + (e.key === 'ArrowRight' ? 1 : tabs.length - 1)) % tabs.length];
        n.focus(); show(n.getAttribute('aria-controls'));
      }
    });
  });
  show(tabs[0].getAttribute('aria-controls'));

  var f = document.getElementById('filtro');
  if (f) f.addEventListener('input', function () {
    var q = f.value.toLowerCase();
    document.querySelectorAll('#inv tbody tr').forEach(function (r) { r.hidden = q && r.textContent.toLowerCase().indexOf(q) < 0; });
  });
})();
