// Portfolio JavaScript

// Theme Toggle - runs immediately to prevent flash
(function() {
    const savedTheme = localStorage.getItem('theme') || 'dark';
    document.documentElement.setAttribute('data-theme', savedTheme);
})();

document.addEventListener('DOMContentLoaded', function() {
    // Theme Picker Modal
    const themeModal = document.getElementById('theme-modal');
    const hasSelectedTheme = localStorage.getItem('hasSelectedTheme');

    // Show modal if user hasn't selected a theme before
    if (!hasSelectedTheme && themeModal) {
        setTimeout(() => {
            themeModal.classList.add('active');
        }, 500);
    }

    // Handle theme option clicks
    const themeOptions = document.querySelectorAll('.theme-option');
    themeOptions.forEach(option => {
        option.addEventListener('click', function() {
            const selectedTheme = this.dataset.theme;
            localStorage.setItem('theme', selectedTheme);
            localStorage.setItem('hasSelectedTheme', 'true');
            location.reload();
        });
    });

    // Theme Toggle
    const themeToggle = document.getElementById('theme-toggle');
    const themes = ['dark', 'normal', 'light'];

    function getCurrentTheme() {
        return document.documentElement.getAttribute('data-theme') || 'dark';
    }

    function setTheme(theme) {
        document.documentElement.setAttribute('data-theme', theme);
        localStorage.setItem('theme', theme);
    }

    function cycleTheme() {
        const currentTheme = getCurrentTheme();
        const currentIndex = themes.indexOf(currentTheme);
        const nextIndex = (currentIndex + 1) % themes.length;
        const nextTheme = themes[nextIndex];
        setTheme(nextTheme);
        showThemeTooltip(nextTheme);
    }

    function showThemeTooltip(theme) {
        const themeNames = {
            'dark': 'Dark Mode',
            'normal': 'Normal Mode',
            'light': 'Light Mode'
        };

        const existingTooltip = document.querySelector('.theme-tooltip');
        if (existingTooltip) {
            existingTooltip.remove();
        }

        const tooltip = document.createElement('div');
        tooltip.className = 'theme-tooltip';
        tooltip.textContent = themeNames[theme];
        themeToggle.appendChild(tooltip);

        setTimeout(() => {
            tooltip.remove();
        }, 1500);
    }

    if (themeToggle) {
        themeToggle.addEventListener('click', cycleTheme);
    }

    // Typewriter Effect
    const typewriter = document.querySelector('.typewriter');
    if (typewriter) {
        const text = typewriter.dataset.text;
        const textElement = typewriter.querySelector('.typewriter-text');
        const cursor = typewriter.querySelector('.typewriter-cursor');
        let charIndex = 0;
        const typingSpeed = 100;

        function type() {
            if (charIndex < text.length) {
                textElement.textContent += text.charAt(charIndex);
                charIndex++;
                setTimeout(type, typingSpeed);
            } else {
                // Fade out and remove cursor after typing is done
                cursor.style.transition = 'opacity 2s ease';
                cursor.style.opacity = '0';
                setTimeout(() => cursor.remove(), 2000);
            }
        }

        // Start typing after a short delay
        setTimeout(type, 500);
    }

    // Mobile Navigation Toggle
    const navToggle = document.getElementById('nav-toggle');
    const navMenu = document.getElementById('nav-menu');

    if (navToggle && navMenu) {
        navToggle.addEventListener('click', function() {
            navToggle.classList.toggle('active');
            navMenu.classList.toggle('active');
            document.body.style.overflow = navMenu.classList.contains('active') ? 'hidden' : '';
        });

        const navLinks = navMenu.querySelectorAll('.nav-link');
        navLinks.forEach(link => {
            link.addEventListener('click', function() {
                navToggle.classList.remove('active');
                navMenu.classList.remove('active');
                document.body.style.overflow = '';
            });
        });

        document.addEventListener('click', function(e) {
            if (!navToggle.contains(e.target) && !navMenu.contains(e.target)) {
                navToggle.classList.remove('active');
                navMenu.classList.remove('active');
                document.body.style.overflow = '';
            }
        });
    }

    // Navbar scroll effect
    const navbar = document.getElementById('navbar');
    let lastScroll = 0;

    window.addEventListener('scroll', function() {
        const currentScroll = window.pageYOffset;

        if (currentScroll > 50) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }

        lastScroll = currentScroll;
    });

    // Active navigation link on scroll
    const sections = document.querySelectorAll('section[id]');
    const navLinksAll = document.querySelectorAll('.nav-link');

    function setActiveNavLink() {
        const scrollPosition = window.scrollY + 100;

        sections.forEach(section => {
            const sectionTop = section.offsetTop;
            const sectionHeight = section.offsetHeight;
            const sectionId = section.getAttribute('id');

            if (scrollPosition >= sectionTop && scrollPosition < sectionTop + sectionHeight) {
                navLinksAll.forEach(link => {
                    link.classList.remove('active');
                    if (link.getAttribute('href') === `#${sectionId}`) {
                        link.classList.add('active');
                    }
                });
            }
        });
    }

    window.addEventListener('scroll', setActiveNavLink);
    setActiveNavLink();

    // Smooth scroll for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            const targetElement = document.querySelector(targetId);

            if (targetElement) {
                const navbarHeight = navbar.offsetHeight;
                const targetPosition = targetElement.offsetTop - navbarHeight;

                window.scrollTo({
                    top: targetPosition,
                    behavior: 'smooth'
                });
            }
        });
    });

    // ============================================
    // Scroll Animation System
    // ============================================

    const animatableSelectors = [
        '.section-title',
        '.skill-category',
        '.timeline-item',
        '.education-card',
        '.certificate-card',
        '.project-card',
        '.contact-method',
        '.about-text',
        '.about-image',
        '.about-stats',
        '.calendly-preview',
        '.hero-schedule',
        '.schedule-benefits',
        '.benefit-card'
    ];

    // Check if element is in viewport
    function isInViewport(element) {
        const rect = element.getBoundingClientRect();
        return (
            rect.top < window.innerHeight - 50 &&
            rect.bottom > 0
        );
    }

    // Setup animations
    function setupAnimations() {
        const allAnimatable = document.querySelectorAll(animatableSelectors.join(', '));

        allAnimatable.forEach((el, globalIndex) => {
            // Skip if already setup
            if (el.dataset.animationSetup) return;
            el.dataset.animationSetup = 'true';

            // Find siblings for stagger calculation
            const parent = el.parentElement;
            const selector = animatableSelectors.find(s => el.matches(s));
            const siblings = parent ? Array.from(parent.querySelectorAll(selector)) : [el];
            const siblingIndex = siblings.indexOf(el);

            // Check if element is already in viewport on page load
            if (isInViewport(el)) {
                // Element is already visible - add classes without animation
                el.classList.add('animate-on-scroll', 'no-transition', 'animated');
                // Remove no-transition after a frame to enable future transitions
                requestAnimationFrame(() => {
                    requestAnimationFrame(() => {
                        el.classList.remove('no-transition');
                    });
                });
            } else {
                // Element is not visible - set up for scroll animation
                el.classList.add('animate-on-scroll');
                el.style.setProperty('--stagger-delay', `${siblingIndex * 0.1}s`);
            }
        });
    }

    // Intersection Observer for scroll animations
    const scrollObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting && !entry.target.classList.contains('animated')) {
                // Get stagger delay
                const delay = getComputedStyle(entry.target).getPropertyValue('--stagger-delay') || '0s';
                const delayMs = parseFloat(delay) * 1000;

                setTimeout(() => {
                    entry.target.classList.add('animated');
                }, delayMs);

                scrollObserver.unobserve(entry.target);
            }
        });
    }, {
        root: null,
        rootMargin: '0px 0px -50px 0px',
        threshold: 0.1
    });

    // Initialize
    setupAnimations();

    // Observe elements that aren't already animated
    document.querySelectorAll('.animate-on-scroll:not(.animated)').forEach(el => {
        scrollObserver.observe(el);
    });

    // ============================================
    // Section animations
    // ============================================
    const sectionObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('in-view');
            }
        });
    }, {
        root: null,
        rootMargin: '0px',
        threshold: 0.1
    });

    document.querySelectorAll('.section').forEach(section => {
        sectionObserver.observe(section);
    });

    // ============================================
    // Parallax effect for hero background
    // ============================================
    const heroGradient = document.querySelector('.hero-gradient');

    if (heroGradient) {
        window.addEventListener('scroll', function() {
            const scrolled = window.pageYOffset;
            heroGradient.style.transform = `translateY(${scrolled * 0.3}px)`;
        });
    }

    // ============================================
    // Skill tags hover effect
    // ============================================
    const skillTags = document.querySelectorAll('.skill-tag[data-proficiency]');

    skillTags.forEach(tag => {
        tag.addEventListener('mouseenter', function() {
            const proficiency = this.dataset.proficiency;
            if (proficiency) {
                this.style.setProperty('--proficiency', `${proficiency}%`);
            }
        });
    });

    // ============================================
    // Preloader
    // ============================================
    window.addEventListener('load', function() {
        document.body.classList.add('loaded');
    });

    // Console easter egg
    console.log('%c Welcome to my portfolio! ', 'background: linear-gradient(135deg, #6366f1, #8b5cf6); color: white; padding: 10px 20px; border-radius: 5px; font-size: 14px;');
    console.log('%c Built with Django & Love ', 'color: #6366f1; font-size: 12px;');
});
