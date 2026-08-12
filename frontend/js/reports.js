const API = (typeof API_BASE !== "undefined") ? API_BASE : "http://127.0.0.1:5000";

let riskChartInstance = null;
let addictionChartInstance = null;

document.addEventListener("DOMContentLoaded", () => {
    loadReportsData();
});

async function loadReportsData() {
    try {
        const response = await fetch(`${API}/reports/summary`);
        if (!response.ok) {
            console.error("Server error when loading reports summary:", response.status);
        }
        const data = await response.json();

        // Update Summary Cards
        if (data && data.summary) {
            document.getElementById("rptTotalPatients").innerText = data.summary.total_patients || 0;
            document.getElementById("rptAvgScore").innerText = (data.summary.avg_recovery_score || 0) + "%";
            document.getElementById("rptTotalAppointments").innerText = data.summary.total_appointments || 0;
        }

        // Count High + Critical
        const riskDist = (data && data.risk_distribution) ? data.risk_distribution : {};
        const highRiskCount = (riskDist.HIGH || 0) + (riskDist.CRITICAL || 0);
        document.getElementById("rptHighRiskCount").innerText = highRiskCount;

        // Render Charts
        renderRiskChart(riskDist);
        renderAddictionChart((data && data.addiction_distribution) ? data.addiction_distribution : {});

        // Render Table
        renderPatientTable((data && data.patient_summaries) ? data.patient_summaries : []);

    } catch (error) {
        console.error("Error loading reports data:", error);
    }
}

function renderRiskChart(riskData) {
    const riskCanvas = document.getElementById("riskChart");
    if (!riskCanvas) return;
    const ctx = riskCanvas.getContext("2d");

    if (riskChartInstance) {
        riskChartInstance.destroy();
    }

    const labels = ["CRITICAL", "HIGH", "MEDIUM", "LOW"];
    const values = labels.map(label => (riskData && riskData[label]) || 0);

    riskChartInstance = new Chart(ctx, {
        type: "doughnut",
        data: {
            labels: ["Critical Risk", "High Risk", "Medium Risk", "Low Risk"],
            datasets: [{
                data: values,
                backgroundColor: ["#dc3545", "#fd7e14", "#ffc107", "#198754"],
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { position: "bottom" }
            }
        }
    });
}

function renderAddictionChart(addictionData) {
    const addictionCanvas = document.getElementById("addictionChart");
    if (!addictionCanvas) return;
    const ctx = addictionCanvas.getContext("2d");

    if (addictionChartInstance) {
        addictionChartInstance.destroy();
    }

    const labels = Object.keys(addictionData || {});
    const values = Object.values(addictionData || {});

    addictionChartInstance = new Chart(ctx, {
        type: "bar",
        data: {
            labels: labels.length ? labels : ["None"],
            datasets: [{
                label: "Patients Count",
                data: values.length ? values : [0],
                backgroundColor: "#0d6efd",
                borderRadius: 6
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: { beginAtZero: true, precision: 0 }
            },
            plugins: {
                legend: { display: false }
            }
        }
    });
}

function renderPatientTable(patientSummaries) {
    const table = document.getElementById("reportsPatientTable");
    if (!table) return;

    table.innerHTML = "";

    if (!Array.isArray(patientSummaries) || patientSummaries.length === 0) {
        table.innerHTML = `<tr><td colspan="7" class="text-center text-muted">No patients recorded</td></tr>`;
        return;
    }

    patientSummaries.forEach(patient => {
        const row = document.createElement("tr");

        let badgeClass = "bg-secondary";
        const risk = String(patient.relapse_risk || "UNASSESSED").toUpperCase();
        if (risk === "CRITICAL") badgeClass = "bg-danger";
        else if (risk === "HIGH") badgeClass = "bg-warning text-dark";
        else if (risk === "MEDIUM") badgeClass = "bg-info text-dark";
        else if (risk === "LOW") badgeClass = "bg-success";

        row.innerHTML = `
            <td>${patient.patient_id}</td>
            <td><strong>${patient.full_name}</strong></td>
            <td><span class="badge bg-light text-dark border">${patient.addiction_type || 'N/A'}</span></td>
            <td>${patient.addiction_severity || 'N/A'}</td>
            <td><strong>${patient.last_recovery_score}${typeof patient.last_recovery_score === 'number' ? '%' : ''}</strong></td>
            <td><span class="badge ${badgeClass}">${patient.relapse_risk || 'UNASSESSED'}</span></td>
            <td>
                <button class="btn btn-outline-primary btn-sm" onclick="runAiAssessment(${patient.patient_id})">
                    <i class="bi bi-cpu"></i> Run AI Assessment
                </button>
            </td>
        `;

        table.appendChild(row);
    });
}

async function runAiAssessment(patientId) {
    try {
        const response = await fetch(`${API}/relapse/assess/${patientId}`, {
            method: "POST"
        });
        const data = await response.json();

        if (!response.ok) {
            alert(data.error || "Failed to generate AI assessment");
            return;
        }

        // Populate Modal
        document.getElementById("aiPatientName").innerText = (data.patient_name || "Patient") + " (ID: " + data.patient_id + ")";
        document.getElementById("aiRiskLevelText").innerText = (data.risk_level || "UNKNOWN") + " RISK";
        document.getElementById("aiRiskScoreText").innerText = (data.risk_score || 0) + "%";

        const banner = document.getElementById("riskBanner");
        banner.className = "d-flex align-items-center justify-content-between p-3 rounded mb-3 text-white ";
        if (data.risk_level === "CRITICAL") banner.classList.add("bg-danger");
        else if (data.risk_level === "HIGH") banner.classList.add("bg-warning", "text-dark");
        else if (data.risk_level === "MEDIUM") banner.classList.add("bg-info", "text-dark");
        else banner.classList.add("bg-success");

        // Triggers List
        const triggersList = document.getElementById("aiTriggersList");
        triggersList.innerHTML = "";
        (data.triggers || []).forEach(trig => {
            triggersList.innerHTML += `<li class="list-group-item list-group-item-warning"><i class="bi bi-exclamation-circle me-2"></i>${trig}</li>`;
        });

        // Recommendations List
        const recsList = document.getElementById("aiRecommendationsList");
        recsList.innerHTML = "";
        (data.recommendations || []).forEach(rec => {
            recsList.innerHTML += `<li class="list-group-item list-group-item-success"><i class="bi bi-check-circle me-2"></i>${rec}</li>`;
        });

        // Show Modal
        const modal = new bootstrap.Modal(document.getElementById("aiAssessmentModal"));
        modal.show();

        // Refresh table & charts
        loadReportsData();

    } catch (error) {
        console.error("Error executing AI assessment:", error);
        alert("Error running AI assessment.");
    }
}

function logout() {
    localStorage.removeItem("token");
    localStorage.removeItem("user");
    window.location.href = "login.html";
}

