from pydantic import BaseModel, ConfigDict


class StudentBase(BaseModel):
    name: str
    age: int


class StudentCreate(StudentBase):
    pass


class StudentResponse(StudentBase):
    model_config = ConfigDict(from_attributes=True)

    id: int


class EnrollmentBase(BaseModel):
    student_id: int
    course_name: str


class EnrollmentCreate(EnrollmentBase):
    pass


class EnrollmentResponse(EnrollmentBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
