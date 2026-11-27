from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()


class StudentCreate(BaseModel):
    name: str
    age: int
    program: str


students = [
    {"name": "Sara Ahmad", "age": 20, "program": "CS"},
    {"name": "Muhammad Ali", "age": 22, "program": "SE"},
    {"name": "Ayesha Bibi", "age": 19, "program": "CS"},
]


@app.get("/")
def home():
    return {"message": "Student Directory API is running"}


@app.get("/students")
def list_students():
    return {"students": students, "count": len(students)}


@app.get("/students/{student_id}")
def get_student(student_id: int):
    if student_id < 0 or student_id >= len(students):
        raise HTTPException(status_code=404, detail="Student not found")
    return {"student": students[student_id]}


@app.post("/students", status_code=201)
def create_student(student: StudentCreate):
    new_student = {
        "name": student.name,
        "age": student.age,
        "program": student.program,
    }
    students.append(new_student)
    return {"message": "Student added", "student": new_student}
