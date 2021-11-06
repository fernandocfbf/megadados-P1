from typing import Optional
from fastapi import FastAPI, Query, HTTPException
from pydantic import BaseModel, Field
from pydantic.fields import MAPPING_LIKE_SHAPES
from utils import *

app = FastAPI()

disciplinas = []

usuarios = {
    'fernando': [],
    'lais': [],
    'gabriela': []
}

class Disciplina(BaseModel):
    nome: str = Field(..., example="Megadados")
    prof: Optional[str] = Field(None, example="Fabio")
    anotacao: str = Field(..., example="Uma anotação legal")
    notas: Optional[dict] = Field({}, example={'PI': 10.0, 'PF': 7.6, 'AF': 3.4})

    class Config:
        schema_extra = {
            "example": {
                "nome": "Megadados",
                "prof": "Fabio",
                "anotacao": "Uma anotação legal",
                "notas": {
                    'PI': 10.0,
                    'PF': 7.6,
                    'AF': 3.4
                    }
            }
        }
    
@app.get("/{usuario}/")
async def lista_disciplinas(usuario: str):
    return usuarios[usuario]

@app.post("/{usuario}")
async def cria_disciplina(usuario: str, disciplina: Disciplina):
    usuarios[usuario].append(disciplina)
    return disciplina

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