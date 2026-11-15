from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class Student(Base):
    __tablename__ = 'students'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True)

    # one-to-one: each student has at most one profile
    profile = relationship(
        "Profile",
        back_populates="student",
        uselist=False,
        cascade="all, delete-orphan"
    )


class Profile(Base):
    __tablename__ = 'profiles'

    id = Column(Integer, primary_key=True, index=True)
    age = Column(Integer)
    address = Column(String)

    # unique=True guarantees the one-to-one side on the database
    student_id = Column(
        Integer,
        ForeignKey('students.id'),
        unique=True,
        nullable=False
    )

    student = relationship("Student", back_populates="profile")
