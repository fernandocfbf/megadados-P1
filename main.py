from typing import Optional
from fastapi import FastAPI, Query, HTTPException
from pydantic import BaseModel, Field
from pydantic.fields import MAPPING_LIKE_SHAPES
from utils import *
from uuid import uuid4

app = FastAPI()

print( "Exemplo _> ", str(uuid4()))

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
    notas: Optional[list] = Field([], example=[9.0, 10.0, 5.6])

    class Config:
        schema_extra = {
            "example": {
                "nome": "Megadados",
                "prof": "Fabio",
                "anotacao": "Uma anotação legal",
                "notas": [3.0, 6.0, 9.0, 3.5]
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
