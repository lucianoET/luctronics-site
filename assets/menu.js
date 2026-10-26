// Menu mobile (painel fixo abaixo da nav); fecha ao tocar num link ou com Esc
const btn = document.getElementById('menu-btn');
const panel = document.getElementById('mobile-menu');
if (btn && panel) {
  const set = open => {
    panel.classList.toggle('open', open);
    btn.setAttribute('aria-expanded', open ? 'true' : 'false');
    btn.setAttribute('aria-label', open ? 'Fechar menu' : 'Abrir menu');
  };
  btn.addEventListener('click', () => set(!panel.classList.contains('open')));
  panel.querySelectorAll('a').forEach(a => a.addEventListener('click', () => set(false)));
  document.addEventListener('keydown', e => { if (e.key === 'Escape') set(false); });
}
