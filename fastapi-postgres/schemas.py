from pydantic import BaseModel, ConfigDict

class EstudanteBase(BaseModel):
    nome: str
    idade: int

class EstudanteCreate(EstudanteBase):
    pass

class EstudanteResponse(EstudanteBase):
    model_config = ConfigDict(from_attributes=True)

    id: int


class MatriculaBase(BaseModel):
    estudante_id: int
    nome_disciplina: str

class MatriculaCreate(MatriculaBase):
    pass

class MatriculaResponse(MatriculaBase):
    model_config = ConfigDict(from_attributes=True)

    id: int

