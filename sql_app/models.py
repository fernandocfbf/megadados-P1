from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import Float
from .database import Base

class User(Base):
    __tablename__ = "users"
    id_usuario = Column(String, primary_key=True, index=True)
    nome = Column(String, unique=False, index=False)

    #relacionamentos
    disciplinas = relationship("Disciplina", back_populates="usuario")

class Disciplina(Base):
    __tablename__ = "disciplina"
    id_disciplina = Column(Integer, primary_key=True, index=True)
    id_usuario = Column(String, ForeignKey("users.id_usuario"))
    nome = Column(String)
    prof = Column(String)
    anotacao = Column(String)
    
    #relacionamentos
    usuario = relationship("User", back_populates="disciplinas")
    nota = relationship("Nota", back_populates="disciplina")


class Nota(Base):
    __tablename__ = "nota"
    id_nota = Column(Integer, primary_key=True, index=True)
    id_disciplina = Column(Integer, ForeignKey("users.id_usuario"))
    identificador = Column(String)
    nota = Column(Float)

    #relacionamentos
    disciplina = relationship("Disciplina", back_populates="nota")