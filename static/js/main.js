document.addEventListener('DOMContentLoaded', () => {
    // Theme Engine Logic
    const body = document.body;
    const themeToggle = document.getElementById('theme-toggle');
    const currentTheme = localStorage.getItem('theme');

    if (currentTheme === 'light') {
        body.classList.add('light-mode');
    }

    if (themeToggle) {
        themeToggle.addEventListener('click', () => {
            body.classList.toggle('light-mode');
            let theme = 'dark';
            if (body.classList.contains('light-mode')) {
                theme = 'light';
            }
            localStorage.setItem('theme', theme);
        });
    }

    // Scroll Progress Bar
    ...

    // Intersection Observer for Reveal Animations
    const observerOptions = {
        threshold: 0.1,
        rootMargin: "0px 0px -50px 0px"
    };

    const revealObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('active');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    const revealElements = document.querySelectorAll('.reveal');
    revealElements.forEach(el => revealObserver.observe(el));

    // Staggered entry for grid items
    const gridItems = document.querySelectorAll('.articles-grid .article-card');
    gridItems.forEach((item, index) => {
        item.style.transitionDelay = `${(index % 3) * 0.1}s`;
        item.classList.add('reveal');
        revealObserver.observe(item);
    });
});
