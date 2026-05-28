/**
 * Animated Circular Risk Gauge using HTML5 Canvas
 */

function initRiskGauge(probability) {
    const canvas = document.getElementById('risk-gauge-canvas');
    if (!canvas) return;
    
    const ctx = canvas.getContext('2d');
    const valueEl = document.getElementById('gauge-value');
    
    // Setup dimensions
    const width = canvas.width;
    const height = canvas.height;
    const cx = width / 2;
    const cy = height / 2 + 10; // offset down slightly
    const radius = 90;
    const strokeWidth = 14;
    
    // Angles (in radians)
    const startAngle = Math.PI * 0.8;
    const endAngle = Math.PI * 2.2;
    const totalAngle = endAngle - startAngle;
    
    // Animation state
    let currentProb = 0;
    const targetProb = probability;
    const duration = 1500; // ms
    const startTime = performance.now();
    
    function getColor(p) {
        if (p < 20) return '#10b981'; // Green
        if (p < 45) return '#f59e0b'; // Amber
        if (p < 70) return '#f97316'; // Orange
        return '#ef4444';             // Red
    }
    
    function drawTrack() {
        ctx.beginPath();
        ctx.arc(cx, cy, radius, startAngle, endAngle);
        ctx.strokeStyle = 'rgba(255, 255, 255, 0.1)';
        ctx.lineWidth = strokeWidth;
        ctx.lineCap = 'round';
        ctx.stroke();
    }
    
    function drawProgress(p) {
        if (p <= 0) return;
        
        const currentEndAngle = startAngle + (totalAngle * (p / 100));
        const color = getColor(p);
        
        ctx.beginPath();
        ctx.arc(cx, cy, radius, startAngle, currentEndAngle);
        ctx.strokeStyle = color;
        ctx.lineWidth = strokeWidth;
        ctx.lineCap = 'round';
        
        // Add glow
        ctx.shadowBlur = 10;
        ctx.shadowColor = color;
        
        ctx.stroke();
        
        // Reset shadow
        ctx.shadowBlur = 0;
    }
    
    function animate(currentTime) {
        const elapsed = currentTime - startTime;
        const progress = Math.min(elapsed / duration, 1);
        
        // Easing (easeOutQuart)
        const ease = 1 - Math.pow(1 - progress, 4);
        
        currentProb = targetProb * ease;
        
        // Clear and redraw
        ctx.clearRect(0, 0, width, height);
        drawTrack();
        drawProgress(currentProb);
        
        // Update text
        valueEl.innerText = currentProb.toFixed(1);
        valueEl.style.color = getColor(currentProb);
        
        if (progress < 1) {
            requestAnimationFrame(animate);
        } else {
            // Final exact frame
            ctx.clearRect(0, 0, width, height);
            drawTrack();
            drawProgress(targetProb);
            valueEl.innerText = targetProb.toFixed(1);
            valueEl.style.color = getColor(targetProb);
        }
    }
    
    // Start animation
    requestAnimationFrame(animate);
}
