const API_HOST = (typeof API_BASE !== "undefined") ? API_BASE : "http://127.0.0.1:5000";
let editingMedicationId = null;

document.addEventListener("DOMContentLoaded", () => {
    loadDropdowns();
    loadMedications();
});

async function loadDropdowns() {
    try {
        const pRes = await fetch(`${API_HOST}/patients/`);
        if (pRes.ok) {
            const patients = await pRes.json();
            const pSelect = document.getElementById("med_patient_id");
            if (pSelect && Array.isArray(patients) && patients.length > 0) {
                pSelect.innerHTML = "";
                patients.forEach(p => {
                    pSelect.innerHTML += `<option value="${p.patient_id}">${p.full_name} (ID: ${p.patient_id})</option>`;
                });
            }
        }

        const dRes = await fetch(`${API_HOST}/doctors/`);
        if (dRes.ok) {
            const doctors = await dRes.json();
            const dSelect = document.getElementById("med_doctor_id");
            if (dSelect && Array.isArray(doctors) && doctors.length > 0) {
                dSelect.innerHTML = "";
                doctors.forEach(d => {
                    dSelect.innerHTML += `<option value="${d.doctor_id}">${d.full_name} (${d.specialization || 'Doctor'})</option>`;
                });
            }
        }
    } catch (err) {
        console.warn("Could not populate dropdowns:", err);
    }
}

async function loadMedications() {
    try {
        const pSelect = document.getElementById("med_patient_id");
        const patientId = pSelect ? (pSelect.value || 1) : 1;

        const response = await fetch(`${API_HOST}/medications/patient/${patientId}`);
        if (response.ok) {
            const data = await response.json();
            const medsList = Array.isArray(data) ? data : (data.medications || []);
            renderMedTable(medsList);
        }
    } catch (err) {
        console.warn("Could not load medications API:", err);
    }
}

function renderMedTable(meds) {
    const tbody = document.getElementById("medicationTableBody");
    if (!tbody) return;
    tbody.innerHTML = "";

    if (!Array.isArray(meds) || meds.length === 0) {
        tbody.innerHTML = `<tr><td colspan="8" class="text-center text-muted">No prescriptions found for this patient</td></tr>`;
        return;
    }

    meds.forEach(m => {
        const tr = document.createElement("tr");
        const freqLower = (m.frequency || '').toLowerCase();
        const morn = freqLower.includes("morning") || freqLower.includes("daily") || freqLower.includes("once") || m.morning;
        const noon = freqLower.includes("noon") || freqLower.includes("afternoon") || freqLower.includes("three") || m.afternoon;
        const night = freqLower.includes("night") || freqLower.includes("evening") || freqLower.includes("twice") || freqLower.includes("three") || m.night;

        tr.innerHTML = `
            <td><strong class="text-navy">${m.medication_name}</strong><br/><small class="text-muted">${m.dosage}</small></td>
            <td>John Doe</td>
            <td>${morn ? '<span class="badge bg-success"><i class="bi bi-check-lg"></i> Scheduled</span>' : '<span class="badge bg-light text-muted">N/A</span>'}</td>
            <td>${noon ? '<span class="badge bg-warning text-dark"><i class="bi bi-clock"></i> Scheduled</span>' : '<span class="badge bg-light text-muted">N/A</span>'}</td>
            <td>${night ? '<span class="badge bg-secondary">Scheduled</span>' : '<span class="badge bg-light text-muted">N/A</span>'}</td>
            <td><span class="badge bg-success">${m.status || 'ACTIVE'}</span></td>
            <td class="small">${m.doctor_notes || m.frequency || 'Take as prescribed'}</td>
            <td>
                <button class="btn btn-warning btn-sm me-1" onclick="editMedication(${m.medication_id}, '${m.medication_name}', '${m.dosage}', '${m.status || 'ACTIVE'}')">
                    <i class="bi bi-pencil"></i> Edit
                </button>
                <button class="btn btn-danger btn-sm" onclick="deleteMedication(${m.medication_id})">
                    <i class="bi bi-trash"></i> Delete
                </button>
            </td>
        `;
        tbody.appendChild(tr);
    });
}

async function submitMedication() {
    const medName = document.getElementById("med_name").value.trim();
    const dosage = document.getElementById("med_dosage").value.trim();
    
    if (!medName || !dosage) {
        alert("Please enter Medication Name and Dosage.");
        return;
    }

    const patientId = parseInt(document.getElementById("med_patient_id").value || 1);
    const doctorId = parseInt(document.getElementById("med_doctor_id").value || 1);

    const morn = document.getElementById("med_morn") ? document.getElementById("med_morn").checked : true;
    const noon = document.getElementById("med_noon") ? document.getElementById("med_noon").checked : false;
    const night = document.getElementById("med_night") ? document.getElementById("med_night").checked : true;

    let freqParts = [];
    if (morn) freqParts.push("Morning");
    if (noon) freqParts.push("Afternoon");
    if (night) freqParts.push("Night");
    const frequency = freqParts.length > 0 ? freqParts.join(" & ") : "Daily";

    const payload = {
        patient_id: patientId,
        doctor_id: doctorId,
        medication_name: medName,
        dosage: dosage,
        frequency: frequency,
        start_date: document.getElementById("med_start").value || "2026-08-04",
        end_date: document.getElementById("med_end").value || "2026-11-04",
        status: "ACTIVE"
    };

    try {
        const url = editingMedicationId
            ? `${API_HOST}/medications/${editingMedicationId}`
            : `${API_HOST}/medications/`;
        const method = editingMedicationId ? "PUT" : "POST";

        const response = await fetch(url, {
            method: method,
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        });

        const resData = await response.json();

        if (response.ok) {
            alert(resData.message || "Prescription saved successfully!");
            editingMedicationId = null;
            const modalEl = document.getElementById("medicationModal");
            const modal = bootstrap.Modal.getInstance(modalEl);
            if (modal) modal.hide();

            // Clear inputs
            document.getElementById("med_name").value = "";
            document.getElementById("med_dosage").value = "";
            loadMedications();
        } else {
            alert(resData.message || resData.error || "Unable to save prescription.");
        }
    } catch (err) {
        console.error("Error submitting medication:", err);
        alert("Unable to save prescription: " + err.message);
    }
}

function editMedication(id, name, dosage, status) {
    editingMedicationId = id;
    document.getElementById("med_name").value = name;
    document.getElementById("med_dosage").value = dosage;

    const modal = new bootstrap.Modal(document.getElementById("medicationModal"));
    modal.show();
}

async function deleteMedication(id) {
    if (!confirm("Are you sure you want to delete this medication prescription?")) return;

    try {
        const response = await fetch(`${API_HOST}/medications/${id}`, { method: "DELETE" });
        const result = await response.json();
        alert(result.message || "Prescription deleted.");
        if (response.ok) {
            loadMedications();
        }
    } catch (err) {
        console.error("Error deleting medication:", err);
        alert("Unable to delete prescription.");
    }
}

function logout() {
    localStorage.removeItem("token");
    localStorage.removeItem("user");
    window.location.href = "login.html";
}


