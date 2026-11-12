from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import models
import schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Escola API")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ---------- Estudantes ----------

@app.post("/estudantes", response_model=schemas.EstudanteResponse, status_code=201)
def criar_estudante(estudante: schemas.EstudanteCreate, db: Session = Depends(get_db)):
    novo = models.Estudante(**estudante.model_dump())
    db.add(novo)
    db.commit()
    db.refresh(novo)
    return novo


@app.get("/estudantes", response_model=List[schemas.EstudanteResponse])
def listar_estudantes(db: Session = Depends(get_db)):
    return db.query(models.Estudante).all()


@app.get("/estudantes/{estudante_id}", response_model=schemas.EstudanteResponse)
def obter_estudante(estudante_id: int, db: Session = Depends(get_db)):
    estudante = db.get(models.Estudante, estudante_id)
    if not estudante:
        raise HTTPException(status_code=404, detail="Estudante não encontrado")
    return estudante


@app.put("/estudantes/{estudante_id}", response_model=schemas.EstudanteResponse)
def atualizar_estudante(estudante_id: int, dados: schemas.EstudanteCreate,
                        db: Session = Depends(get_db)):
    estudante = db.get(models.Estudante, estudante_id)
    if not estudante:
        raise HTTPException(status_code=404, detail="Estudante não encontrado")
    for campo, valor in dados.model_dump().items():
        setattr(estudante, campo, valor)
    db.commit()
    db.refresh(estudante)
    return estudante


@app.delete("/estudantes/{estudante_id}", status_code=204)
def deletar_estudante(estudante_id: int, db: Session = Depends(get_db)):
    estudante = db.get(models.Estudante, estudante_id)
    if not estudante:
        raise HTTPException(status_code=404, detail="Estudante não encontrado")
    # sem cascade no model, remove as matrículas antes para não violar a FK
    db.query(models.Matricula).filter(
        models.Matricula.estudante_id == estudante_id
    ).delete()
    db.delete(estudante)
    db.commit()


# ---------- Matrículas ----------

@app.post("/matriculas", response_model=schemas.MatriculaResponse, status_code=201)
def criar_matricula(matricula: schemas.MatriculaCreate, db: Session = Depends(get_db)):
    if not db.get(models.Estudante, matricula.estudante_id):
        raise HTTPException(status_code=404, detail="Estudante não encontrado")
    nova = models.Matricula(**matricula.model_dump())
    db.add(nova)
    db.commit()
    db.refresh(nova)
    return nova


@app.get("/matriculas", response_model=List[schemas.MatriculaResponse])
def listar_matriculas(db: Session = Depends(get_db)):
    return db.query(models.Matricula).all()


@app.get("/matriculas/{matricula_id}", response_model=schemas.MatriculaResponse)
def obter_matricula(matricula_id: int, db: Session = Depends(get_db)):
    matricula = db.get(models.Matricula, matricula_id)
    if not matricula:
        raise HTTPException(status_code=404, detail="Matrícula não encontrada")
    return matricula


@app.put("/matriculas/{matricula_id}", response_model=schemas.MatriculaResponse)
def atualizar_matricula(matricula_id: int, dados: schemas.MatriculaCreate,
                        db: Session = Depends(get_db)):
    matricula = db.get(models.Matricula, matricula_id)
    if not matricula:
        raise HTTPException(status_code=404, detail="Matrícula não encontrada")
    if not db.get(models.Estudante, dados.estudante_id):
        raise HTTPException(status_code=404, detail="Estudante não encontrado")
    for campo, valor in dados.model_dump().items():
        setattr(matricula, campo, valor)
    db.commit()
    db.refresh(matricula)
    return matricula


@app.delete("/matriculas/{matricula_id}", status_code=204)
def deletar_matricula(matricula_id: int, db: Session = Depends(get_db)):
    matricula = db.get(models.Matricula, matricula_id)
    if not matricula:
        raise HTTPException(status_code=404, detail="Matrícula não encontrada")
    db.delete(matricula)
    db.commit()

