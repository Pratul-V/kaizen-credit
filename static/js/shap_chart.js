/**
 * SHAP Waterfall Chart Visualization
 */

function initShapChart(shapData, baseValue) {
    const canvas = document.getElementById('shap-chart-canvas');
    if (!canvas || !shapData || shapData.length === 0) return;

    const ctx = canvas.getContext('2d');
    
    // Extract data
    const labels = shapData.map(d => `${d.feature} (${d.display})`);
    const values = shapData.map(d => d.value);
    
    // Determine colors
    // Positive (pushes towards default) = Red/Orange
    // Negative (pushes towards safe) = Blue/Green
    const backgroundColors = values.map(v => 
        v > 0 ? 'rgba(244, 63, 94, 0.8)' : 'rgba(59, 130, 246, 0.8)'
    );
    const borderColors = values.map(v => 
        v > 0 ? '#f43f5e' : '#3b82f6'
    );

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Impact on Prediction',
                data: values,
                backgroundColor: backgroundColors,
                borderColor: borderColors,
                borderWidth: 1,
                borderRadius: 4
            }]
        },
        options: {
            indexAxis: 'y',
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false },
                tooltip: {
                    callbacks: {
                        label: (context) => {
                            const val = context.raw;
                            const sign = val > 0 ? '+' : '';
                            return ` Impact: ${sign}${val.toFixed(4)}`;
                        }
                    }
                }
            },
            scales: {
                x: {
                    title: {
                        display: true,
                        text: 'SHAP Value (Impact on Default Risk)',
                        color: '#94a3b8'
                    },
                    grid: {
                        color: (ctx) => ctx.tick.value === 0 ? 'rgba(255,255,255,0.2)' : 'rgba(255,255,255,0.05)',
                        lineWidth: (ctx) => ctx.tick.value === 0 ? 2 : 1
                    },
                    ticks: { color: '#94a3b8' }
                },
                y: {
                    grid: { display: false },
                    ticks: { color: '#f1f5f9' }
                }
            }
        }
    });

    // Display Base Value
    const baseValEl = document.getElementById('shap-base-value');
    if (baseValEl) {
        baseValEl.innerHTML = `Model Base Expected Value: <strong>${baseValue.toFixed(4)}</strong>`;
    }
}
