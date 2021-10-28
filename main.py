from typing import Optional
from fastapi import FastAPI, Query
from pydantic import BaseModel, Field

app = FastAPI()

disciplinas = []

class Disciplina(BaseModel):
    nome: str = Field(..., example="Megadados")
    prof: Optional[str] = Field(None, example="Fabio")
    anotacao: str = Field(..., example="Uma anotação legal")

    class Config:
        schema_extra = {
            "example": {
                "nome": "Megadados",
                "prof": "Fabio",
                "anotacao": "Uma anotação legal"
            }
        }
    

@app.post("/disciplinas/")
async def cria_disciplina(disciplina: Disciplina):
    disciplinas.append(disciplina)
    return disciplina

@app.get("/disciplinas/")
async def lista_disciplinas():
    return disciplinas