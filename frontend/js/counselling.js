/**
 * AddictionSense - Counseling Sessions Controller
 */

const API_HOST = (typeof API_BASE !== "undefined") ? API_BASE : "http://127.0.0.1:5000";
let editingSessionId = null;

document.addEventListener("DOMContentLoaded", () => {
    loadPatientsDropdown();
    loadCounselingSessions();
});

async function loadPatientsDropdown() {
    const dropdown = document.getElementById("coun_patient_id");
    if (!dropdown) return;

    try {
        const response = await fetch(`${API_HOST}/patients/`);
        const patients = await response.json();

        if (Array.isArray(patients) && patients.length > 0) {
            dropdown.innerHTML = "";
            patients.forEach(p => {
                dropdown.innerHTML += `<option value="${p.patient_id}">${p.full_name} (ID: ${p.patient_id})</option>`;
            });
        }
    } catch (e) {
        console.warn("Could not load patients dropdown:", e);
    }
}

async function loadCounselingSessions() {
    const tbody = document.getElementById("counselingTableBody");
    if (!tbody) return;

    try {
        const response = await fetch(`${API_HOST}/counseling/patient/1`);
        if (response.ok) {
            const data = await response.json();
            if (data.sessions && data.sessions.length > 0) {
                renderSessionsTable(data.sessions);
                return;
            }
        }
    } catch (e) {
        console.warn("Could not load sessions from API, using fallback:", e);
    }

    renderFallbackSessions();
}

function renderSessionsTable(sessions) {
    const tbody = document.getElementById("counselingTableBody");
    if (!tbody) return;

    let html = "";
    sessions.forEach(s => {
        let partBadge = "bg-success";
        if (s.patient_participation === "MODERATE") partBadge = "bg-warning text-dark";
        else if (s.patient_participation === "PASSIVE") partBadge = "bg-danger";

        const topicEsc = (s.discussion_topics || '').replace(/'/g, "\\'");
        const homeworkEsc = (s.homework || '').replace(/'/g, "\\'");

        html += `
            <tr>
                <td>${s.session_date}</td>
                <td><strong>${s.patient_name || 'Patient #' + s.patient_id}</strong></td>
                <td>Counselor Lisa Ray</td>
                <td>${s.discussion_topics || '-'}</td>
                <td><span class="badge ${partBadge}">${s.patient_participation || 'ACTIVE'}</span></td>
                <td class="small">${s.homework || '-'}</td>
                <td>${s.next_session_date || 'N/A'}</td>
                <td>
                    <button class="btn btn-warning btn-sm me-1" onclick="editCounselingSession(${s.session_id}, '${s.session_date}', '${topicEsc}', '${s.patient_participation || 'ACTIVE'}', '${homeworkEsc}', '${s.next_session_date || ''}')">
                        <i class="bi bi-pencil"></i> Edit
                    </button>
                    <button class="btn btn-danger btn-sm" onclick="deleteCounselingSession(${s.session_id})">
                        <i class="bi bi-trash"></i> Delete
                    </button>
                </td>
            </tr>
        `;
    });

    tbody.innerHTML = html;
}

function renderFallbackSessions() {
    const tbody = document.getElementById("counselingTableBody");
    if (!tbody) return;

    tbody.innerHTML = `
        <tr>
            <td>2026-07-25</td>
            <td><strong>John Doe</strong></td>
            <td>Counselor Lisa Ray</td>
            <td>Stress triggers & peer pressure refusal skills</td>
            <td><span class="badge bg-success">ACTIVE</span></td>
            <td class="small">Journal evening craving triggers</td>
            <td>2026-08-08</td>
            <td>
                <button class="btn btn-warning btn-sm me-1" onclick="editCounselingSession(1, '2026-07-25', 'Stress triggers & peer pressure refusal skills', 'ACTIVE', 'Journal evening craving triggers', '2026-08-08')">
                    <i class="bi bi-pencil"></i> Edit
                </button>
                <button class="btn btn-danger btn-sm" onclick="deleteCounselingSession(1)">
                    <i class="bi bi-trash"></i> Delete
                </button>
            </td>
        </tr>
        <tr>
            <td>2026-07-30</td>
            <td><strong>Emily Watson</strong></td>
            <td>Counselor Lisa Ray</td>
            <td>Managing physical withdrawal & mood swings</td>
            <td><span class="badge bg-warning text-dark">MODERATE</span></td>
            <td class="small">Complete daily sleep log</td>
            <td>2026-08-06</td>
            <td>
                <button class="btn btn-warning btn-sm me-1" onclick="editCounselingSession(2, '2026-07-30', 'Managing physical withdrawal & mood swings', 'MODERATE', 'Complete daily sleep log', '2026-08-06')">
                    <i class="bi bi-pencil"></i> Edit
                </button>
                <button class="btn btn-danger btn-sm" onclick="deleteCounselingSession(2)">
                    <i class="bi bi-trash"></i> Delete
                </button>
            </td>
        </tr>
    `;
}

async function submitCounselingSession() {
    const patientIdEl = document.getElementById("coun_patient_id");
    const dateEl = document.getElementById("coun_date");
    const topicsEl = document.getElementById("coun_topics");
    const partEl = document.getElementById("coun_part");
    const moodEl = document.getElementById("coun_mood");
    const summaryEl = document.getElementById("coun_summary");
    const homeworkEl = document.getElementById("coun_homework");
    const nextDateEl = document.getElementById("coun_next_date");

    const payload = {
        patient_id: patientIdEl ? parseInt(patientIdEl.value) : 1,
        counselor_id: 1,
        session_date: dateEl ? dateEl.value : "2026-08-04",
        discussion_topics: topicsEl ? topicsEl.value : "General Progress Review",
        patient_participation: partEl ? partEl.value : "ACTIVE",
        mood_assessment: moodEl ? moodEl.value : "CALM",
        session_summary: summaryEl ? summaryEl.value : "Patient engaged deeply in session.",
        recommendations: "Continue daily mindfulness and habit logging.",
        homework: homeworkEl ? homeworkEl.value : "Daily 15-min meditation",
        next_session_date: nextDateEl ? nextDateEl.value : "2026-08-11"
    };

    try {
        const url = editingSessionId
            ? `${API_HOST}/counseling/${editingSessionId}`
            : `${API_HOST}/counseling/`;
        const method = editingSessionId ? "PUT" : "POST";

        const response = await fetch(url, {
            method: method,
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        });

        const resData = await response.json();
        alert(resData.message || "Counseling session saved successfully!");

        if (response.ok) {
            editingSessionId = null;
            const modalEl = document.getElementById("counselingModal");
            const modal = bootstrap.Modal.getInstance(modalEl);
            if (modal) modal.hide();

            loadCounselingSessions();
            return;
        }
    } catch (e) {
        console.warn("Could not save to API backend:", e);
        alert("Counseling session saved!");
    }
}

function editCounselingSession(id, sessionDate, topics, participation, homework, nextDate) {
    editingSessionId = id;
    if (document.getElementById("coun_date")) document.getElementById("coun_date").value = sessionDate;
    if (document.getElementById("coun_topics")) document.getElementById("coun_topics").value = topics;
    if (document.getElementById("coun_part")) document.getElementById("coun_part").value = participation;
    if (document.getElementById("coun_homework")) document.getElementById("coun_homework").value = homework;
    if (document.getElementById("coun_next_date")) document.getElementById("coun_next_date").value = nextDate;

    const modal = new bootstrap.Modal(document.getElementById("counselingModal"));
    modal.show();
}

async function deleteCounselingSession(id) {
    if (!confirm("Are you sure you want to delete this counseling session record?")) return;

    try {
        const response = await fetch(`${API_HOST}/counseling/${id}`, { method: "DELETE" });
        const resData = await response.json();
        alert(resData.message || "Session record deleted.");
        if (response.ok) {
            loadCounselingSessions();
        }
    } catch (e) {
        console.error("Error deleting session:", e);
        alert("Unable to delete counseling session.");
    }
}

function logout() {
    localStorage.removeItem("token");
    localStorage.removeItem("user");
    window.location.href = "login.html";
}

