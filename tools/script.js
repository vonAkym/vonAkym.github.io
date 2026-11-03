(function () {
  try {
    document.querySelectorAll('.card').forEach(function (c) {
      c.addEventListener('click', function () {
        c.setAttribute('aria-pressed', c.getAttribute('aria-pressed') === 'true' ? 'false' : 'true');
      });
    });
  } catch (e) {}
  try {
    var box = document.getElementById('lightbox');
    var big = box.querySelector('img');
    document.querySelectorAll('.zoom').forEach(function (b) {
      b.addEventListener('click', function () {
        var img = b.querySelector('img');
        big.src = img.src;
        big.alt = img.alt;
        if (box.showModal) { box.showModal(); }
      });
    });
    box.querySelector('.close').addEventListener('click', function () { box.close(); });
    box.addEventListener('click', function (e) { if (e.target === box) { box.close(); } });
  } catch (e) {}
})();
