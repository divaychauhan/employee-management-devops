from flask import Flask, render_template, request, redirect, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from bson.objectid import ObjectId
import os

app = Flask(__name__)
CORS(app)

# ============================================
# MongoDB Connection
# ============================================

MONGO_URI = os.getenv(
    "MONGO_URI",
    "mongodb://10.10.0.2:27017/"
)

client = MongoClient(MONGO_URI)

db = client["EmployeeDB"]
collection = db["employees"]


# ============================================
# Temporary HTML Routes
# (Will be removed after frontend migration)
# ============================================

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/employees")
def employees():

    employee_list = list(collection.find())

    total = collection.count_documents({})

    return render_template(
        "employees.html",
        employees=employee_list,
        total=total
    )


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


@app.route("/delete/<id>")
def delete_employee(id):

    collection.delete_one(
        {"_id": ObjectId(id)}
    )

    return redirect("/employees")


# ============================================
# REST API
# ============================================

# Get All Employees
@app.route("/api/employees", methods=["GET"])
def api_get_employees():

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


# Add Employee
@app.route("/api/employees", methods=["POST"])
def api_add_employee():

    data = request.get_json()

    employee = {

        "name": data["name"],
        "email": data["email"],
        "phone": data["phone"],
        "city": data["city"]

    }

    result = collection.insert_one(employee)

    return jsonify({

        "message": "Employee added successfully",
        "id": str(result.inserted_id)

    }), 201


# Delete Employee
@app.route("/api/employees/<id>", methods=["DELETE"])
def api_delete_employee(id):

    collection.delete_one(
        {"_id": ObjectId(id)}
    )

    return jsonify({

        "message": "Employee deleted successfully"

    })


# Health Check
@app.route("/health")
def health():

    return jsonify({

        "status": "UP"

    })


# ============================================
# Run Flask App
# ============================================

if __name__ == "__main__":

    app.run(

        host="0.0.0.0",
        port=5000,
        debug=True

    )