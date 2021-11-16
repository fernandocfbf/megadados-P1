from typing import List, Optional
from pydantic import BaseModel

class CriaUsuario(BaseModel):
    id_usuario: str
    nome: str

class CriaDisciplina(BaseModel):
    id_disciplina: int  # colocar auto increment no futuro
    id_usuario: str
    nome: str
    prof: str
    anotacao: str

