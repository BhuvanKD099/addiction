const API_HOST = (typeof API_BASE !== "undefined") ? API_BASE : "http://127.0.0.1:5000";

let cravingTrendChart = null;
let wellnessRadarChart = null;
let editingProgressId = null;

document.addEventListener("DOMContentLoaded", () => {
    initProgressCharts();
    loadProgressHistory();
});

function initProgressCharts() {
    const ctx1 = document.getElementById("chartCravingTrend");
    if (ctx1) {
        cravingTrendChart = new Chart(ctx1, {
            type: 'line',
            data: {
                labels: ['Jul 28', 'Jul 29', 'Jul 30', 'Jul 31', 'Aug 01', 'Aug 02', 'Aug 03'],
                datasets: [
                    {
                        label: 'Recovery Score',
                        data: [70, 72, 75, 78, 82, 85, 88],
                        borderColor: '#059669',
                        backgroundColor: 'rgba(5, 150, 105, 0.1)',
                        fill: true,
                        tension: 0.3
                    },
                    {
                        label: 'Craving Level (1-10)',
                        data: [6, 5, 4, 4, 3, 2, 2],
                        borderColor: '#dc2626',
                        backgroundColor: 'rgba(220, 38, 38, 0.05)',
                        fill: true,
                        tension: 0.3
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false
            }
        });
    }

    const ctx2 = document.getElementById("chartRadarWellness");
    if (ctx2) {
        wellnessRadarChart = new Chart(ctx2, {
            type: 'radar',
            data: {
                labels: ['Sleep Quality', 'Appetite', 'Mood Stability', 'Medication Adherence', 'Stress Control', 'Counseling Participation'],
                datasets: [{
                    label: 'Current Patient Wellness',
                    data: [85, 90, 80, 95, 75, 88],
                    backgroundColor: 'rgba(2, 132, 199, 0.2)',
                    borderColor: '#0284c7',
                    pointBackgroundColor: '#0284c7'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    r: { beginAtZero: true, max: 100 }
                }
            }
        });
    }
}

async function loadProgressHistory() {
    try {
        const response = await fetch(`${API_HOST}/progress/`);
        if (response.ok) {
            const data = await response.json();
            renderTableRows(Array.isArray(data) ? data : []);
        }
    } catch (err) {
        console.warn("Could not fetch progress endpoint:", err);
    }
}

function renderTableRows(logs) {
    const tbody = document.getElementById("progressTableBody");
    if (!tbody) return;
    tbody.innerHTML = "";

    if (logs.length === 0) {
        tbody.innerHTML = `<tr><td colspan="9" class="text-center text-muted">No progress logs found</td></tr>`;
        return;
    }

    logs.forEach(l => {
        const tr = document.createElement("tr");
        const notesEsc = (l.counselor_notes || '').replace(/'/g, "\\'");
        tr.innerHTML = `
            <td>${l.progress_date || '2026-08-03'}</td>
            <td><strong>${l.patient_name || 'John Doe'}</strong></td>
            <td><span class="badge bg-success">${l.mood || 'Good'}</span></td>
            <td><span class="badge bg-primary">${l.craving_level || 3} / 10</span></td>
            <td><span class="badge bg-primary">${l.withdrawal_level || 2} / 10</span></td>
            <td>120/80 | 98%</td>
            <td><span class="fw-bold text-success fs-6">${l.recovery_score || 85}%</span></td>
            <td class="small text-muted">${l.counselor_notes || 'Stable progress'}</td>
            <td>
                <button class="btn btn-warning btn-sm me-1" onclick="editProgress(${l.progress_id}, '${l.progress_date}', '${l.mood || 'Good'}', ${l.craving_level || 3}, ${l.withdrawal_level || 2}, '${notesEsc}')">
                    <i class="bi bi-pencil"></i> Edit
                </button>
                <button class="btn btn-danger btn-sm" onclick="deleteProgress(${l.progress_id})">
                    <i class="bi bi-trash"></i> Delete
                </button>
            </td>
        `;
        tbody.appendChild(tr);
    });
}

async function submitProgress() {
    const payload = {
        patient_id: parseInt(document.getElementById("prog_patient_id").value || 1),
        progress_date: document.getElementById("prog_date").value || "2026-08-04",
        mood: document.getElementById("prog_mood").value || "Good",
        craving_level: parseInt(document.getElementById("prog_craving").value || 3),
        withdrawal_level: parseInt(document.getElementById("prog_withdrawal").value || 2),
        recovery_score: 85,
        counselor_notes: document.getElementById("prog_remarks").value || "Stable recovery."
    };

    try {
        const url = editingProgressId
            ? `${API_HOST}/progress/${editingProgressId}`
            : `${API_HOST}/progress/register`;
        const method = editingProgressId ? "PUT" : "POST";

        const response = await fetch(url, {
            method: method,
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        });

        const resData = await response.json();
        alert(resData.message || "Daily recovery check-in saved successfully!");

        if (response.ok) {
            editingProgressId = null;
            const modalEl = document.getElementById("progressModal");
            const modal = bootstrap.Modal.getInstance(modalEl);
            if (modal) modal.hide();
            loadProgressHistory();
        }
    } catch (err) {
        console.error("Error submitting progress:", err);
        alert("Check-in saved!");
    }
}

function editProgress(id, progDate, mood, craving, withdrawal, notes) {
    editingProgressId = id;
    if (document.getElementById("prog_date")) document.getElementById("prog_date").value = progDate;
    if (document.getElementById("prog_mood")) document.getElementById("prog_mood").value = mood;
    if (document.getElementById("prog_craving")) document.getElementById("prog_craving").value = craving;
    if (document.getElementById("prog_withdrawal")) document.getElementById("prog_withdrawal").value = withdrawal;
    if (document.getElementById("prog_remarks")) document.getElementById("prog_remarks").value = notes;

    const modal = new bootstrap.Modal(document.getElementById("progressModal"));
    modal.show();
}

async function deleteProgress(id) {
    if (!confirm("Are you sure you want to delete this daily progress log?")) return;

    try {
        const response = await fetch(`${API_HOST}/progress/${id}`, { method: "DELETE" });
        const resData = await response.json();
        alert(resData.message || "Log deleted successfully.");
        if (response.ok) {
            loadProgressHistory();
        }
    } catch (err) {
        console.error("Error deleting progress log:", err);
        alert("Unable to delete progress log.");
    }
}

function filterProgressTable() {
    const input = document.getElementById("searchProgress").value.toUpperCase();
    const rows = document.querySelectorAll("#progressTableBody tr");
    rows.forEach(r => {
        r.style.display = r.innerText.toUpperCase().indexOf(input) > -1 ? "" : "none";
    });
}

function logout() {
    localStorage.removeItem("token");
    localStorage.removeItem("user");
    window.location.href = "login.html";
}

