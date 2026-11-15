from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import models
import schemas
from database import SessionLocal, engine
from sqlalchemy.orm import joinedload

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="School API")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ---------- Students (with nested profile) ----------

@app.post("/students", response_model=schemas.StudentResponse, status_code=201)
def create_student(student: schemas.StudentCreate, db: Session = Depends(get_db)):
    if db.query(models.Student).filter(models.Student.email == student.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    # the relationship fills profile.student_id when the student is inserted
    db_student = models.Student(
        name=student.name,
        email=student.email,
        profile=models.Profile(**student.profile.model_dump()),
    )
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student


@app.get("/students", response_model=List[schemas.StudentResponse])
def read_students(db: Session = Depends(get_db)):
    return db.query(models.Student).options(joinedload(models.Student.profile)).all()


@app.get("/students/{student_id}", response_model=schemas.StudentResponse)
def read_student(student_id: int, db: Session = Depends(get_db)):
    db_student = (
        db.query(models.Student)
        .options(joinedload(models.Student.profile))
        .filter(models.Student.id == student_id)
        .first()
    )
    if not db_student:
        raise HTTPException(status_code=404, detail="Student not found")
    return db_student


@app.put("/students/{student_id}", response_model=schemas.StudentResponse)
def update_student(student_id: int, data: schemas.StudentCreate,
                   db: Session = Depends(get_db)):
    db_student = db.get(models.Student, student_id)
    if not db_student:
        raise HTTPException(status_code=404, detail="Student not found")
    email_owner = db.query(models.Student).filter(models.Student.email == data.email).first()
    if email_owner and email_owner.id != student_id:
        raise HTTPException(status_code=400, detail="Email already registered")
    db_student.name = data.name
    db_student.email = data.email
    if db_student.profile:
        for field, value in data.profile.model_dump().items():
            setattr(db_student.profile, field, value)
    else:
        db_student.profile = models.Profile(**data.profile.model_dump())
    db.commit()
    db.refresh(db_student)
    return db_student


@app.delete("/students/{student_id}", status_code=204)
def delete_student(student_id: int, db: Session = Depends(get_db)):
    db_student = db.get(models.Student, student_id)
    if not db_student:
        raise HTTPException(status_code=404, detail="Student not found")
    # cascade="all, delete-orphan" on the relationship removes the profile too
    db.delete(db_student)
    db.commit()
