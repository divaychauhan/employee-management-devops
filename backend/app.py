from flask import Flask, render_template, request, redirect, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from bson.objectid import ObjectId
import os

app = Flask(__name__)
CORS(app)

# ==========================
# MongoDB Connection
# ==========================

MONGO_URI = os.getenv(
    "MONGO_URI",
    "mongodb://10.10.0.2:27017/"
)

client = MongoClient(MONGO_URI)

db = client["EmployeeDB"]
collection = db["employees"]

# ==========================
# Home Page
# ==========================

@app.route("/")
def home():
    return render_template("index.html")


# ==========================
# Add Employee
# ==========================

@app.route("/add", methods=["POST"])
def add_employee():

    employee = {
        "name": request.form["name"],
        "email": request.form["email"],
        "phone": request.form["phone"],
        "city": request.form["city"]
    }

    collection.insert_one(employee)

    return redirect("/employees")


# ==========================
# View Employees
# ==========================

@app.route("/employees")
def employees():

    employee_list = list(collection.find())

    total = collection.count_documents({})

    return render_template(
        "employees.html",
        employees=employee_list,
        total=total
    )


# ==========================
# Delete Employee
# ==========================

@app.route("/delete/<id>")
def delete_employee(id):

    collection.delete_one(
        {"_id": ObjectId(id)}
    )

    return redirect("/employees")


# ===================================================
# REST API
# ===================================================

@app.route("/api/employees", methods=["GET"])
def api_employees():

    employee_list = []

    for emp in collection.find():

        employee_list.append({
            "id": str(emp["_id"]),
            "name": emp["name"],
            "email": emp["email"],
            "phone": emp["phone"],
            "city": emp["city"]
        })

    return jsonify(employee_list)


# ==========================
# Run Flask Application
# ==========================

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )