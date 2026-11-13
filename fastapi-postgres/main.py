from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import models
import schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="School API")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ---------- Students ----------

@app.post("/students", response_model=schemas.StudentResponse, status_code=201)
def create_student(student: schemas.StudentCreate, db: Session = Depends(get_db)):
    db_student = models.Student(**student.model_dump())
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student


@app.get("/students", response_model=List[schemas.StudentResponse])
def read_students(db: Session = Depends(get_db)):
    return db.query(models.Student).all()


@app.get("/students/{student_id}", response_model=schemas.StudentResponse)
def read_student(student_id: int, db: Session = Depends(get_db)):
    db_student = db.get(models.Student, student_id)
    if not db_student:
        raise HTTPException(status_code=404, detail="Student not found")
    return db_student


@app.put("/students/{student_id}", response_model=schemas.StudentResponse)
def update_student(student_id: int, data: schemas.StudentCreate,
                   db: Session = Depends(get_db)):
    db_student = db.get(models.Student, student_id)
    if not db_student:
        raise HTTPException(status_code=404, detail="Student not found")
    for field, value in data.model_dump().items():
        setattr(db_student, field, value)
    db.commit()
    db.refresh(db_student)
    return db_student


@app.delete("/students/{student_id}", status_code=204)
def delete_student(student_id: int, db: Session = Depends(get_db)):
    db_student = db.get(models.Student, student_id)
    if not db_student:
        raise HTTPException(status_code=404, detail="Student not found")
    # no cascade on the model: delete enrollments first to avoid breaking the FK
    db.query(models.Enrollment).filter(
        models.Enrollment.student_id == student_id
    ).delete()
    db.delete(db_student)
    db.commit()


# ---------- Enrollments ----------

@app.post("/enrollments", response_model=schemas.EnrollmentResponse, status_code=201)
def create_enrollment(enrollment: schemas.EnrollmentCreate, db: Session = Depends(get_db)):
    if not db.get(models.Student, enrollment.student_id):
        raise HTTPException(status_code=404, detail="Student not found")
    db_enrollment = models.Enrollment(**enrollment.model_dump())
    db.add(db_enrollment)
    db.commit()
    db.refresh(db_enrollment)
    return db_enrollment


@app.get("/enrollments", response_model=List[schemas.EnrollmentResponse])
def read_enrollments(db: Session = Depends(get_db)):
    return db.query(models.Enrollment).all()


@app.get("/enrollments/{enrollment_id}", response_model=schemas.EnrollmentResponse)
def read_enrollment(enrollment_id: int, db: Session = Depends(get_db)):
    db_enrollment = db.get(models.Enrollment, enrollment_id)
    if not db_enrollment:
        raise HTTPException(status_code=404, detail="Enrollment not found")
    return db_enrollment


@app.put("/enrollments/{enrollment_id}", response_model=schemas.EnrollmentResponse)
def update_enrollment(enrollment_id: int, data: schemas.EnrollmentCreate,
                      db: Session = Depends(get_db)):
    db_enrollment = db.get(models.Enrollment, enrollment_id)
    if not db_enrollment:
        raise HTTPException(status_code=404, detail="Enrollment not found")
    if not db.get(models.Student, data.student_id):
        raise HTTPException(status_code=404, detail="Student not found")
    for field, value in data.model_dump().items():
        setattr(db_enrollment, field, value)
    db.commit()
    db.refresh(db_enrollment)
    return db_enrollment


@app.delete("/enrollments/{enrollment_id}", status_code=204)
def delete_enrollment(enrollment_id: int, db: Session = Depends(get_db)):
    db_enrollment = db.get(models.Enrollment, enrollment_id)
    if not db_enrollment:
        raise HTTPException(status_code=404, detail="Enrollment not found")
    db.delete(db_enrollment)
    db.commit()
