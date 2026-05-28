/**
 * Client-side Form Validation & UI Logic
 */

document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('predict-form');
    if (!form) return;

    const incomeInput = document.getElementById('person_income');
    const loanInput = document.getElementById('loan_amnt');
    const ratioDisplay = document.getElementById('loan-to-income-display');
    const submitBtn = document.getElementById('submit-btn');

    // Auto-calculate Loan-to-Income Ratio
    function updateRatio() {
        const income = parseFloat(incomeInput.value) || 0;
        const loan = parseFloat(loanInput.value) || 0;
        
        if (income > 0) {
            const ratio = (loan / income) * 100;
            ratioDisplay.innerText = `${ratio.toFixed(1)}%`;
            
            // Highlight if high risk (> 200%)
            if (ratio > 200) {
                ratioDisplay.style.color = 'var(--color-rose)';
            } else if (ratio > 100) {
                ratioDisplay.style.color = 'var(--color-amber)';
            } else {
                ratioDisplay.style.color = 'var(--color-blue)';
            }
        } else {
            ratioDisplay.innerText = '—';
        }
    }

    incomeInput.addEventListener('input', updateRatio);
    loanInput.addEventListener('input', updateRatio);
    
    // Initial calculation if values exist
    updateRatio();

    // Form Submission State
    form.addEventListener('submit', () => {
        // Hide icon/text, show spinner
        const icon = submitBtn.querySelector('.btn-icon');
        const text = submitBtn.querySelector('.btn-text');
        const loading = submitBtn.querySelector('.btn-loading');
        
        if (icon) icon.style.display = 'none';
        if (text) text.style.display = 'none';
        if (loading) loading.style.display = 'inline-flex';
        
        submitBtn.disabled = true;
        submitBtn.style.opacity = '0.8';
        submitBtn.style.cursor = 'not-allowed';
    });

    // Dismiss Alerts manually
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        alert.addEventListener('click', () => {
            alert.style.opacity = '0';
            alert.style.transform = 'translateY(-10px)';
            setTimeout(() => alert.remove(), 300);
        });
        alert.style.cursor = 'pointer';
        alert.title = 'Click to dismiss';
    });
});
