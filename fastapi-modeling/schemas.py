from typing import Optional

from pydantic import BaseModel, ConfigDict


# ---------- Profile ----------

class ProfileBase(BaseModel):
    age: Optional[int] = None
    address: Optional[str] = None


class ProfileCreate(ProfileBase):
    # no student_id here: the profile is created nested inside the student,
    # and the server fills student_id after the student gets its id
    pass


class ProfileResponse(ProfileBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    student_id: int


# ---------- Student ----------

class StudentBase(BaseModel):
    name: str
    email: Optional[str] = None


class StudentCreate(StudentBase):
    name: str
    email: str
    profile: ProfileCreate


class StudentResponse(StudentBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    # nested one-to-one: the student comes with their profile (or null)
    profile: Optional[ProfileResponse] = None
