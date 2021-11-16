from typing import Optional, List
from fastapi import FastAPI, Query, HTTPException, Depends
from sqlalchemy.orm import Session
import crud, models, schemas
from database import SessionLocal, engine
from utils import *

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/usuario")
async def lista_usuario(id_usuario: str, db: Session = Depends(get_db)):
    return crud.pega_usuario(db, id_usuario=id_usuario)

@app.post("/usuario", response_model=schemas.CriaUsuario)
async def cria_usuario(usuario: schemas.CriaUsuario, db: Session = Depends(get_db)):
    db_usuario = crud.pega_usuario(db, id_usuario=usuario.id_usuario)
    if db_usuario:
         raise HTTPException(status_code=404, detail="Usuario já registrado")
    else:
        crud.cria_usuario(db, usuario=usuario)
        return usuario

@app.get("/disciplina")
async def lista_disciplinas(id_usuario: str, db: Session = Depends(get_db)):
    return crud.lista_disciplinas(db, id_usuario=id_usuario)

@app.post("/disciplina")
async def cria_disciplina_rota(disciplina: schemas.CriaDisciplina, db: Session = Depends(get_db)):
    db_disciplina = crud.pega_disciplina(db, nome=disciplina.nome, id_usuario=disciplina.id_usuario)
    if db_disciplina:
         raise HTTPException(status_code=404, detail="Disciplina já registrada")
    else:
        crud.cria_disciplina(db, disciplina=disciplina)
        return disciplina