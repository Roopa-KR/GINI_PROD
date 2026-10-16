(() => {
  'use strict';
  const menu = document.getElementById('mobileMenu');
  const nav = document.getElementById('sideNav');
  const shade = document.getElementById('mobileShade');
  function close() { if (nav) nav.classList.remove('open'); if (shade) shade.hidden = true; }
  if (menu && nav && shade) {
    menu.addEventListener('click', () => { nav.classList.toggle('open'); shade.hidden = !nav.classList.contains('open'); });
    shade.addEventListener('click', close);
    window.addEventListener('keydown', ev => { if (ev.key === 'Escape') close(); });
  }
  const answer = document.getElementById('answer');
  const evidence = document.getElementById('evidence');
  if (answer && evidence && answer.tagName === 'SELECT') {
    const update = () => {
      const required = (answer.value === 'Yes' && evidence.dataset.requiredYes === 'true') ||
                       (answer.value === 'No' && evidence.dataset.requiredNo === 'true');
      evidence.required = required;
    };
    answer.addEventListener('change', update); update();
  }
})();
