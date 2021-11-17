from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import Float
from database import Base

class User(Base):
    __tablename__ = "users"
    id_usuario = Column(String(45), primary_key=True, index=True)
    nome = Column(String(45), unique=False, index=False)

    #relacionamentos
    disciplinas = relationship("Disciplina", back_populates="usuario")

class Disciplina(Base):
    __tablename__ = "disciplina"
    id_disciplina = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id_usuario = Column(String(45), ForeignKey("users.id_usuario"))
    nome = Column(String(45))
    prof = Column(String(45))
    anotacao = Column(String(100))
    
    #relacionamentos
    usuario = relationship("User", back_populates="disciplinas")
    nota = relationship("Nota", back_populates="disciplina")


class Nota(Base):
    __tablename__ = "nota"
    id_nota = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id_disciplina = Column(Integer, ForeignKey("disciplina.id_disciplina"))
    identificador = Column(String(45))
    nota = Column(Float)

    #relacionamentos
    disciplina = relationship("Disciplina", back_populates="nota")