// static/js/consent.js
document.addEventListener('DOMContentLoaded', () => {
    const consentGate = document.getElementById('consent-gate');
    const btnAccept = document.getElementById('btn-accept-consent');
    const btnDecline = document.getElementById('btn-decline-consent');
    const chkTerms = document.getElementById('chk-terms');
    const chkPrivacy = document.getElementById('chk-privacy');

    // Check if already consented
    const hasConsented = localStorage.getItem('creditguard_consent_v1');
    if (!hasConsented) {
        consentGate.style.display = 'flex';
        // Trap focus to prevent interacting with the app behind the modal
        document.body.style.overflow = 'hidden';
    }

    function checkValidity() {
        if (chkTerms.checked && chkPrivacy.checked) {
            btnAccept.disabled = false;
            btnAccept.classList.remove('btn-disabled');
        } else {
            btnAccept.disabled = true;
            btnAccept.classList.add('btn-disabled');
        }
    }

    chkTerms.addEventListener('change', checkValidity);
    chkPrivacy.addEventListener('change', checkValidity);

    btnAccept.addEventListener('click', () => {
        if (!btnAccept.disabled) {
            localStorage.setItem('creditguard_consent_v1', 'true');
            consentGate.classList.add('fade-out');
            setTimeout(() => {
                consentGate.style.display = 'none';
                document.body.style.overflow = '';
            }, 500); // match fade-out animation duration
        }
    });

    btnDecline.addEventListener('click', () => {
        document.body.innerHTML = `
            <div style="display:flex; flex-direction:column; align-items:center; justify-content:center; height:100vh; background:var(--color-bg-primary); color:var(--color-text-primary); font-family:var(--font-sans); text-align:center;">
                <h1 style="color:var(--color-rose);">Access Denied</h1>
                <p style="margin-top:20px; color:var(--color-text-secondary); max-width:500px;">You must accept the Terms & Conditions and Privacy Policy to access the Credit Risk Intelligence Platform.</p>
                <button onclick="location.reload()" style="margin-top:30px; padding:10px 20px; background:var(--color-blue); border:none; border-radius:var(--radius-md); color:white; cursor:pointer;">Go Back</button>
            </div>
        `;
    });
});

// Modal functions for Legal Docs
function openLegalModal(modalId) {
    document.getElementById('legal-modals').style.display = 'flex';
    document.querySelectorAll('.legal-modal').forEach(m => m.style.display = 'none');
    document.getElementById(modalId).style.display = 'block';
    
    // Add fade-in animation
    const modal = document.getElementById(modalId);
    modal.style.animation = 'none';
    modal.offsetHeight; // trigger reflow
    modal.style.animation = 'fadeInUp 0.3s ease forwards';
}

function closeLegalModal() {
    document.getElementById('legal-modals').style.display = 'none';
}
