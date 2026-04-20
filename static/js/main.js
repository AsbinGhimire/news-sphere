document.addEventListener('DOMContentLoaded', () => {
    // Theme Engine Logic
    const body = document.body;
    const themeToggle = document.getElementById('theme-toggle');
    const currentTheme = localStorage.getItem('theme');

    // Default to Light Mode (none), add 'dark-mode' if preference is dark
    if (currentTheme === 'dark') {
        body.classList.add('dark-mode');
    }

    if (themeToggle) {
        themeToggle.addEventListener('click', () => {
            body.classList.toggle('dark-mode');
            const theme = body.classList.contains('dark-mode') ? 'dark' : 'light';
            localStorage.setItem('theme', theme);
        });
    }

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

    // Back to Top Logic
    const backToTop = document.getElementById('back-to-top');
    if (backToTop) {
        window.addEventListener('scroll', () => {
            if (window.pageYOffset > 500) {
                backToTop.classList.add('show');
            } else {
                backToTop.classList.remove('show');
            }
        });

        backToTop.addEventListener('click', () => {
            window.scrollTo({ top: 0, behavior: 'smooth' });
        });
    }

    // AJAX Newsletter Subscription
    const subscribeForm = document.querySelector('.subscribe-form');
    if (subscribeForm) {
        subscribeForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const emailInput = subscribeForm.querySelector('input[name="email"]');
            const submitBtn = subscribeForm.querySelector('button');
            const alertContainer = document.querySelector('.alert-container') || document.createElement('div');
            
            if (!document.querySelector('.alert-container')) {
                alertContainer.className = 'alert-container';
                subscribeForm.after(alertContainer);
            }

            submitBtn.disabled = true;
            submitBtn.textContent = 'Joining...';

            const formData = new FormData(subscribeForm);
            
            try {
                const response = await fetch(subscribeForm.action, {
                    method: 'POST',
                    body: formData,
                    headers: {
                        'X-Requested-With': 'XMLHttpRequest',
                    }
                });

                const data = await response.json();
                
                alertContainer.innerHTML = `<div class="alert alert-${data.status}">${data.message}</div>`;
                
                if (data.status === 'success') {
                    emailInput.value = '';
                }
            } catch (error) {
                alertContainer.innerHTML = `<div class="alert alert-error">Something went wrong. Please try again later.</div>`;
            } finally {
                submitBtn.disabled = false;
                submitBtn.textContent = 'Join';
            }
        });
    }
});
