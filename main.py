from typing import Optional, List
from fastapi import FastAPI, Query, HTTPException, Depends
from sqlalchemy.orm import Session

from sql_app import crud, models, schemas
from sql_app.database import SessionLocal, engine

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

@app.post("/usuario")
async def cria_usuario(usuario: schemas.CriaUsuario, db: Session = Depends(get_db)):

    #verifica se disciplina já existe
    db_usuario = crud.pega_usuario(db, nome=usuario.nome, id_usuario=usuario.id_usuario)
    if db_usuario:
         raise HTTPException(status_code=404, detail="Usuario já registrado")
    else:
        crud.cria_usuario(db, usuario=usuario)
        return usuario

@app.post("/{disciplina_}")
async def cria_disciplina_rota(disciplina: schemas.CriaDisciplina, db: Session = Depends(get_db)):

    #verifica se disciplina já existe
    db_disciplina = crud.pega_disciplina(db, nome=disciplina.nome, id_usuario=disciplina.id_usuario)
    if db_disciplina:
         raise HTTPException(status_code=404, detail="Disciplina já registrada")
    else:
        crud.cria_disciplina(db, disciplina=disciplina)
        return disciplina
    
'''
@app.delete("/{usuario}/{disciplina}/")
def deleta_disciplina(usuario: str, disciplina: str):
    disciplina_deletar, indice = achar_disciplina(usuarios, usuario, disciplina) #pega disciplina correta
    if disciplina_deletar is not None:
        list_disc_usuario = usuarios[usuario] #pega lista de disciplinas do usuário
        list_disc_usuario.remove(disciplina_deletar) #deleta a disciplina
        return {'status': 200, 'descrição': 'deletado'}
    else:
        raise HTTPException(status_code=404, detail="Item not found")

@app.put("/{usuario}/{disciplina}/")
async def update_item(usuario: str, disciplina: str, nova_disciplina: Disciplina):
    disciplina_atualizar, indice = achar_disciplina(usuarios, usuario, disciplina) #pega disciplina correta
    usuarios[usuario][indice] = nova_disciplina
    return {'status': 200, 'descrição': 'atualizado'}

@app.post("/{usuario}/{disciplina}")
async def adiciona_nota(usuario: str, disciplina: str, identifier: str, nova_nota: float):
    disciplina_atualizar, indice = achar_disciplina(usuarios, usuario, disciplina) #pega disciplina correta
    if disciplina_atualizar is None:
        raise HTTPException(status_code=404, detail="Item not found")
    elif identifier in disciplina_atualizar.notas:
        raise HTTPException(status_code=404, detail="Identifier already exists")
    else:
        usuarios[usuario][indice].notas[identifier] = nova_nota
        return {'status': 200, 'descrição': 'adicionado'}

@app.delete("/{usuario}/{disciplina}/{nota}")
def deleta_disciplina(usuario: str, disciplina: str, nota: str):
    disciplina_deletar, indice = achar_disciplina(usuarios, usuario, disciplina) #pega disciplina correta
    if disciplina_deletar is not None:
        list_disc_usuario = usuarios[usuario] #pega lista de disciplinas do usuário
        
        if nota in list_disc_usuario[indice].notas:
            del list_disc_usuario[indice].notas[nota]
            return {'status': 200, 'descrição': 'deletado'}
    raise HTTPException(status_code=404, detail="Item not found")
'''