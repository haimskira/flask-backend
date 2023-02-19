from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
#CORS(app)
cors = CORS(app, resources={r"/*": {"origins": "*"}}, allow_methods=["*"],allow_host=["*"])

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    def __repr__(self):
        return f"Student({self.id}, {self.name}, {self.age})"

#GET
@app.route('/student/<int:student_id>', methods=['GET'])
def get_student(student_id):
    student = Student.query.get(student_id)
    return {'id': student.id, 'name': student.name, 'age': student.age}

#GET All Student
@app.route('/student', methods=['GET'])
def display_all():
    res=[]
    for stu in Student.query.all():
        res.append({'id': stu.id, 'name': stu.name, 'age': stu.age})
    return jsonify (res)

#POST
@app.route('/student', methods=['POST'])
def add_student():
    student_data = request.get_json()
    student = Student(name=student_data['name'], age= student_data['age'])
    db.session.add(student)
    db.session.commit()
    return {'id': student.id, 'name': student.name, 'age': student.age}

#Update
@app.route('/student/<int:student_id>', methods=['PUT'])
def update_student(student_id):
    student_data = request.get_json()
    student = Student.query.get(student_id)
    student.name = student_data['name']
    student.age = student_data['age']
    db.session.commit()
    return {'id': student.id, 'name': student.name, 'age': student.age}

#DELETE
@app.route('/student/<int:student_id>', methods=['DELETE'])
def delete_student(student_id):
    student = Student.query.get(student_id)
    db.session.delete(student)
    db.session.commit()
    return {'id': student.id, 'name': student.name, 'age': student.age}

# @app.after_request
# def after_request(response):
#     response.headers.add('Access-Control-Allow-Origin', '*')
#     response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
#     response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
#     return response

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
