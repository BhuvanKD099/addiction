const API = "http://127.0.0.1:5000";

let appointments = [];
let editingAppointmentId = null;

document.addEventListener("DOMContentLoaded", () => {
    loadPatients();
    loadDoctors();
    loadAppointments();

    const saveBtn = document.getElementById("saveButton");
    if (saveBtn) {
        saveBtn.addEventListener("click", saveAppointment);
    }

    const searchInput = document.getElementById("searchAppointment");
    if (searchInput) {
        searchInput.addEventListener("input", searchAppointment);
    }
});

async function loadPatients() {
    try {
        const response = await fetch(`${API}/patients/`);
        const patients = await response.json();
        const dropdown = document.getElementById("patient_id");
        if (!dropdown) return;

        dropdown.innerHTML = `<option value="">Select Patient</option>`;

        if (Array.isArray(patients)) {
            patients.forEach(patient => {
                dropdown.innerHTML += `
                    <option value="${patient.patient_id}">
                        ${patient.full_name} (ID: ${patient.patient_id})
                    </option>
                `;
            });
        }
    } catch (error) {
        console.error("Error loading patients dropdown:", error);
    }
}

async function loadDoctors() {
    try {
        const response = await fetch(`${API}/doctors/`);
        const doctors = await response.json();
        const dropdown = document.getElementById("doctor_id");
        if (!dropdown) return;

        dropdown.innerHTML = `<option value="">Select Doctor</option>`;

        if (Array.isArray(doctors)) {
            doctors.forEach(doctor => {
                dropdown.innerHTML += `
                    <option value="${doctor.doctor_id}">
                        ${doctor.full_name} - ${doctor.specialization} (ID: ${doctor.doctor_id})
                    </option>
                `;
            });
        }
    } catch (error) {
        console.error("Error loading doctors dropdown:", error);
    }
}

async function loadAppointments() {
    try {
        const response = await fetch(`${API}/appointments/`);
        appointments = await response.json();

        if (!Array.isArray(appointments)) {
            appointments = [];
        }

        displayAppointments(appointments);
    } catch (error) {
        console.error("Error loading appointments:", error);
        alert("Unable to load appointments.");
    }
}

function displayAppointments(data) {
    const table = document.getElementById("appointmentTable");
    if (!table) return;

    table.innerHTML = "";

    if (!Array.isArray(data) || data.length === 0) {
        table.innerHTML = `<tr><td colspan="8" class="text-center text-muted">No appointments found</td></tr>`;
        return;
    }

    data.forEach(appointment => {
        const row = document.createElement("tr");

        let statusBadgeClass = "bg-primary";
        const statusStr = String(appointment.status).toUpperCase();
        if (statusStr === "COMPLETED") statusBadgeClass = "bg-success";
        else if (statusStr === "CANCELLED") statusBadgeClass = "bg-danger";
        else if (statusStr === "MISSED") statusBadgeClass = "bg-warning text-dark";

        row.innerHTML = `
            <td>${appointment.appointment_id}</td>
            <td><strong>${appointment.patient ? appointment.patient.name : 'Unknown Patient'}</strong></td>
            <td>${appointment.doctor ? appointment.doctor.name : 'Unknown Doctor'}</td>
            <td>${appointment.appointment_date}</td>
            <td>${appointment.appointment_time}</td>
            <td><span class="badge ${statusBadgeClass}">${appointment.status}</span></td>
            <td>${appointment.notes || '-'}</td>
            <td>
                <button class="btn btn-warning btn-sm edit-btn me-1" data-id="${appointment.appointment_id}">
                    <i class="bi bi-pencil"></i> Edit
                </button>
                <button class="btn btn-danger btn-sm delete-btn" data-id="${appointment.appointment_id}">
                    <i class="bi bi-trash"></i> Delete
                </button>
            </td>
        `;

        table.appendChild(row);
    });

    document.querySelectorAll(".edit-btn").forEach(button => {
        button.addEventListener("click", () => editAppointment(button.dataset.id));
    });

    document.querySelectorAll(".delete-btn").forEach(button => {
        button.addEventListener("click", () => deleteAppointment(button.dataset.id));
    });
}

async function saveAppointment() {
    const patientId = document.getElementById("patient_id").value;
    const doctorId = document.getElementById("doctor_id").value;
    const appointmentDate = document.getElementById("appointment_date").value;
    const appointmentTime = document.getElementById("appointment_time").value;
    const status = document.getElementById("status").value;
    const notes = document.getElementById("notes").value;

    if (!patientId || !doctorId || !appointmentDate || !appointmentTime) {
        alert("Please select a Patient, Doctor, Date, and Time.");
        return;
    }

    const payload = {
        patient_id: parseInt(patientId),
        doctor_id: parseInt(doctorId),
        appointment_date: appointmentDate,
        appointment_time: appointmentTime,
        status: status || "SCHEDULED",
        notes: notes || ""
    };

    try {
        const url = editingAppointmentId
            ? `${API}/appointments/${editingAppointmentId}`
            : `${API}/appointments/register`;

        const method = editingAppointmentId ? "PUT" : "POST";

        const response = await fetch(url, {
            method: method,
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        });

        const result = await response.json();
        alert(result.message || result.error);

        if (response.ok) {
            const modalEl = document.getElementById("appointmentModal");
            const modal = bootstrap.Modal.getInstance(modalEl);
            if (modal) modal.hide();

            resetAppointmentForm();
            loadAppointments();
        }
    } catch (error) {
        console.error("Error saving appointment:", error);
        alert("Unable to save appointment.");
    }
}

async function editAppointment(id) {
    try {
        const response = await fetch(`${API}/appointments/${id}`);
        const appointment = await response.json();

        editingAppointmentId = id;
        document.getElementById("appointment_id").value = appointment.appointment_id;
        document.getElementById("patient_id").value = appointment.patient_id;
        document.getElementById("doctor_id").value = appointment.doctor_id;
        document.getElementById("appointment_date").value = appointment.appointment_date;

        let timeVal = appointment.appointment_time || "";
        if (timeVal.length >= 5) {
            timeVal = timeVal.substring(0, 5);
        }
        document.getElementById("appointment_time").value = timeVal;
        document.getElementById("status").value = appointment.status;
        document.getElementById("notes").value = appointment.notes || "";

        document.getElementById("modalTitle").textContent = "Edit Appointment";
        document.getElementById("saveButton").textContent = "Update Appointment";

        const modal = new bootstrap.Modal(document.getElementById("appointmentModal"));
        modal.show();
    } catch (error) {
        console.error("Error loading appointment details:", error);
        alert("Unable to load appointment.");
    }
}

async function deleteAppointment(id) {
    if (!confirm("Are you sure you want to delete this appointment?")) return;

    try {
        const response = await fetch(`${API}/appointments/${id}`, { method: "DELETE" });
        const result = await response.json();
        alert(result.message || result.error);

        if (response.ok) {
            loadAppointments();
        }
    } catch (error) {
        console.error("Error deleting appointment:", error);
        alert("Unable to delete appointment.");
    }
}

function searchAppointment() {
    const value = document.getElementById("searchAppointment").value.toLowerCase();
    const filtered = appointments.filter(app =>
        (app.patient && app.patient.name.toLowerCase().includes(value)) ||
        (app.doctor && app.doctor.name.toLowerCase().includes(value)) ||
        (app.status && app.status.toLowerCase().includes(value))
    );
    displayAppointments(filtered);
}

function resetAppointmentForm() {
    editingAppointmentId = null;
    document.getElementById("appointment_id").value = "";
    document.getElementById("patient_id").value = "";
    document.getElementById("doctor_id").value = "";
    document.getElementById("appointment_date").value = "";
    document.getElementById("appointment_time").value = "";
    document.getElementById("status").value = "SCHEDULED";
    document.getElementById("notes").value = "";
    document.getElementById("modalTitle").textContent = "Add Appointment";
    document.getElementById("saveButton").textContent = "Save Appointment";
}

function logout() {
    localStorage.removeItem("token");
    localStorage.removeItem("user");
    window.location.href = "login.html";
}