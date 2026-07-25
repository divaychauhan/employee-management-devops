from flask import (
    Flask,
    render_template,
    request,
    redirect,
    jsonify,
    session,
    url_for
)

from flask_cors import CORS

from pymongo import MongoClient

from bson.objectid import ObjectId

import os

# ============================================
# Flask App
# ============================================

app = Flask(__name__)

app.secret_key = "guitaracademy123"

CORS(app)

# ============================================
# MongoDB Connection
# ============================================

MONGO_URI = os.getenv("MONGO_URI")

client = MongoClient(MONGO_URI)

db = client["GuitarAcademyDB"]

collection = db["students"]

admin_collection = db["admins"]
# ============================================
# HOME PAGE
# ============================================

@app.route("/")
def home():

    return render_template("index.html")

# ============================================
# STUDENT REST API
# ============================================

# Get All Students
@app.route("/api/students", methods=["GET"])
def api_get_students():

    students = []

    for student in collection.find():

        students.append({

            "id": str(student["_id"]),
            "student_name": student.get("student_name", ""),
            "father_name": student.get("father_name", ""),
            "mother_name": student.get("mother_name", ""),
            "dob": student.get("dob", ""),
            "gender": student.get("gender", ""),
            "email": student.get("email", ""),
            "phone": student.get("phone", ""),
            "whatsapp": student.get("whatsapp", ""),
            "address": student.get("address", ""),
            "city": student.get("city", ""),
            "state": student.get("state", ""),
            "pincode": student.get("pincode", ""),
            "guitar_type": student.get("guitar_type", ""),
            "level": student.get("level", ""),
            "batch": student.get("batch", ""),
            "experience": student.get("experience", ""),
            "guardian_name": student.get("guardian_name", ""),
            "guardian_phone": student.get("guardian_phone", "")

        })

    return jsonify(students)


# Register Student
@app.route("/api/students", methods=["POST"])
def api_add_student():

    data = request.get_json()

    student = {

        "student_name": data.get("student_name"),
        "father_name": data.get("father_name"),
        "mother_name": data.get("mother_name"),
        "dob": data.get("dob"),
        "gender": data.get("gender"),
        "email": data.get("email"),
        "phone": data.get("phone"),
        "whatsapp": data.get("whatsapp"),
        "address": data.get("address"),
        "city": data.get("city"),
        "state": data.get("state"),
        "pincode": data.get("pincode"),
        "guitar_type": data.get("guitar_type"),
        "level": data.get("level"),
        "batch": data.get("batch"),
        "experience": data.get("experience"),
        "guardian_name": data.get("guardian_name"),
        "guardian_phone": data.get("guardian_phone")

    }

    result = collection.insert_one(student)

    return jsonify({

        "message": "Student registered successfully",
        "id": str(result.inserted_id)

    }), 201


# Delete Student
@app.route("/api/students/<id>", methods=["DELETE"])
def api_delete_student(id):

    collection.delete_one({

        "_id": ObjectId(id)

    })

    return jsonify({

        "message": "Student deleted successfully"

    })
    
    # ============================================
# ADMIN LOGIN
# ============================================

@app.route("/admin/login")
def admin_login():

    return render_template("admin_login.html")


@app.route("/admin/login", methods=["POST"])
def admin_login_post():

    username = request.form.get("username")
    password = request.form.get("password")

    admin = admin_collection.find_one({

        "username": username,
        "password": password

    })

    if admin:

        session["admin"] = username

        return redirect(url_for("admin_dashboard"))

    return render_template(

        "admin_login.html",

        error="Invalid Username or Password"

    )


# ============================================
# ADMIN DASHBOARD
# ============================================

@app.route("/admin/dashboard")
def admin_dashboard():

    if not session.get("admin"):

        return redirect(url_for("admin_login"))

    students = list(collection.find())

    total = collection.count_documents({})

    return render_template(

        "dashboard.html",

        students=students,

        total=total,

        admin=session["admin"]

    )


# ============================================
# ADMIN LOGOUT
# ============================================

@app.route("/admin/logout")
def admin_logout():

    session.clear()

    return redirect(url_for("admin_login"))
# ============================================
# HEALTH CHECK
# ============================================

@app.route("/health")
def health():

    return jsonify({

        "status": "UP",

        "application": "Guitar Coaching Academy",

        "database": "MongoDB Atlas"

    })


# ============================================
# RUN FLASK APP
# ============================================

if __name__ == "__main__":

    app.run(

        host="0.0.0.0",

        port=5000,

        debug=True

    )