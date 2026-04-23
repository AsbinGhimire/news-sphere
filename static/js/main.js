/**
 * Main Frontend Logic for GlobalNews Portal
 * Handles theme switching, scroll animations, and AJAX interactions.
 */

document.addEventListener('DOMContentLoaded', () => {
    
    // --- Theme Engine Logic ---
    // Persists user preference (dark/light) in localStorage
    const body = document.body;
    const themeToggle = document.getElementById('theme-toggle');
    const currentTheme = localStorage.getItem('theme');

    // Apply saved theme on initial load
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

    // --- Scroll Progress Bar ---
    // Visual indicator at the top of the page showing how far the user has scrolled
    const progress = document.getElementById('scroll-progress');
    if (progress) {
        window.addEventListener('scroll', () => {
            const winScroll = document.body.scrollTop || document.documentElement.scrollTop;
            const height = document.documentElement.scrollHeight - document.documentElement.clientHeight;
            const scrolled = (winScroll / height) * 100;
            progress.style.width = scrolled + "%";
        });
    }

    // --- reveal Animations (Intersection Observer) ---
    // Triggers entry animations when elements enter the viewport
    const observerOptions = {
        threshold: 0.1,
        rootMargin: "0px 0px -50px 0px" // Triggers slightly before the element is fully visible
    };

    const revealObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('active');
                observer.unobserve(entry.target); // Animates only once
            }
        });
    }, observerOptions);

    // Observe all elements with the 'reveal' class
    const revealElements = document.querySelectorAll('.reveal');
    revealElements.forEach(el => revealObserver.observe(el));

    // --- Staggered Entry for Grid Items ---
    // Adds a slight delay to each card in a grid for a professional cascading effect
    const gridItems = document.querySelectorAll('.articles-grid .article-card');
    gridItems.forEach((item, index) => {
        item.style.transitionDelay = `${(index % 3) * 0.1}s`;
        item.classList.add('reveal');
        revealObserver.observe(item);
    });

    // --- Back to Top Button ---
    // Smooth scroll back to the top of the page
    const backToTop = document.getElementById('back-to-top');
    if (backToTop) {
        window.addEventListener('scroll', () => {
            // Show button only after scrolling 500px down
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

    // --- AJAX Newsletter Subscription ---
    // Handles form submission without refreshing the page
    const subscribeForm = document.querySelector('.subscribe-form');
    if (subscribeForm) {
        subscribeForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const emailInput = subscribeForm.querySelector('input[name="email"]');
            const submitBtn = subscribeForm.querySelector('button');
            const alertContainer = document.querySelector('.alert-container') || document.createElement('div');
            
            // Create alert container if it doesn't exist
            if (!document.querySelector('.alert-container')) {
                alertContainer.className = 'alert-container';
                subscribeForm.after(alertContainer);
            }

            // UI feedback during request
            submitBtn.disabled = true;
            submitBtn.textContent = 'Joining...';

            const formData = new FormData(subscribeForm);
            
            try {
                const response = await fetch(subscribeForm.action, {
                    method: 'POST',
                    body: formData,
                    headers: {
                        'X-Requested-With': 'XMLHttpRequest', // Identifies this as an AJAX request for Django
                    }
                });

                const data = await response.json();
                
                // Display success/error message
                alertContainer.innerHTML = `<div class="alert alert-${data.status}">${data.message}</div>`;
                
                if (data.status === 'success') {
                    emailInput.value = ''; // Clear input on success
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
