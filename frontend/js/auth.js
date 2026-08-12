/* ==========================================
   AddictionSense - Professional Auth Script
   ========================================== */

// Helper to show floating Toast Notifications
function showToast(title, message, type = 'info') {
    let container = document.querySelector('.toast-container');
    if (!container) {
        container = document.createElement('div');
        container.className = 'toast-container';
        document.body.appendChild(container);
    }

    const toast = document.createElement('div');
    toast.className = `custom-toast toast-${type}`;
    
    let iconClass = 'fa-circle-info';
    if (type === 'success') iconClass = 'fa-circle-check';
    if (type === 'error') iconClass = 'fa-circle-exclamation';
    if (type === 'warning') iconClass = 'fa-triangle-exclamation';

    toast.innerHTML = `
        <i class="fa-solid ${iconClass} toast-icon"></i>
        <div class="toast-content">
            <div class="toast-title">${title}</div>
            <div class="toast-message">${message}</div>
        </div>
        <button class="toast-close" onclick="this.parentElement.remove()">
            <i class="fa-solid fa-xmark"></i>
        </button>
    `;

    container.appendChild(toast);

    // Trigger animation
    setTimeout(() => toast.classList.add('show'), 10);

    // Auto dismiss after 4.5 seconds
    setTimeout(() => {
        toast.classList.remove('show');
        setTimeout(() => toast.remove(), 400);
    }, 4500);
}

// Toggle password visibility (show / hide)
function togglePasswordVisibility(inputId, btn) {
    const input = document.getElementById(inputId);
    const icon = btn.querySelector('i');
    if (!input || !icon) return;

    if (input.type === 'password') {
        input.type = 'text';
        icon.className = 'fa-regular fa-eye-slash';
    } else {
        input.type = 'password';
        icon.className = 'fa-regular fa-eye';
    }
}

// Check Password Strength (Signup Page)
function updatePasswordStrength() {
    const passwordInput = document.getElementById('password');
    const strengthBar = document.getElementById('strengthBar');
    const strengthLabel = document.getElementById('strengthLabel');
    
    if (!passwordInput || !strengthBar || !strengthLabel) return;

    const val = passwordInput.value;

    // Rules check
    const lenRule = val.length >= 8;
    const numRule = /[0-9]/.test(val);
    const upperRule = /[A-Z]/.test(val);
    const specialRule = /[^A-Za-z0-9]/.test(val);

    // Update rule items visuals if present
    const ruleLen = document.getElementById('ruleLen');
    const ruleNum = document.getElementById('ruleNum');
    const ruleUpper = document.getElementById('ruleUpper');
    const ruleSpecial = document.getElementById('ruleSpecial');

    if (ruleLen) toggleRuleClass(ruleLen, lenRule);
    if (ruleNum) toggleRuleClass(ruleNum, numRule);
    if (ruleUpper) toggleRuleClass(ruleUpper, upperRule);
    if (ruleSpecial) toggleRuleClass(ruleSpecial, specialRule);

    if (val.length === 0) {
        strengthBar.className = 'strength-bar';
        strengthBar.style.width = '0%';
        strengthLabel.textContent = 'Password Strength';
        strengthLabel.style.color = 'var(--text-muted)';
        return;
    }

    let score = 0;
    if (lenRule) score += 1;
    if (numRule) score += 1;
    if (upperRule) score += 1;
    if (specialRule) score += 1;

    if (score <= 1) {
        strengthBar.className = 'strength-bar weak';
        strengthLabel.textContent = 'Weak Password';
        strengthLabel.style.color = 'var(--danger-red)';
    } else if (score <= 3) {
        strengthBar.className = 'strength-bar medium';
        strengthLabel.textContent = 'Medium Strength';
        strengthLabel.style.color = 'var(--accent-amber)';
    } else {
        strengthBar.className = 'strength-bar strong';
        strengthLabel.textContent = 'Strong Password';
        strengthLabel.style.color = 'var(--recovery-green)';
    }
}

function toggleRuleClass(el, isValid) {
    const icon = el.querySelector('i');
    if (isValid) {
        el.classList.add('valid');
        if (icon) icon.className = 'fa-solid fa-check';
    } else {
        el.classList.remove('valid');
        if (icon) icon.className = 'fa-solid fa-circle';
    }
}

// User Login Logic
async function login(event) {
    if (event) event.preventDefault();

    const emailEl = document.getElementById("email");
    const passwordEl = document.getElementById("password");
    const loginBtn = document.getElementById("loginBtn");
    const btnText = document.getElementById("btnText");
    const spinner = document.getElementById("btnSpinner");

    const email = emailEl ? emailEl.value.trim() : '';
    const password = passwordEl ? passwordEl.value : '';

    if (!email) {
        showToast("Missing Email", "Please enter your registered email address.", "warning");
        if (emailEl) emailEl.focus();
        return;
    }

    if (!password) {
        showToast("Missing Password", "Please enter your account password.", "warning");
        if (passwordEl) passwordEl.focus();
        return;
    }

    // UI Loading State
    if (loginBtn) loginBtn.disabled = true;
    if (btnText) btnText.textContent = "Signing In...";
    if (spinner) spinner.style.display = "inline-block";

    try {
        const result = await apiRequest(
            "/auth/login",
            "POST",
            { email: email, password: password }
        );

        if (result && result.access_token) {
            localStorage.setItem("token", result.access_token);
            localStorage.setItem("user", JSON.stringify(result.user || { email, role: 'patient' }));

            showToast("Welcome Back!", "Login successful. Redirecting to dashboard...", "success");

            setTimeout(() => {
                window.location.href = "dashboard.html";
            }, 1200);
        } else {
            const errorMsg = (result && result.error) ? result.error : "Invalid email or password";
            showToast("Authentication Failed", errorMsg, "error");
        }
    } catch (err) {
        console.error("Login Error:", err);
        showToast("Connection Error", "Unable to connect to the authentication server. Please verify backend is running.", "error");
    } finally {
        if (loginBtn) loginBtn.disabled = false;
        if (btnText) btnText.textContent = "Sign In";
        if (spinner) spinner.style.display = "none";
    }
}

// User Registration Logic
async function register(event) {
    if (event) event.preventDefault();

    const nameEl = document.getElementById("fullName");
    const emailEl = document.getElementById("email");
    const passwordEl = document.getElementById("password");
    const confirmPasswordEl = document.getElementById("confirmPassword");
    const termsEl = document.getElementById("termsCheck");
    
    const signupBtn = document.getElementById("signupBtn");
    const btnText = document.getElementById("btnText");
    const spinner = document.getElementById("btnSpinner");

    const fullName = nameEl ? nameEl.value.trim() : '';
    const email = emailEl ? emailEl.value.trim() : '';
    const password = passwordEl ? passwordEl.value : '';
    const confirmPassword = confirmPasswordEl ? confirmPasswordEl.value : '';
    
    // Get Selected Role
    const roleRadio = document.querySelector('input[name="role"]:checked');
    const role = roleRadio ? roleRadio.value : 'patient';

    if (!fullName) {
        showToast("Missing Name", "Please enter your full name.", "warning");
        if (nameEl) nameEl.focus();
        return;
    }

    if (!email || !email.includes('@')) {
        showToast("Invalid Email", "Please enter a valid email address.", "warning");
        if (emailEl) emailEl.focus();
        return;
    }

    if (!password || password.length < 6) {
        showToast("Weak Password", "Password must be at least 6 characters long.", "warning");
        if (passwordEl) passwordEl.focus();
        return;
    }

    if (password !== confirmPassword) {
        showToast("Password Mismatch", "Passwords do not match. Please re-enter.", "warning");
        if (confirmPasswordEl) confirmPasswordEl.focus();
        return;
    }

    if (termsEl && !termsEl.checked) {
        showToast("Terms Required", "Please agree to the Terms of Service & Privacy Policy.", "warning");
        return;
    }

    // UI Loading State
    if (signupBtn) signupBtn.disabled = true;
    if (btnText) btnText.textContent = "Creating Account...";
    if (spinner) spinner.style.display = "inline-block";

    try {
        const result = await apiRequest(
            "/auth/register",
            "POST",
            {
                full_name: fullName,
                email: email,
                password: password,
                role: role
            }
        );

        if (result && (result.message || result.user_id)) {
            showToast("Account Created!", "Registration successful. You can now log in.", "success");

            setTimeout(() => {
                window.location.href = "login.html";
            }, 1500);
        } else {
            const errorMsg = (result && result.error) ? result.error : "Registration failed. Please try again.";
            showToast("Registration Failed", errorMsg, "error");
        }
    } catch (err) {
        console.error("Register Error:", err);
        showToast("Connection Error", "Unable to connect to the authentication server. Please verify backend is running.", "error");
    } finally {
        if (signupBtn) signupBtn.disabled = false;
        if (btnText) btnText.textContent = "Create Account";
        if (spinner) spinner.style.display = "none";
    }
}

// Auto Attach Listeners on DOM Ready
document.addEventListener("DOMContentLoaded", () => {
    const passwordInput = document.getElementById('password');
    if (passwordInput && document.getElementById('strengthBar')) {
        passwordInput.addEventListener('input', updatePasswordStrength);
    }
});