// static/js/theme.js
(function() {
    // Execute immediately to prevent flash of wrong theme
    const savedTheme = localStorage.getItem('creditguard_theme');
    if (savedTheme === 'light') {
        document.documentElement.classList.add('light-theme');
        document.addEventListener("DOMContentLoaded", () => {
            const logo = document.getElementById('kaizen-logo');
            if(logo) logo.src = "/static/img/Logo_Light.png";
        });
    }
})();

function toggleTheme(event) {
    const isLight = document.documentElement.classList.contains('light-theme');
    const newTheme = isLight ? 'dark' : 'light';
    
    // View Transitions API fallback
    if (!document.startViewTransition) {
        applyTheme(newTheme);
        return;
    }

    // Get click position for radial animation
    const x = event.clientX;
    const y = event.clientY;
    const endRadius = Math.hypot(
        Math.max(x, innerWidth - x),
        Math.max(y, innerHeight - y)
    );

    const transition = document.startViewTransition(() => {
        applyTheme(newTheme);
    });

    transition.ready.then(() => {
        const clipPath = [
            `circle(0px at ${x}px ${y}px)`,
            `circle(${endRadius}px at ${x}px ${y}px)`
        ];

        document.documentElement.animate(
            {
                clipPath: clipPath
            },
            {
                duration: 500,
                easing: "ease-in-out",
                pseudoElement: "::view-transition-new(root)"
            }
        );
    });
}

function applyTheme(theme) {
    const logo = document.getElementById('kaizen-logo');
    if (logo) logo.classList.add('logo-transition');
    
    if (theme === 'light') {
        document.documentElement.classList.add('light-theme');
        localStorage.setItem('creditguard_theme', 'light');
        if (logo) logo.src = "/static/img/Logo_Light.png";
    } else {
        document.documentElement.classList.remove('light-theme');
        localStorage.setItem('creditguard_theme', 'dark');
        if (logo) logo.src = "/static/img/Logo_Dark.png";
    }
    
    if (logo) {
        // Allow the browser to paint the new src before removing the transition class
        requestAnimationFrame(() => {
            requestAnimationFrame(() => {
                logo.classList.remove('logo-transition');
            });
        });
    }
}
