from flask import Flask, request, jsonify
from flask_basicauth import BasicAuth
from pymongo.mongo_client import MongoClient

app = Flask(__name__)


uri = "mongodb+srv://thitsanu25:Avocadoo.13124@cluster0.l40hdec.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri)

    
app.config['BASIC_AUTH_USERNAME'] = 'admin'
app.config['BASIC_AUTH_PASSWORD'] = 'max'
basic_auth = BasicAuth(app)

client.admin.command('ping')
db = client["students"]
collection = db["std_info"]
 
 
@app.route("/")
def greet():
    return "<p>Welcome to Student Management API</p>"

@app.route("/students", methods=["GET"])
@basic_auth.required

def get_all_students():
    students = collection.find()
    return jsonify({"students": list(students)})


@app.route("/students/<int:student_id>", methods=["GET"])
@basic_auth.required

def get_student(student_id):
    student = collection.find_one({"_id": str(student_id)})
    if not student:
        return jsonify({"error": "Student not found"}), 404

    return jsonify(student)


@app.route("/students", methods=["POST"])
@basic_auth.required

def create_student():
    data = request.get_json()
    collection.insert_one(data)
    
    return jsonify(data),201



@app.route("/students/<int:student_id>", methods=["PUT"])
@basic_auth.required

def update_student(student_id):
    student = collection.find_one({"_id": str(student_id)})
    if not student:
        return jsonify({"error": "Student not found"}), 404
    
    data = request.get_json()
    collection.update_one({"_id": str(student_id)}, {"$set": data})
    return jsonify(collection.find_one({"_id": str(student_id)}))


@app.route("/students/<int:student_id>", methods=["DELETE"])
@basic_auth.required

def delete_student(student_id):
    student = collection.find_one({"_id": str(student_id)})
    if not student:
       return jsonify({"error": "Student not found"}), 404
   
    collection.delete_one({"_id": str(student_id)})
    return jsonify({"message": "Student deleted successfully"}), 200



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
   
