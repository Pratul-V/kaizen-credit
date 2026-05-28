/**
 * Dashboard Charts Initialization
 * Fetches data from /api/analytics/* and renders Chart.js charts
 */

document.addEventListener('DOMContentLoaded', () => {
    // Check if we're on the dashboard
    if (!document.getElementById('chart-grade')) return;

    // Common Chart.js Defaults for Dark Theme
    Chart.defaults.color = '#94a3b8';
    Chart.defaults.font.family = "'Inter', sans-serif";
    Chart.defaults.plugins.tooltip.backgroundColor = 'rgba(17, 24, 39, 0.9)';
    Chart.defaults.plugins.tooltip.titleColor = '#f1f5f9';
    Chart.defaults.plugins.tooltip.bodyColor = '#f1f5f9';
    Chart.defaults.plugins.tooltip.borderColor = 'rgba(255,255,255,0.1)';
    Chart.defaults.plugins.tooltip.borderWidth = 1;
    Chart.defaults.plugins.tooltip.padding = 10;
    Chart.defaults.plugins.tooltip.cornerRadius = 8;
    
    const commonOptions = {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: { display: false }
        },
        scales: {
            x: {
                grid: { color: 'rgba(255,255,255,0.05)', drawBorder: false },
                ticks: { color: '#94a3b8' }
            },
            y: {
                grid: { color: 'rgba(255,255,255,0.05)', drawBorder: false },
                ticks: { color: '#94a3b8' }
            }
        }
    };

    // Helper to fetch data
    async function fetchData(endpoint) {
        try {
            const response = await fetch(`/api/analytics/${endpoint}`);
            if (!response.ok) throw new Error('Network response was not ok');
            return await response.json();
        } catch (error) {
            console.error(`Error fetching ${endpoint}:`, error);
            return null;
        }
    }

    // 1. Default Rate by Grade (Doughnut)
    async function initGradeChart() {
        const data = await fetchData('default-by-grade');
        if (!data) return;

        const ctx = document.getElementById('chart-grade').getContext('2d');
        
        // Create gradient
        const gradient = ctx.createLinearGradient(0, 0, 0, 300);
        gradient.addColorStop(0, '#f43f5e'); // Rose
        gradient.addColorStop(1, '#f97316'); // Orange

        new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: data.labels,
                datasets: [{
                    data: data.values,
                    backgroundColor: [
                        '#10b981', '#34d399', // A, B (Green)
                        '#fcd34d', '#fbbf24', // C, D (Yellow)
                        '#f97316', '#ea580c', // E, F (Orange)
                        '#e11d48'             // G (Red)
                    ],
                    borderWidth: 0,
                    hoverOffset: 4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                cutout: '75%',
                plugins: {
                    legend: {
                        display: true,
                        position: 'right',
                        labels: { boxWidth: 12, usePointStyle: true }
                    },
                    tooltip: {
                        callbacks: {
                            label: (context) => ` ${context.raw}% Default Rate`
                        }
                    }
                }
            }
        });
    }

    // 2. Default Rate by Intent (Bar)
    async function initIntentChart() {
        const data = await fetchData('default-by-intent');
        if (!data) return;

        const ctx = document.getElementById('chart-intent').getContext('2d');
        new Chart(ctx, {
            type: 'bar',
            data: {
                labels: data.labels,
                datasets: [{
                    label: 'Default Rate (%)',
                    data: data.values,
                    backgroundColor: 'rgba(59, 130, 246, 0.8)',
                    borderRadius: 4
                }]
            },
            options: {
                ...commonOptions,
                indexAxis: 'y', // Horizontal bar
            }
        });
    }

    // 3. Income Distribution (Bar)
    async function initIncomeChart() {
        const data = await fetchData('income-distribution');
        if (!data) return;

        const ctx = document.getElementById('chart-income').getContext('2d');
        new Chart(ctx, {
            type: 'bar',
            data: {
                labels: data.labels,
                datasets: [
                    {
                        label: 'Defaults',
                        data: data.defaults,
                        backgroundColor: 'rgba(244, 63, 94, 0.8)', // Rose
                        borderRadius: 4,
                        stacked: true
                    },
                    {
                        label: 'Non-Defaults',
                        data: data.non_defaults,
                        backgroundColor: 'rgba(16, 185, 129, 0.8)', // Emerald
                        borderRadius: 4,
                        stacked: true
                    }
                ]
            },
            options: {
                ...commonOptions,
                plugins: { legend: { display: true, position: 'top' } },
                scales: {
                    x: { stacked: true, grid: { display: false } },
                    y: { stacked: true, grid: { color: 'rgba(255,255,255,0.05)' } }
                }
            }
        });
    }

    // 4. Loan Amount Distribution (Bar)
    async function initLoanChart() {
        const data = await fetchData('loan-distribution');
        if (!data) return;

        const ctx = document.getElementById('chart-loan').getContext('2d');
        new Chart(ctx, {
            type: 'bar',
            data: {
                labels: data.labels,
                datasets: [
                    {
                        label: 'Defaults',
                        data: data.defaults,
                        backgroundColor: 'rgba(244, 63, 94, 0.8)',
                        stacked: true
                    },
                    {
                        label: 'Non-Defaults',
                        data: data.non_defaults,
                        backgroundColor: 'rgba(59, 130, 246, 0.8)', // Blue
                        stacked: true
                    }
                ]
            },
            options: {
                ...commonOptions,
                plugins: { legend: { display: true, position: 'top' } },
                scales: { x: { stacked: true }, y: { stacked: true } }
            }
        });
    }

    // 5. Age Distribution (Line)
    async function initAgeChart() {
        const data = await fetchData('age-distribution');
        if (!data) return;

        const ctx = document.getElementById('chart-age').getContext('2d');
        new Chart(ctx, {
            type: 'line',
            data: {
                labels: data.labels,
                datasets: [
                    {
                        label: 'Defaults',
                        data: data.defaults,
                        borderColor: '#f43f5e',
                        backgroundColor: 'rgba(244, 63, 94, 0.1)',
                        fill: true,
                        tension: 0.4
                    },
                    {
                        label: 'Non-Defaults',
                        data: data.non_defaults,
                        borderColor: '#10b981',
                        backgroundColor: 'rgba(16, 185, 129, 0.1)',
                        fill: true,
                        tension: 0.4
                    }
                ]
            },
            options: {
                ...commonOptions,
                plugins: { legend: { display: true } },
                interaction: { mode: 'index', intersect: false }
            }
        });
    }

    // 6. Interest Rate by Grade (Line/Bar combo)
    async function initInterestChart() {
        const data = await fetchData('interest-by-grade');
        if (!data) return;

        const ctx = document.getElementById('chart-interest').getContext('2d');
        new Chart(ctx, {
            type: 'line',
            data: {
                labels: data.labels,
                datasets: [{
                    label: 'Avg Interest Rate (%)',
                    data: data.values,
                    borderColor: '#8b5cf6', // Purple
                    backgroundColor: 'rgba(139, 92, 246, 0.2)',
                    borderWidth: 2,
                    pointBackgroundColor: '#8b5cf6',
                    pointRadius: 4,
                    fill: true,
                    tension: 0.2
                }]
            },
            options: {
                ...commonOptions,
                scales: {
                    y: {
                        beginAtZero: false,
                        grid: { color: 'rgba(255,255,255,0.05)' }
                    }
                }
            }
        });
    }

    // Initialize all charts
    initGradeChart();
    initIntentChart();
    initIncomeChart();
    initLoanChart();
    initAgeChart();
    initInterestChart();

    // --- KPI Animated Counters ---
    const counters = document.querySelectorAll('.counter');
    counters.forEach(counter => {
        const target = +counter.getAttribute('data-target');
        const prefix = counter.getAttribute('data-prefix') || '';
        const suffix = counter.getAttribute('data-suffix') || '';
        const format = counter.getAttribute('data-format'); // 'compact'
        
        const duration = 1500; // ms
        const steps = 60;
        const stepTime = Math.abs(Math.floor(duration / steps));
        
        let current = 0;
        const increment = target / steps;
        
        const timer = setInterval(() => {
            current += increment;
            if (current >= target) {
                current = target;
                clearInterval(timer);
            }
            
            // Format number
            let displayStr = '';
            if (format === 'compact' && current >= 1000) {
                displayStr = (current / 1000).toFixed(1) + 'k';
            } else if (Number.isInteger(target)) {
                displayStr = Math.floor(current).toLocaleString();
            } else {
                displayStr = current.toFixed(2);
            }
            
            counter.innerText = prefix + displayStr + suffix;
        }, stepTime);
    });
});
