const API = (typeof API_BASE !== "undefined") ? API_BASE : "http://127.0.0.1:5000";

let patients = [];
let editingPatientId = null;

document.addEventListener("DOMContentLoaded", () => {
    loadDoctorsDropdown();
    loadPatients();

    const saveBtn = document.getElementById("saveButton");
    if (saveBtn) {
        saveBtn.addEventListener("click", savePatient);
    }

    const searchInput = document.getElementById("searchPatient");
    if (searchInput) {
        searchInput.addEventListener("input", searchPatient);
    }
});

function setSelectValue(selectId, value, defaultValue) {
    const el = document.getElementById(selectId);
    if (!el) return;
    const targetVal = String(value || defaultValue || "").trim().toUpperCase();
    let found = false;

    for (let i = 0; i < el.options.length; i++) {
        const opt = el.options[i];
        if (opt.value.trim().toUpperCase() === targetVal || opt.text.trim().toUpperCase().includes(targetVal)) {
            el.selectedIndex = i;
            found = true;
            break;
        }
    }

    if (!found && el.options.length > 0) {
        el.selectedIndex = 0;
    }
}

async function loadDoctorsDropdown() {
    const dropdown = document.getElementById("doctor_id");
    if (!dropdown) return;

    try {
        const response = await fetch(`${API}/doctors/`);
        const doctors = await response.json();

        if (Array.isArray(doctors) && doctors.length > 0) {
            dropdown.innerHTML = "";
            doctors.forEach(d => {
                dropdown.innerHTML += `<option value="${d.doctor_id}">${d.full_name} (${d.specialization || 'Doctor'})</option>`;
            });
        }
    } catch (e) {
        console.warn("Could not load doctors dropdown:", e);
    }
}

async function loadPatients() {
    try {
        const response = await fetch(`${API}/patients/`);
        patients = await response.json();
        if (!Array.isArray(patients)) patients = [];
        displayPatients(patients);
    } catch (error) {
        console.error(error);
        alert("Unable to load patients.");
    }
}

function displayPatients(data) {
    const table = document.getElementById("patientTable");
    if (!table) return;

    table.innerHTML = "";

    if (!Array.isArray(data) || data.length === 0) {
        table.innerHTML = `<tr><td colspan="11" class="text-center text-muted">No patients found</td></tr>`;
        return;
    }

    data.forEach(patient => {
        const row = document.createElement("tr");

        row.innerHTML = `
            <td>${patient.patient_id}</td>
            <td><strong>${patient.full_name}</strong></td>
            <td>${patient.email}</td>
            <td>${patient.doctor_name || 'Dr. Sarah Jenkins'}</td>
            <td>${patient.age}</td>
            <td>${patient.gender}</td>
            <td>${patient.phone}</td>
            <td>${patient.addiction_type}</td>
            <td><span class="badge ${patient.addiction_severity === 'SEVERE' ? 'bg-danger' : (patient.addiction_severity === 'MODERATE' ? 'bg-warning text-dark' : 'bg-success')}">${patient.addiction_severity}</span></td>
            <td>${patient.admission_date}</td>
            <td>
                <button class="btn btn-warning btn-sm edit-btn me-1" data-id="${patient.patient_id}">
                    <i class="bi bi-pencil"></i> Edit
                </button>
                <button class="btn btn-danger btn-sm delete-btn" data-id="${patient.patient_id}">
                    <i class="bi bi-trash"></i> Delete
                </button>
            </td>
        `;

        table.appendChild(row);
    });

    document.querySelectorAll(".edit-btn").forEach(button => {
        button.addEventListener("click", () => editPatient(button.dataset.id));
    });

    document.querySelectorAll(".delete-btn").forEach(button => {
        button.addEventListener("click", () => deletePatient(button.dataset.id));
    });
}

async function savePatient() {
    const docSelect = document.getElementById("doctor_id");
    const docVal = (docSelect && docSelect.value) ? parseInt(docSelect.value) : 1;

    const addTypeEl = document.getElementById("addiction_type");
    const addTypeVal = (addTypeEl && addTypeEl.value) ? addTypeEl.value : "Alcohol";

    const addSevEl = document.getElementById("addiction_severity");
    const addSevVal = (addSevEl && addSevEl.value) ? addSevEl.value : "SEVERE";

    const genderEl = document.getElementById("gender");
    const genderVal = (genderEl && genderEl.value) ? genderEl.value : "MALE";

    let admDate = document.getElementById("admission_date").value;
    if (!admDate) admDate = "2026-06-01";

    const patient = {
        full_name: document.getElementById("full_name").value.trim() || "Patient",
        email: document.getElementById("email").value.trim() || "patient@recovery.org",
        password: document.getElementById("password").value || "password123",
        doctor_id: docVal,
        age: parseInt(document.getElementById("age").value || 30),
        gender: genderVal,
        phone: document.getElementById("phone").value.trim() || "+1 555-0000",
        address: document.getElementById("address").value.trim() || "124 Main St",
        emergency_contact: document.getElementById("emergency_contact").value.trim() || "+1 555-9999",
        admission_date: admDate,
        addiction_type: addTypeVal,
        addiction_severity: addSevVal
    };

    try {
        const url = editingPatientId
            ? `${API}/patients/${editingPatientId}`
            : `${API}/patients/register`;

        const method = editingPatientId ? "PUT" : "POST";

        const response = await fetch(url, {
            method: method,
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(patient)
        });

        const result = await response.json();

        if (response.ok) {
            alert(result.message || "Patient details saved successfully.");
            const modalEl = document.getElementById("patientModal");
            const modal = bootstrap.Modal.getInstance(modalEl);
            if (modal) modal.hide();

            editingPatientId = null;
            document.getElementById("saveButton").textContent = "Register Patient";
            loadPatients();
        } else {
            alert(result.message || result.error || "Unable to save patient.");
        }
    } catch (error) {
        console.error(error);
        alert("Unable to save patient: " + error.message);
    }
}

function searchPatient() {
    const value = document.getElementById("searchPatient").value.toLowerCase();
    const filtered = patients.filter(patient =>
        (patient.full_name && patient.full_name.toLowerCase().includes(value)) ||
        (patient.email && patient.email.toLowerCase().includes(value)) ||
        (patient.addiction_type && patient.addiction_type.toLowerCase().includes(value))
    );
    displayPatients(filtered);
}

async function deletePatient(patientId) {
    if (!confirm("Are you sure you want to delete this patient record?")) return;

    try {
        const response = await fetch(`${API}/patients/${patientId}`, { method: "DELETE" });
        const result = await response.json();
        alert(result.message || result.error);

        if (response.ok) {
            loadPatients();
        }
    } catch (error) {
        console.error(error);
        alert("Unable to delete patient.");
    }
}

async function editPatient(patientId) {
    try {
        const response = await fetch(`${API}/patients/${patientId}`);
        const data = await response.json();

        editingPatientId = patientId;

        document.getElementById("full_name").value = data.full_name || (data.patient ? data.patient.full_name : "");
        document.getElementById("email").value = data.email || "";

        const docId = (data.doctor && data.doctor.doctor_id) ? data.doctor.doctor_id : (data.doctor_id || 1);
        setSelectValue("doctor_id", docId, 1);

        document.getElementById("age").value = data.patient ? data.patient.age : (data.age || 30);

        const genderVal = data.patient ? data.patient.gender : (data.gender || "MALE");
        setSelectValue("gender", genderVal, "MALE");

        document.getElementById("phone").value = data.patient ? data.patient.phone : (data.phone || "");
        document.getElementById("address").value = data.patient ? data.patient.address : (data.address || "");
        document.getElementById("emergency_contact").value = data.patient ? data.patient.emergency_contact : (data.emergency_contact || "");

        let admDate = data.patient ? data.patient.admission_date : (data.admission_date || "");
        if (admDate && admDate.length > 10) admDate = admDate.substring(0, 10);
        document.getElementById("admission_date").value = admDate;

        const addType = data.patient ? data.patient.addiction_type : (data.addiction_type || "Alcohol");
        setSelectValue("addiction_type", addType, "Alcohol");

        const addSev = data.patient ? data.patient.addiction_severity : (data.addiction_severity || "SEVERE");
        setSelectValue("addiction_severity", addSev, "SEVERE");

        document.getElementById("password").value = "";

        if (document.getElementById("modalTitle")) document.getElementById("modalTitle").textContent = "Edit Patient Details";
        if (document.getElementById("saveButton")) document.getElementById("saveButton").textContent = "Update Patient";

        const modal = new bootstrap.Modal(document.getElementById("patientModal"));
        modal.show();
    } catch (error) {
        console.error(error);
        alert("Unable to load patient details.");
    }
}
