const API_HOST = (typeof API_BASE !== "undefined") ? API_BASE : "http://127.0.0.1:5000";

let recoveryChart = null;
let riskPieChart = null;

document.addEventListener("DOMContentLoaded", () => {
    initCharts();
    loadDashboardMetrics();
});

function switchUserRole(role) {
    const roleBtnAdmin = document.getElementById("roleBtnAdmin");
    const roleBtnDoctor = document.getElementById("roleBtnDoctor");
    const roleBtnCounselor = document.getElementById("roleBtnCounselor");
    const roleBtnPatient = document.getElementById("roleBtnPatient");

    [roleBtnAdmin, roleBtnDoctor, roleBtnCounselor, roleBtnPatient].forEach(btn => {
        if (btn) btn.classList.remove("active");
    });

    const activeText = document.getElementById("activeRoleText");
    const activeDesc = document.getElementById("activeRoleDesc");
    const title = document.getElementById("dashWelcomeTitle");

    if (role === "ADMIN") {
        if (roleBtnAdmin) roleBtnAdmin.classList.add("active");
        if (activeText) activeText.innerText = "ADMINISTRATOR";
        if (activeDesc) activeDesc.innerText = "Full system management access to doctors, counselors, patients, and hospital analytics.";
        if (title) title.innerText = "Executive Healthcare Dashboard";
    } else if (role === "DOCTOR") {
        if (roleBtnDoctor) roleBtnDoctor.classList.add("active");
        if (activeText) activeText.innerText = "DOCTOR PORTAL";
        if (activeDesc) activeDesc.innerText = "Clinical treatment management, prescriptions, daily observation notes & medical history.";
        if (title) title.innerText = "Physician Clinical Dashboard";
    } else if (role === "COUNSELOR") {
        if (roleBtnCounselor) roleBtnCounselor.classList.add("active");
        if (activeText) activeText.innerText = "COUNSELOR PORTAL";
        if (activeDesc) activeDesc.innerText = "Therapy session logging, CBT homework assignments, and psychological assessments.";
        if (title) title.innerText = "Counselor Rehabilitation Dashboard";
    } else if (role === "PATIENT") {
        if (roleBtnPatient) roleBtnPatient.classList.add("active");
        if (activeText) activeText.innerText = "PATIENT RECOVERY PORTAL";
        if (activeDesc) activeDesc.innerText = "Daily recovery tracking, habit check-ins, medication reminders & AI assessment.";
        if (title) title.innerText = "My Personal Recovery Center";
    }
}

function initCharts() {
    const ctx1 = document.getElementById("dashRecoveryChart");
    if (ctx1) {
        recoveryChart = new Chart(ctx1, {
            type: 'line',
            data: {
                labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
                datasets: [
                    {
                        label: 'Avg Recovery Score',
                        data: [65, 70, 72, 78, 80, 82, 85],
                        borderColor: '#059669',
                        backgroundColor: 'rgba(5, 150, 105, 0.1)',
                        fill: true,
                        tension: 0.3
                    },
                    {
                        label: 'Craving Intensity (1-10)',
                        data: [7, 6, 5, 4, 3, 3, 2],
                        borderColor: '#dc2626',
                        backgroundColor: 'rgba(220, 38, 38, 0.05)',
                        fill: true,
                        tension: 0.3
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { position: 'top' }
                },
                scales: {
                    y: { beginAtZero: true, max: 100 }
                }
            }
        });
    }

    const ctx2 = document.getElementById("dashRiskPieChart");
    if (ctx2) {
        riskPieChart = new Chart(ctx2, {
            type: 'doughnut',
            data: {
                labels: ['Low Risk', 'Moderate Risk', 'High Risk'],
                datasets: [{
                    data: [5, 2, 1],
                    backgroundColor: ['#059669', '#d97706', '#dc2626']
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { position: 'bottom' }
                }
            }
        });
    }
}

async function loadDashboardMetrics() {
    try {
        const response = await fetch(`${API_HOST}/reports/summary`);
        if (response.ok) {
            const data = await response.json();
            const s = data.summary || {};

            if (document.getElementById("statPatients")) {
                document.getElementById("statPatients").innerText = s.total_patients || 4;
            }
            if (document.getElementById("statRecoveryScore")) {
                document.getElementById("statRecoveryScore").innerText = `${s.avg_recovery_score || 75} / 100`;
            }
        }
    } catch (err) {
        console.warn("Using default client metrics for dashboard demonstration:", err);
    }
}

function logout() {
    localStorage.removeItem("token");
    localStorage.removeItem("user");
    window.location.href = "login.html";
}