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
    return {'status': 200, 'descrição': 'Sucesso', 'cacheability': 'False', 'tipo': 'lista'}, usuarios[usuario]

@app.post("/{usuario}")
async def cria_disciplina(usuario: str, disciplina: Disciplina):
    disciplina_adicionar, indice = achar_disciplina(usuarios, usuario, disciplina.nome) #pega disciplina correta
    if disciplina_adicionar is None:
        usuarios[usuario].append(disciplina)
        return {'status': 200, 'descrição': 'Criado', 'cacheability': 'False'}
    else: 
        raise HTTPException(status_code=406, detail="Essa Disciplina já existe")
    

@app.delete("/{usuario}/{disciplina}/")
def deleta_disciplina(usuario: str, disciplina: str):
    disciplina_deletar, indice = achar_disciplina(usuarios, usuario, disciplina) #pega disciplina correta
    if disciplina_deletar is not None:
        list_disc_usuario = usuarios[usuario] #pega lista de disciplinas do usuário
        list_disc_usuario.remove(disciplina_deletar) #deleta a disciplina
        return {'status': 200, 'descrição': 'deletado', 'cacheability': 'False'}
    else:
        raise HTTPException(status_code=404, detail="Disciplina não encontrada")

@app.put("/{usuario}/{disciplina}/")
async def modificar_item(usuario: str, disciplina: str, nova_disciplina: Disciplina):
    disciplina_atualizar, indice = achar_disciplina(usuarios, usuario, disciplina) #pega disciplina correta
    if disciplina_atualizar is not None:
        usuarios[usuario][indice] = nova_disciplina
        return {'status': 200, 'descrição': 'Atualizado', 'cacheability': 'False'}
    else:
        raise HTTPException(status_code=404, detail="Disciplina não encontrada")


@app.post("/{usuario}/{disciplina}")
async def adiciona_nota(usuario: str, disciplina: str, identifier: str, nota: float):
    disciplina_atualizar, indice = achar_disciplina(usuarios, usuario, disciplina) #pega disciplina correta
    if disciplina_atualizar is None:
        raise HTTPException(status_code=404, detail="Disciplina não encontrada")
    elif identifier in disciplina_atualizar.notas:
        raise HTTPException(status_code=406, detail="Identificador já existe")
    else:
        usuarios[usuario][indice].notas[identifier] = nota
        return {'status': 200, 'descrição': 'Adicionado', 'cacheability': 'False'}

@app.delete("/{usuario}/{disciplina}/{identifier}")
def deleta_nota(usuario: str, disciplina: str, identifier: str):
    disciplina_deletar, indice = achar_disciplina(usuarios, usuario, disciplina) #pega disciplina correta
    if disciplina_deletar is not None:
        list_disc_usuario = usuarios[usuario] #pega lista de disciplinas do usuário
        
        if identifier in list_disc_usuario[indice].notas:
            del list_disc_usuario[indice].notas[identifier]
            return {'status': 200, 'descrição': 'Deletado', 'cacheability': 'False'}    

    raise HTTPException(status_code=404, detail="Item não encontrado")


@app.get("/{usuario}/{disciplina}")
async def lista_notas_disciplina(usuario: str, disciplina: str):
    disciplina_notas, indice = achar_disciplina(usuarios, usuario, disciplina)
    if disciplina_notas is not None:
        list_disc_usuario = usuarios[usuario]
        return {'status': 200, 'descrição': 'Sucesso', 'cacheability': 'False', 'tipo': 'lista'},list_disc_usuario[indice].notas
    raise HTTPException(status_code=404, detail="Disciplina não encontrada") 

@app.put("/{usuario}/{disciplina}/{identifier}/{nota}")
async def modifica_nota(usuario: str, disciplina: str, identifier: str, nota: int):
    disciplina_atualizar, indice = achar_disciplina(usuarios, usuario, disciplina) #pega disciplina correta
    if disciplina_atualizar is not None:
        list_disc_usuario = usuarios[usuario]
        if identifier in list_disc_usuario[indice].notas:
            usuarios[usuario][indice].notas[identifier] = nota
            return {'status': 200, 'descrição': 'Atualizado', 'cacheability': 'False'} 
    raise HTTPException(status_code=404, detail="Item não encontrado")

