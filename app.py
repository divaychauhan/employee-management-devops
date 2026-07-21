from flask import Flask, render_template, request, redirect
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)

# MongoDB Connection
client = MongoClient("mongodb://10.10.0.2:27017/")

db = client["EmployeeDB"]
collection = db["employees"]


# Home Page
@app.route("/")
def home():
    return render_template("index.html")


# Add Employee
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


# View Employees
@app.route("/employees")
def employees():

    employee_list = list(collection.find())

    total = collection.count_documents({})

    return render_template(
        "employees.html",
        employees=employee_list,
        total=total
    )


# Delete Employee
@app.route("/delete/<id>")
def delete_employee(id):

    collection.delete_one(
        {"_id": ObjectId(id)}
    )

    return redirect("/employees")


# Run Flask App
if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )
