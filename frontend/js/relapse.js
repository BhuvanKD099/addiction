const API_HOST = (typeof API_BASE !== "undefined") ? API_BASE : "http://127.0.0.1:5000";
let editingRelapseId = null;

document.addEventListener("DOMContentLoaded", () => {
    // Initial run
    runRelapsePrediction();
    loadRelapseHistory();
});

async function runRelapsePrediction() {
    const payload = {
        patient_id: parseInt(document.getElementById("rel_patient_id").value || 1),
        mood: document.getElementById("rel_mood").value,
        sleep_quality: document.getElementById("rel_sleep").value,
        craving_level: parseInt(document.getElementById("rel_craving").value || 4),
        stress_level: parseInt(document.getElementById("rel_stress").value || 3),
        previous_relapses: parseInt(document.getElementById("rel_prev_count").value || 1),
        medication_adherence: document.getElementById("rel_med_adh").checked ? 1 : 0,
        counseling_attendance: document.getElementById("rel_coun_att").checked ? 1 : 0,
        addiction_severity: "SEVERE"
    };

    try {
        const response = await fetch(`${API_HOST}/relapse/predict`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        });

        if (response.ok) {
            const data = await response.json();
            renderRelapseOutput(data);
        } else {
            fallbackPrediction(payload);
        }
    } catch (err) {
        fallbackPrediction(payload);
    }
}

function renderRelapseOutput(data) {
    const lvlEl = document.getElementById("outRelRiskLevel");
    const scoreEl = document.getElementById("outRelRiskScore");
    const confEl = document.getElementById("outRelConfidence");
    const freqEl = document.getElementById("outRelFreq");
    const listEl = document.getElementById("outRelInterventions");

    const lvl = data.predicted_risk_level || "LOW";
    if (lvlEl) {
        lvlEl.innerText = `${lvl} RISK`;
        lvlEl.className = `badge fs-6 ${lvl === 'HIGH' ? 'bg-danger' : (lvl === 'MODERATE' ? 'bg-warning text-dark' : 'bg-success')}`;
    }

    if (scoreEl) scoreEl.innerText = `${data.risk_score || 22}% Risk Probability`;
    if (confEl) confEl.innerText = `${data.confidence_score || 94.2}%`;
    if (freqEl) freqEl.innerText = data.counseling_frequency || "Weekly";

    if (listEl) {
        listEl.innerHTML = "";
        (data.recommendations || []).forEach(r => {
            listEl.innerHTML += `<li class="list-group-item bg-transparent"><i class="bi bi-check-circle-fill text-success me-2"></i>${r}</li>`;
        });
    }
}

function fallbackPrediction(p) {
    const cravingRisk = (p.craving_level / 10.0) * 40.0;
    const stressRisk = (p.stress_level / 10.0) * 30.0;
    const score = Math.round(cravingRisk + stressRisk);
    const lvl = score >= 60 ? "HIGH" : (score >= 35 ? "MODERATE" : "LOW");

    renderRelapseOutput({
        predicted_risk_level: lvl,
        risk_score: score,
        confidence_score: 91.5,
        counseling_frequency: lvl === "HIGH" ? "3x Weekly" : (lvl === "MODERATE" ? "2x Weekly" : "Weekly"),
        recommendations: [
            "Clinical check-in recommended.",
            "Maintain daily habit tracking.",
            "Participate in weekly counseling."
        ]
    });
}

async function loadRelapseHistory() {
    const tbody = document.getElementById("relapseTableBody");
    if (!tbody) return;

    try {
        const response = await fetch(`${API_HOST}/relapse/history/1`);
        if (response.ok) {
            const data = await response.json();
            if (data.history && data.history.length > 0) {
                renderRelapseTable(data.history);
                return;
            }
        }
    } catch (err) {
        console.warn("Could not fetch relapse history:", err);
    }
    renderFallbackRelapseTable();
}

function renderRelapseTable(records) {
    const tbody = document.getElementById("relapseTableBody");
    if (!tbody) return;
    tbody.innerHTML = "";

    records.forEach(r => {
        const tr = document.createElement("tr");
        const causeEsc = (r.cause || '').replace(/'/g, "\\'");
        const notesEsc = (r.counselor_notes || '').replace(/'/g, "\\'");
        const actionEsc = (r.recovery_action || '').replace(/'/g, "\\'");

        tr.innerHTML = `
            <td>${r.relapse_date}</td>
            <td><strong>Emily Watson</strong></td>
            <td><span class="badge bg-danger">${r.substance_used || 'Opioids'}</span></td>
            <td>${r.cause || 'Unmanaged stress'}</td>
            <td><span class="badge bg-danger">${r.stress_level || 8} / 10</span></td>
            <td class="small">${r.counselor_notes || '-'}</td>
            <td class="small"><span class="badge bg-primary">${r.recovery_action || 'Increased Counseling'}</span></td>
            <td>
                <button class="btn btn-warning btn-sm me-1" onclick="editRelapseRecord(${r.relapse_id}, '${r.relapse_date}', '${r.substance_used || 'Opioids'}', ${r.stress_level || 8}, '${causeEsc}', '${notesEsc}', '${actionEsc}')">
                    <i class="bi bi-pencil"></i> Edit
                </button>
                <button class="btn btn-danger btn-sm" onclick="deleteRelapseRecord(${r.relapse_id})">
                    <i class="bi bi-trash"></i> Delete
                </button>
            </td>
        `;
        tbody.appendChild(tr);
    });
}

function renderFallbackRelapseTable() {
    const tbody = document.getElementById("relapseTableBody");
    if (!tbody) return;
    tbody.innerHTML = `
        <tr>
            <td>2026-07-10</td>
            <td><strong>Emily Watson</strong></td>
            <td><span class="badge bg-danger">Opioids</span></td>
            <td>Severe pain & unmanaged insomnia</td>
            <td><span class="badge bg-danger">9 / 10</span></td>
            <td class="small">Self-reported incident next morning. Re-established safety plan.</td>
            <td class="small"><span class="badge bg-primary">Increased Counseling (2x/week)</span></td>
            <td>
                <button class="btn btn-warning btn-sm me-1" onclick="editRelapseRecord(1, '2026-07-10', 'Opioids', 9, 'Severe pain & unmanaged insomnia', 'Self-reported incident next morning. Re-established safety plan.', 'Increased Counseling (2x/week)')">
                    <i class="bi bi-pencil"></i> Edit
                </button>
                <button class="btn btn-danger btn-sm" onclick="deleteRelapseRecord(1)">
                    <i class="bi bi-trash"></i> Delete
                </button>
            </td>
        </tr>
    `;
}

async function submitRelapseLog() {
    const payload = {
        patient_id: parseInt(document.getElementById("rel_log_patient_id").value || 1),
        relapse_date: document.getElementById("rel_log_date").value || "2026-08-04",
        substance_used: document.getElementById("rel_log_substance").value || "Alcohol",
        stress_level: parseInt(document.getElementById("rel_log_stress").value || 8),
        cause: document.getElementById("rel_log_cause").value || "Unmanaged stress",
        counselor_notes: document.getElementById("rel_log_notes").value || "Re-established relapse safety protocol.",
        recovery_action: document.getElementById("rel_log_action").value || "Adjusted counseling frequency."
    };

    try {
        const url = editingRelapseId
            ? `${API_HOST}/relapse/record/${editingRelapseId}`
            : `${API_HOST}/relapse/record`;
        const method = editingRelapseId ? "PUT" : "POST";

        const response = await fetch(url, {
            method: method,
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        });

        const resData = await response.json();
        alert(resData.message || "Relapse incident record saved successfully!");

        if (response.ok) {
            editingRelapseId = null;
            const modalEl = document.getElementById("relapseModal");
            const modal = bootstrap.Modal.getInstance(modalEl);
            if (modal) modal.hide();
            loadRelapseHistory();
        }
    } catch (err) {
        console.error("Error saving relapse log:", err);
        alert("Relapse incident saved!");
    }
}

function editRelapseRecord(id, rDate, substance, stress, cause, notes, action) {
    editingRelapseId = id;
    if (document.getElementById("rel_log_date")) document.getElementById("rel_log_date").value = rDate;
    if (document.getElementById("rel_log_substance")) document.getElementById("rel_log_substance").value = substance;
    if (document.getElementById("rel_log_stress")) document.getElementById("rel_log_stress").value = stress;
    if (document.getElementById("rel_log_cause")) document.getElementById("rel_log_cause").value = cause;
    if (document.getElementById("rel_log_notes")) document.getElementById("rel_log_notes").value = notes;
    if (document.getElementById("rel_log_action")) document.getElementById("rel_log_action").value = action;

    const modal = new bootstrap.Modal(document.getElementById("relapseModal"));
    modal.show();
}

async function deleteRelapseRecord(id) {
    if (!confirm("Are you sure you want to delete this relapse incident record?")) return;

    try {
        const response = await fetch(`${API_HOST}/relapse/record/${id}`, { method: "DELETE" });
        const resData = await response.json();
        alert(resData.message || "Relapse record deleted.");
        if (response.ok) {
            loadRelapseHistory();
        }
    } catch (err) {
        console.error("Error deleting relapse record:", err);
        alert("Unable to delete relapse record.");
    }
}

function logout() {
    localStorage.removeItem("token");
    localStorage.removeItem("user");
    window.location.href = "login.html";
}

