// Simulator logic for what-if scenarios
document.addEventListener('DOMContentLoaded', function() {
    const loanSlider = document.getElementById('sim_loan_amnt');
    const incomeSlider = document.getElementById('sim_income');
    const loanValDisplay = document.getElementById('sim_loan_val');
    const incomeValDisplay = document.getElementById('sim_income_val');
    const originalForm = document.getElementById('predict-form');
    
    if(!loanSlider || !incomeSlider) return;

    let debounceTimer;

    function formatCurrency(val) {
        return parseInt(val).toLocaleString();
    }

    function updateSimulation() {
        // Build payload from original form but override with sliders
        const formData = new FormData(originalForm);
        const dataObj = {};
        formData.forEach((value, key) => {
            dataObj[key] = value;
        });

        dataObj['loan_amnt'] = loanSlider.value;
        dataObj['person_income'] = incomeSlider.value;

        // Visual update
        loanValDisplay.innerText = formatCurrency(loanSlider.value);
        incomeValDisplay.innerText = formatCurrency(incomeSlider.value);

        // Fetch new data
        fetch('/api/simulate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(dataObj)
        })
        .then(response => response.json())
        .then(data => {
            if(data.error) {
                console.error("Simulation error", data.error);
                return;
            }
            
            // Re-initialize gauge with new probability
            if(typeof initRiskGauge === 'function') {
                initRiskGauge(data.probability);
            }
            
            // Animate banner change if needed
            const policyBanner = document.getElementById('policy-banner');
            if(policyBanner && data.pricing) {
                policyBanner.className = 'policy-banner fade-in-up ' + data.pricing.risk_metadata.css_class;
                policyBanner.querySelector('.policy-action').innerHTML = data.pricing.risk_metadata.icon + ' ' + data.pricing.action;
                policyBanner.querySelector('.policy-reason').innerText = data.pricing.risk_metadata.explanation;
            }
        })
        .catch(err => console.error(err));
    }

    loanSlider.addEventListener('input', function() {
        loanValDisplay.innerText = formatCurrency(loanSlider.value);
        clearTimeout(debounceTimer);
        debounceTimer = setTimeout(updateSimulation, 500);
    });

    incomeSlider.addEventListener('input', function() {
        incomeValDisplay.innerText = formatCurrency(incomeSlider.value);
        clearTimeout(debounceTimer);
        debounceTimer = setTimeout(updateSimulation, 500);
    });
});
