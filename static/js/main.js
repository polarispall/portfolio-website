// Portfolio JavaScript

// Theme Toggle - runs immediately to prevent flash
(function() {
    const savedTheme = localStorage.getItem('theme') || 'dark';
    document.documentElement.setAttribute('data-theme', savedTheme);
})();

document.addEventListener('DOMContentLoaded', function() {
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

        // Show tooltip with theme name
        showThemeTooltip(nextTheme);
    }

    function showThemeTooltip(theme) {
        const themeNames = {
            'dark': 'Dark Mode',
            'normal': 'Normal Mode',
            'light': 'Light Mode'
        };

        // Remove existing tooltip
        const existingTooltip = document.querySelector('.theme-tooltip');
        if (existingTooltip) {
            existingTooltip.remove();
        }

        // Create and show tooltip
        const tooltip = document.createElement('div');
        tooltip.className = 'theme-tooltip';
        tooltip.textContent = themeNames[theme];
        themeToggle.appendChild(tooltip);

        // Remove tooltip after animation
        setTimeout(() => {
            tooltip.remove();
        }, 1500);
    }

    if (themeToggle) {
        themeToggle.addEventListener('click', cycleTheme);
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

        // Close menu when clicking a link
        const navLinks = navMenu.querySelectorAll('.nav-link');
        navLinks.forEach(link => {
            link.addEventListener('click', function() {
                navToggle.classList.remove('active');
                navMenu.classList.remove('active');
                document.body.style.overflow = '';
            });
        });

        // Close menu when clicking outside
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

    // Elements to animate on scroll
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

    // Add animation classes with stagger delay
    function setupAnimations() {
        animatableSelectors.forEach(selector => {
            const elements = document.querySelectorAll(selector);
            elements.forEach((el, index) => {
                if (!el.classList.contains('animate-on-scroll')) {
                    el.classList.add('animate-on-scroll');
                    // Add stagger delay based on siblings
                    const parent = el.parentElement;
                    const siblings = parent.querySelectorAll(selector);
                    const siblingIndex = Array.from(siblings).indexOf(el);
                    el.style.setProperty('--animation-order', siblingIndex);
                }
            });
        });
    }

    // Intersection Observer for scroll animations
    const scrollObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                // Add animated class with a small delay based on order
                const order = getComputedStyle(entry.target).getPropertyValue('--animation-order') || 0;
                const delay = parseInt(order) * 100; // 100ms stagger

                setTimeout(() => {
                    entry.target.classList.add('animated');
                }, delay);

                // Stop observing once animated
                scrollObserver.unobserve(entry.target);
            }
        });
    }, {
        root: null,
        rootMargin: '0px 0px -50px 0px',
        threshold: 0.1
    });

    // Setup and observe elements
    setupAnimations();
    document.querySelectorAll('.animate-on-scroll').forEach(el => {
        scrollObserver.observe(el);
    });

    // ============================================
    // Section title animations
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
