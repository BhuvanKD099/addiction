
const token = localStorage.getItem("token") || "demo_token";
let editMode = false;

// Load Doctors
async function loadDoctors() {

    try {

        const doctors = await apiRequest(
            "/doctors/",
            "GET",
            null,   
            token
        );

        const table = document.getElementById("doctorTable");

        table.innerHTML = "";

        doctors.forEach((doctor) => {

            table.innerHTML += `
<tr>

    <td>${doctor.doctor_id}</td>

    <td>${doctor.full_name}</td>

    <td>${doctor.email}</td>

    <td>${doctor.specialization}</td>

    <td>${doctor.phone}</td>

    <td>${doctor.experience_years}</td>

    <td>${doctor.qualification}</td>

    <td>

        <button
            class="btn btn-warning btn-sm edit-btn"
            data-id="${doctor.doctor_id}"
            data-name="${doctor.full_name}"
            data-email="${doctor.email}"
            data-specialization="${doctor.specialization}"
            data-phone="${doctor.phone}"
            data-experience="${doctor.experience_years}"
            data-qualification="${doctor.qualification}">

            <i class="bi bi-pencil"></i>
            Edit

        </button>

        <button
            class="btn btn-danger btn-sm ms-2 delete-btn"
            data-id="${doctor.doctor_id}">

            <i class="bi bi-trash"></i>
            Delete

        </button>

    </td>

</tr>
`;

        });
document.querySelectorAll(".edit-btn").forEach(button => {

    button.addEventListener("click", function () {

        openEditDoctor(
            this.dataset.id,
            this.dataset.name,
            this.dataset.email,
            this.dataset.specialization,
            this.dataset.phone,
            this.dataset.experience,
            this.dataset.qualification
        );

    });

});

document.querySelectorAll(".delete-btn").forEach(button => {

    button.addEventListener("click", function () {

        deleteDoctor(this.dataset.id);

    });

});

    } catch (error) {

        console.error(error);
        alert("Unable to load doctors.");

    }

}

// Add Doctor
async function addDoctor() {
    console.log("addDoctor() called");
    const doctor = {

        full_name: document.getElementById("full_name").value.trim(),
        email: document.getElementById("email").value.trim(),
        password: document.getElementById("password").value,
        specialization: document.getElementById("specialization").value.trim(),
        phone: document.getElementById("phone").value.trim(),
        experience_years: parseInt(document.getElementById("experience").value),
        qualification: document.getElementById("qualification").value.trim()

    };

    // Simple validation
    if (
        !doctor.full_name ||
        !doctor.email ||
        !doctor.password ||
        !doctor.specialization ||
        !doctor.phone ||
        !doctor.qualification ||
        isNaN(doctor.experience_years)
    ) {
        alert("Please fill all fields.");
        return;
    }

    try {

        const result = await apiRequest(
            "/doctors/register",
            "POST",
            doctor,
            token
        );

        alert(result.message);

        // Close Modal
        const modalElement = document.getElementById("doctorModal");
        const modal = bootstrap.Modal.getInstance(modalElement);
        modal.hide();

        // Clear Form
        document.getElementById("full_name").value = "";
        document.getElementById("email").value = "";
        document.getElementById("password").value = "";
        document.getElementById("specialization").value = "";
        document.getElementById("phone").value = "";
        document.getElementById("experience").value = "";
        document.getElementById("qualification").value = "";

        // Reload Table
        loadDoctors();

    } catch (error) {

        console.error(error);
        alert("Failed to add doctor.");

    }

}
function openAddDoctorModal() {
    editMode = false;
    if (document.getElementById("doctor_id")) document.getElementById("doctor_id").value = "";
    if (document.getElementById("full_name")) document.getElementById("full_name").value = "";
    if (document.getElementById("email")) document.getElementById("email").value = "";
    if (document.getElementById("password")) document.getElementById("password").value = "";
    if (document.getElementById("specialization")) document.getElementById("specialization").value = "";
    if (document.getElementById("phone")) document.getElementById("phone").value = "";
    if (document.getElementById("experience")) document.getElementById("experience").value = "10";
    if (document.getElementById("qualification")) document.getElementById("qualification").value = "";

    if (document.getElementById("email")) document.getElementById("email").disabled = false;
    if (document.getElementById("password")) document.getElementById("password").disabled = false;

    if (document.getElementById("modalTitle")) document.getElementById("modalTitle").innerText = "Register New Doctor";
    if (document.getElementById("saveButton")) document.getElementById("saveButton").innerText = "Save Doctor";

    const modal = new bootstrap.Modal(document.getElementById("doctorModal"));
    modal.show();
}

function openEditDoctor(
    doctor_id,
    full_name,
    email,
    specialization,
    phone,
    experience_years,
    qualification
) {

    console.log("Edit clicked");

    console.log(document.getElementById("doctor_id"));
    console.log(document.getElementById("full_name"));
    console.log(document.getElementById("modalTitle"));
    console.log(document.getElementById("saveButton"));

    editMode = true;

    document.getElementById("doctor_id").value = doctor_id;
    document.getElementById("full_name").value = full_name;
    document.getElementById("email").value = email;
    document.getElementById("specialization").value = specialization;
    document.getElementById("phone").value = phone;
    document.getElementById("experience").value = experience_years;
    document.getElementById("qualification").value = qualification;

    document.getElementById("email").disabled = true;
    document.getElementById("password").disabled = true;

    if (document.getElementById("modalTitle"))
        document.getElementById("modalTitle").innerText = "Edit Doctor";

    if (document.getElementById("saveButton"))
        document.getElementById("saveButton").innerText = "Update Doctor";

    new bootstrap.Modal(document.getElementById("doctorModal")).show();
}
function saveDoctor() {

    console.log("saveDoctor() called");
    console.log("editMode =", editMode);

    if (editMode) {

        updateDoctor();

    } else {

        addDoctor();

    }

}
async function updateDoctor() {
console.log("Update button clicked");
    const doctor_id = document.getElementById("doctor_id").value;

    const doctor = {

        full_name: document.getElementById("full_name").value.trim(),
        specialization: document.getElementById("specialization").value.trim(),
        phone: document.getElementById("phone").value.trim(),
        experience_years: parseInt(document.getElementById("experience").value),
        qualification: document.getElementById("qualification").value.trim()

    };

    try {

        const result = await apiRequest(
            `/doctors/${doctor_id}`,
            "PUT",
            doctor,
            token
        );

        alert(result.message);

        // Close modal
        const modal = bootstrap.Modal.getInstance(
            document.getElementById("doctorModal")
        );
        modal.hide();

        // Clear form
        document.getElementById("doctor_id").value = "";
        document.getElementById("full_name").value = "";
        document.getElementById("email").value = "";
        document.getElementById("password").value = "";
        document.getElementById("specialization").value = "";
        document.getElementById("phone").value = "";
        document.getElementById("experience").value = "";
        document.getElementById("qualification").value = "";

        // Restore Add mode
        editMode = false;
        document.getElementById("modalTitle").innerText = "Add Doctor";
        document.getElementById("saveButton").innerText = "Save Doctor";
        document.getElementById("email").disabled = false;
        document.getElementById("password").disabled = false;

        loadDoctors();

    } catch (error) {

        console.error(error);
        alert("Failed to update doctor.");

    }

}
async function deleteDoctor(doctor_id) {

    const confirmDelete = confirm("Are you sure you want to delete this doctor?");

    if (!confirmDelete) {
        return;
    }

    try {

        const result = await apiRequest(
            `/doctors/${doctor_id}`,
            "DELETE",
            null,
            token
        );

        alert(result.message);

        loadDoctors();

    } catch (error) {

        console.error(error);
        alert("Failed to delete doctor.");

    }

}
// Logout
function logout() {

    localStorage.removeItem("token");
    localStorage.removeItem("user");

    window.location.href = "login.html";

}
document.getElementById("searchDoctor").addEventListener("keyup", function () {

    const searchText = this.value.toLowerCase();

    const rows = document.querySelectorAll("#doctorTable tr");

    rows.forEach(row => {

        const rowText = row.innerText.toLowerCase();

        if (rowText.includes(searchText)) {
            row.style.display = "";
        } else {
            row.style.display = "none";
        }

    });

});
// Initial Load
loadDoctors();