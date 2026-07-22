// ===========================================
// Backend API URL
// ===========================================

const API_URL = "http://34.47.233.168:5000/api/employees";


// ===========================================
// Add Employee
// ===========================================

const employeeForm = document.getElementById("employeeForm");

if (employeeForm) {

    employeeForm.addEventListener("submit", async function (e) {

        e.preventDefault();

        const employee = {

            name: document.getElementById("name").value,
            email: document.getElementById("email").value,
            phone: document.getElementById("phone").value,
            city: document.getElementById("city").value

        };

        const response = await fetch(API_URL, {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify(employee)

        });

        if (response.ok) {

            alert("Employee Added Successfully");

            employeeForm.reset();

        } else {

            alert("Failed to Add Employee");

        }

    });

}


// ===========================================
// Load Employees
// ===========================================

async function loadEmployees() {

    const table = document.getElementById("employeeTable");

    if (!table) return;

    table.innerHTML = "";

    const response = await fetch(API_URL);

    const employees = await response.json();

    employees.forEach(emp => {

        table.innerHTML += `

        <tr>

            <td>${emp.name}</td>

            <td>${emp.email}</td>

            <td>${emp.phone}</td>

            <td>${emp.city}</td>

            <td>

                <button
                    class="btn btn-danger btn-sm"
                    onclick="deleteEmployee('${emp.id}')">

                    Delete

                </button>

            </td>

        </tr>

        `;

    });

}


// ===========================================
// Delete Employee
// ===========================================

async function deleteEmployee(id) {

    if (!confirm("Delete this employee?")) {

        return;

    }

    const response = await fetch(`${API_URL}/${id}`, {

        method: "DELETE"

    });

    if (response.ok) {

        loadEmployees();

    } else {

        alert("Delete Failed");

    }

}


// ===========================================
// Auto Load Employee List
// ===========================================

loadEmployees();