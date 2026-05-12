# ============================================================
# 📝 FastAPI Student Management System App (CRUD) - SQLite
# ============================================================

from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

# ============================================================
# Create FastAPI App
# ============================================================

app = FastAPI()

# ============================================================
# Database Configuration
# ============================================================

DATABASE_URL = "sqlite:///./students.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()

# ============================================================
# Database Model
# ============================================================

class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    age = Column(Integer)
    marks = Column(Integer)
    course = Column(String)
    is_active = Column(Boolean, default=True)

# Create tables
Base.metadata.create_all(bind=engine)

# ============================================================
# Pydantic Models
# ============================================================

class StudentCreate(BaseModel):
    id: int
    name: str
    age: int
    marks: int
    course: str


class StudentResponse(BaseModel):
    id: int
    name: str
    age: int
    marks: int
    course: str
    is_active: bool

    class Config:
        from_attributes = True

# ============================================================
# Database Dependency
# ============================================================

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ============================================================
# Home Route
# ============================================================

@app.get("/")
def home():
    return {
        "message": "Welcome to Student Management System API"
    }

# ============================================================
# Create Student
# ============================================================

@app.post("/students/")
def create_student(
    student: StudentCreate,
    db: Session = Depends(get_db)
):

    # Check duplicate ID
    existing_student = (
        db.query(Student)
        .filter(Student.id == student.id)
        .first()
    )

    if existing_student:
        raise HTTPException(
            status_code=400,
            detail="Student with this ID already exists"
        )

    # Create student object
    new_student = Student(
        id=student.id,
        name=student.name,
        age=student.age,
        marks=student.marks,
        course=student.course,
        is_active=True
    )

    db.add(new_student)
    db.commit()
    db.refresh(new_student)

    return {
        "message": "Student created successfully",
        "student": new_student
    }

# ============================================================
# Get All Students
# ============================================================

@app.get("/students/")
def get_all_students(db: Session = Depends(get_db)):

    students = db.query(Student).all()

    return {
        "count": len(students),
        "students": students
    }

# ============================================================
# Get Student By ID
# ============================================================

@app.get("/students/{student_id}")
def get_student(
    student_id: int,
    db: Session = Depends(get_db)
):

    student = (
        db.query(Student)
        .filter(Student.id == student_id)
        .first()
    )

    if not student:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    return {"student": student}

# ============================================================
# Update Student
# ============================================================

@app.put("/students/{student_id}")
def update_student(
    student_id: int,
    updated_student: StudentCreate,
    db: Session = Depends(get_db)
):

    student = (
        db.query(Student)
        .filter(Student.id == student_id)
        .first()
    )

    if not student:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    # Update fields
    student.name = updated_student.name
    student.age = updated_student.age
    student.marks = updated_student.marks
    student.course = updated_student.course

    db.commit()
    db.refresh(student)

    return {
        "message": "Student updated successfully",
        "student": student
    }

# ============================================================
# Delete Student
# ============================================================

@app.delete("/students/{student_id}")
def delete_student(
    student_id: int,
    db: Session = Depends(get_db)
):

    student = (
        db.query(Student)
        .filter(Student.id == student_id)
        .first()
    )

    if not student:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    db.delete(student)
    db.commit()

    return {
        "message": "Student deleted successfully"
    }