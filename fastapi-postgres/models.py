from sqlalchemy import Column, Integer, String, ForeignKey
from database import Base


class Student(Base):
    __tablename__ = 'students'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    age = Column(Integer)


class Enrollment(Base):
    __tablename__ = 'enrollments'

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey('students.id'))
    course_name = Column(String(100), nullable=False)
