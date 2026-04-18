document.addEventListener('DOMContentLoaded', () => {
    // Scroll Progress Bar
    const progress = document.getElementById('scroll-progress');
    if (progress) {
        window.addEventListener('scroll', () => {
            const winScroll = document.body.scrollTop || document.documentElement.scrollTop;
            const height = document.documentElement.scrollHeight - document.documentElement.clientHeight;
            const scrolled = (winScroll / height) * 100;
            progress.style.width = scrolled + "%";
        });
    }

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
