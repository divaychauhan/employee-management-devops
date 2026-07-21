from flask import Flask, render_template, request, redirect
from pymongo import MongoClient
from bson.objectid import ObjectId
import os

app = Flask(__name__)

# MongoDB Connection
MONGO_URI = os.getenv(
    "MONGO_URI",
    "mongodb://10.10.0.2:27017/"
)

client = MongoClient(MONGO_URI)

db = client["EmployeeDB"]
collection = db["employees"]