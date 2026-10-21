/* ===== Shorin Ryu Karate Do India — main.js ===== */

// ─── Mobile Menu ─────────────────────────────────────────────────────────────
function toggleMenu() {
  const menu = document.getElementById('mobile-menu');
  if (menu) menu.classList.toggle('open');
}

// Close mobile menu when any link inside is clicked
document.addEventListener('DOMContentLoaded', function () {
  const mobileLinks = document.querySelectorAll('.mobile-menu a');
  mobileLinks.forEach(link => {
    link.addEventListener('click', function () {
      const menu = document.getElementById('mobile-menu');
      if (menu) menu.classList.remove('open');
    });
  });
});

// ─── About Page Tabs ─────────────────────────────────────────────────────────
function showTab(id, btn) {
  document.querySelectorAll('.tab-content').forEach(t => t.classList.remove('active'));
  document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
  const tab = document.getElementById('tab-' + id);
  if (tab) tab.classList.add('active');
  if (btn) btn.classList.add('active');
}

// ─── Scroll Reveal ───────────────────────────────────────────────────────────
function initReveal() {
  const reveals = document.querySelectorAll('.reveal');
  if (!reveals.length) return;

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(e => {
      if (e.isIntersecting) {
        e.target.classList.add('visible');
        observer.unobserve(e.target);
      }
    });
  }, { threshold: 0.1, rootMargin: '0px 0px -40px 0px' });

  reveals.forEach(r => observer.observe(r));
}

// ─── Navbar Shadow on Scroll ─────────────────────────────────────────────────
window.addEventListener('scroll', function () {
  const nav = document.getElementById('navbar');
  if (!nav) return;
  nav.style.boxShadow = window.scrollY > 50
    ? '0 4px 30px rgba(0,0,0,0.5)'
    : 'none';
});

// ─── Auto-dismiss Django messages ────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', function () {
  const msgs = document.querySelectorAll('.django-msg');
  msgs.forEach(msg => {
    setTimeout(() => {
      msg.style.opacity = '0';
      msg.style.transform = 'translateY(-10px)';
      setTimeout(() => msg.remove(), 400);
    }, 5000);
  });
});

// ─── Init on load ────────────────────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', initReveal);
