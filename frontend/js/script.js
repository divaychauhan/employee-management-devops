const form = document.getElementById("registrationForm");

form.addEventListener("submit", async function (e) {
    e.preventDefault();

    const student = {
        student_name: document.getElementById("studentName").value.trim(),
        father_name: document.getElementById("fatherName").value.trim(),
        mother_name: document.getElementById("motherName").value.trim(),
        dob: document.getElementById("dob").value,
        gender: document.getElementById("gender").value,

        email: document.getElementById("email").value.trim(),
        phone: document.getElementById("phone").value.trim(),
        whatsapp: document.getElementById("whatsapp").value.trim(),

        address: document.getElementById("address").value.trim(),
        city: document.getElementById("city").value.trim(),
        state: document.getElementById("state").value.trim(),
        pincode: document.getElementById("pincode").value.trim(),

        guitar_type: document.getElementById("guitarType").value,
        level: document.getElementById("level").value,
        batch: document.getElementById("batch").value,

        experience: document.getElementById("experience").value.trim(),

        guardian_name: document.getElementById("guardianName").value.trim(),
        guardian_phone: document.getElementById("guardianPhone").value.trim()
    };

    // Basic Validation
    if (
        student.student_name === "" ||
        student.father_name === "" ||
        student.email === "" ||
        student.phone === ""
    ) {
        alert("Please fill all required fields.");
        return;
    }

    try {

        // Development Backend
        const response = await fetch("http://34.47.233.168:5000/api/students", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(student)
        });

        const data = await response.json();

        if (response.ok) {
            alert("🎸 Student Registered Successfully!");
            form.reset();
        } else {
            alert(data.message || "Registration Failed.");
        }

    } catch (error) {
        console.error(error);
        alert("Unable to connect to the backend server.");
    }
});