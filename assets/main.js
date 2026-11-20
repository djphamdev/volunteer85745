// Volunteer 85745 - Interactive Features (Clean - No PII)
(function() {
  'use strict';

  // ===== Theme Toggle (dark default) =====
  const THEME_KEY = 'volunteer-theme';

  function getTheme() {
    return localStorage.getItem(THEME_KEY) || 'dark';
  }

  function setTheme(theme) {
    if (theme === 'light') {
      document.documentElement.setAttribute('data-theme', 'light');
    } else {
      document.documentElement.removeAttribute('data-theme');
    }
    localStorage.setItem(THEME_KEY, theme);
    const btn = document.getElementById('themeToggle');
    if (btn) btn.textContent = theme === 'dark' ? '☀️ Light' : '🌙 Dark';
  }

  function setBtnFromTheme(theme) {
    const btn = document.getElementById('themeToggle');
    if (btn) btn.textContent = theme === 'dark' ? '☀️ Light' : '🌙 Dark';
  }

  // Apply on load (before render)
  setTheme(getTheme());
  setBtnFromTheme(getTheme());

  document.addEventListener('DOMContentLoaded', function() {
    const btn = document.getElementById('themeToggle');
    if (btn) {
      btn.addEventListener('click', function() {
        const next = getTheme() === 'dark' ? 'light' : 'dark';
        setTheme(next);
      });
    }
  });

  // ===== Back to Top Button =====
  document.addEventListener('DOMContentLoaded', function() {
    const btn = document.getElementById('backToTop');
    if (!btn) return;

    let ticking = false;

    function updateBtn() {
      if (window.scrollY > 300) {
        btn.classList.add('visible');
      } else {
        btn.classList.remove('visible');
      }
      ticking = false;
    }

    window.addEventListener('scroll', function() {
      if (!ticking) {
        window.requestAnimationFrame(updateBtn);
        ticking = true;
      }
    }, { passive: true });

    btn.addEventListener('click', function() {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
  });

  // ===== Filters (category + hours + search) =====
  document.addEventListener('DOMContentLoaded', function() {
    const catFilter = document.getElementById('catFilter');
    const hoursFilter = document.getElementById('hoursFilter');
    const searchInput = document.getElementById('searchFilter');
    if (!catFilter && !hoursFilter && !searchInput) return;

    const cards = Array.from(document.querySelectorAll('.lead-card'));

    function applyFilters() {
      const catVal = catFilter ? catFilter.value : 'all';
      const hoursVal = hoursFilter ? hoursFilter.value : '0';
      const searchTerm = (searchInput ? searchInput.value : '').toLowerCase();

      cards.forEach(function(card) {
        const category = card.getAttribute('data-category') || 'remote';
        const hours = parseInt(card.getAttribute('data-hours') || '0', 10);
        const text = (card.textContent || '').toLowerCase();

        // Category filter
        let categoryMatch = true;
        if (catVal === 'remote') categoryMatch = category === 'remote';
        else if (catVal === 'local') categoryMatch = category === 'local';

        // Hours filter
        let hoursMatch = true;
        if (hoursVal === '20') hoursMatch = hours >= 20;
        else if (hoursVal === '10') hoursMatch = hours >= 10;
        else if (hoursVal === '5') hoursMatch = hours >= 5;

        const searchMatch = !searchTerm || text.includes(searchTerm);

        if (categoryMatch && hoursMatch && searchMatch) {
          card.style.display = '';
        } else {
          card.style.display = 'none';
        }
      });
    }

    if (catFilter) catFilter.addEventListener('change', applyFilters);
    if (hoursFilter) hoursFilter.addEventListener('change', applyFilters);
    if (searchInput) {
      let timer;
      searchInput.addEventListener('input', function() {
        clearTimeout(timer);
        timer = setTimeout(applyFilters, 200);
      });
    }
  });
})();
