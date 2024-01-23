from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from flask_basicauth import BasicAuth

app = Flask(__name__)

# MongoDB configuration
app.config['MONGO_URI'] = "mongodb+srv://thitsanu:Avocadoo.13124@cluster0.l40hdec.mongodb.net/test"
mongo = PyMongo(app)

# Basic authentication configuration
app.config['BASIC_AUTH_USERNAME'] = 'admin'
app.config['BASIC_AUTH_PASSWORD'] = 'secret'
basic_auth = BasicAuth(app)

@app.route("/")
def greet():
    return "<p>Welcome to Student Management API</p>"

@app.route("/students", methods=["GET"])
@basic_auth.required
def get_all_students():
    students = mongo.db.students.find()
    return jsonify({"students": list(students)})

@app.route("/students/<int:student_id>", methods=["GET"])
@basic_auth.required
def get_student(student_id):
    student = mongo.db.students.find_one({"id": student_id})
    if student:
        return jsonify(student)
    else:
        return jsonify({"error": "Student not found"}), 404

@app.route("/students", methods=["POST"])
@basic_auth.required
def create_student():
    data = request.get_json()
    new_student = {
        "id": data["id"],
        "Name": data["Name"],
        "author": data["author"]
    }
    mongo.db.students.insert_one(new_student)
    return jsonify(new_student), 201

@app.route("/students/<int:student_id>", methods=["PUT"])
@basic_auth.required
def update_student(student_id):
    student = mongo.db.students.find_one({"id": student_id})
    if student:
        data = request.get_json()
        mongo.db.students.update_one({"id": student_id}, {"$set": data})
        return jsonify(data)
    else:
        return jsonify({"error": "Student not found"}), 404

@app.route("/students/<int:student_id>", methods=["DELETE"])
@basic_auth.required
def delete_student(student_id):
    result = mongo.db.students.delete_one({"id": student_id})
    if result.deleted_count > 0:
        return jsonify({"message": "Student deleted successfully"}), 200
    else:
        return jsonify({"error": "Student not found"}), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
    print("max")
