from typing import Optional, List
from fastapi import FastAPI, Query, HTTPException, Depends
from sqlalchemy.orm import Session
import crud
import models
import schemas
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

# lista usuários
@app.get("/usuario")
async def lista_usuario(db: Session = Depends(get_db)):
    return crud.lista_usuarios(db)

# cria usuário
@app.post("/usuario", response_model=schemas.CriaUsuario)
async def cria_usuario(usuario: schemas.CriaUsuario, db: Session = Depends(get_db)):
    db_usuario = crud.pega_usuario(db, id_usuario=usuario.id_usuario)
    if db_usuario:
        raise HTTPException(status_code=404, detail="Usuario já registrado")
    else:
        crud.cria_usuario(db, usuario=usuario)
        return {'status': 200, 'descrição': 'Criado', 'cacheability': 'False'}

# o usuário pode listar suas disciplinas
@app.get("/disciplina")
async def lista_disciplinas(id_usuario: str, db: Session = Depends(get_db)):
    return crud.lista_disciplinas(db, id_usuario=id_usuario)


# o usuário pode criar uma disciplina
@app.post("/disciplina")
async def cria_disciplina(disciplina: schemas.CriaDisciplina, db: Session = Depends(get_db)):
    db_usuario = crud.pega_usuario(db, id_usuario=disciplina.id_usuario)
    db_disciplina = crud.pega_disciplina(
        db, nome=disciplina.nome, id_usuario=disciplina.id_usuario)
    if db_disciplina:
        raise HTTPException(status_code=404, detail="Disciplina já registrada")
    elif not db_usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    else:
        crud.cria_disciplina(db, disciplina=disciplina)
        return {'status': 200, 'descrição': 'Criado', 'cacheability': 'False'}

# o usuário pode deletar uma disciplina
@app.delete("/disciplina")
async def deleta_disciplina(disciplina: schemas.DeletaDisciplina, db: Session = Depends(get_db)):
    db_disciplina = crud.pega_disciplina(
        db, nome=disciplina.nome, id_usuario=disciplina.id_usuario)
    if db_disciplina:
        crud.deleta_disciplina(db, disciplina=disciplina)
        return {'status': 200, 'descrição': 'Deletado', 'cacheability': 'False'}
    else:
        raise HTTPException(
            status_code=404, detail="Disciplina não encontrada")

# o usuário pode deletar uma disciplina
@app.put("/disciplina")
async def atualiza_disciplina(
    disciplina_para_atualizar: schemas.EncontraDisciplina,
    disciplina: schemas.AtualizaDisciplina,
    db: Session = Depends(get_db)):
    db_disciplina = crud.pega_disciplina(
        db,
        nome=disciplina_para_atualizar.nome,
        id_usuario=disciplina_para_atualizar.id_usuario)
    if db_disciplina:
        crud.atualiza_disciplina(
            db, 
            disciplina_atualizar=disciplina_para_atualizar,
            disciplina=disciplina)
        return {'status': 200, 'descrição': 'Atualizado', 'cacheability': 'False'}
    else:
        raise HTTPException(
            status_code=404, detail="Disciplina não encontrada")

# o usuário pode adicionar uma nota em uma disciplina
@app.post("/usuario/disciplina")
async def adiciona_nota(nota: schemas.CriaNota, db: Session = Depends(get_db)):
    disciplina_atualizar = crud.id_pega_disciplina(db, id_disciplina=nota.id_disciplina)
    if disciplina_atualizar is None:
        raise HTTPException(status_code=404, detail="Disciplina não encontrada")
    else:
        nota_criar = crud.pega_nota(db, id_disciplina=nota.id_disciplina, identificador=nota.identificador)
        if nota_criar is None:
            crud.cria_nota(db, nota=nota)
            return {'status': 200, 'descrição': 'Adicionado', 'cacheability': 'False'}
        else:
            raise HTTPException(status_code=406, detail="Identificador de nota já existe")

# o usuário pode listar suas notas
@app.get("/nota")
async def lista_nota(id_disciplina: int, db: Session = Depends(get_db)):
    return crud.lista_notas(db, id_disciplina=id_disciplina)

# o usuário pode deletar uma nota
@app.delete("/usuario/disciplina/identificador")
def deleta_nota(id_disciplina: int, identificador: str, db: Session = Depends(get_db)):
    disciplina_deletar = crud.id_pega_disciplina(db, id_disciplina=id_disciplina)
    if disciplina_deletar is not None:
        nota_deletar = crud.pega_nota(db, id_disciplina=id_disciplina, identificador=identificador)
        if nota_deletar is not None:
            crud.deleta_nota(db, id_disciplina=id_disciplina, identificador=identificador)
            return {'status': 200, 'descrição': 'Deletado', 'cacheability': 'False'}  
    raise HTTPException(status_code=404, detail="Item não encontrado")

# O usuário pode modificar uma nota de uma disciplina
@app.put("/disciplina/notas")
async def atualiza_nota(
    id_nota: int,
    nota: float,
    db: Session = Depends(get_db)):
    db_nota = crud.pega_notas(db,id_nota= id_nota) #verifica se tem nota
    if db_nota:
        crud.atualiza_nota(
            db, 
            nota= nota ,
            nota_id= id_nota
            )
        return {'status': 200, 'descrição': 'Atualizado', 'cacheability': 'False'}  #modificar esse return para um json correto
    else:
        raise HTTPException(
            status_code=404, detail="Disciplina não encontrada")


