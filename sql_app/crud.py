from sqlalchemy.orm import Session
import models
import schemas


def cria_disciplina(db: Session, disciplina: schemas.CriaDisciplina):
    db_disciplina = models.Disciplina(
        id_usuario=disciplina.id_usuario,
        nome=disciplina.nome,
        prof=disciplina.prof,
        anotacao=disciplina.anotacao,
    )
    db.add(db_disciplina)
    db.commit()
    db.refresh(db_disciplina)
    return db_disciplina


def pega_disciplina(db: Session, nome: str, id_usuario: str):
    return db.query(models.Disciplina).filter(
        models.Disciplina.nome == nome,
        models.Disciplina.id_usuario == id_usuario).first()


def lista_disciplinas(db: Session, id_usuario: str):
    return db.query(models.Disciplina.nome).filter(
        models.Disciplina.id_usuario == id_usuario).all()


def deleta_disciplina(db: Session, disciplina: schemas.DeletaDisciplina):
    db_disciplina = db.query(models.Disciplina).filter(
        models.Disciplina.nome == disciplina.nome,
        models.Disciplina.id_usuario == disciplina.id_usuario)
    db_disciplina.delete()
    db.commit()
    return db_disciplina


def atualiza_disciplina(db: Session, disciplina_atualizar: schemas.EncontraDisciplina, disciplina: schemas.AtualizaDisciplina):
    db_disciplina = db.query(models.Disciplina).filter(
        models.Disciplina.nome == disciplina_atualizar.nome,
        models.Disciplina.id_usuario == disciplina_atualizar.id_usuario)
    db_disciplina.update({
        'nome': disciplina.nome,
        'prof': disciplina.prof,
        'anotacao': disciplina.anotacao
    })
    db.commit()

def cria_usuario(db: Session, usuario: schemas.CriaUsuario):
    db_usuario = models.User(
        id_usuario=usuario.id_usuario,
        nome=usuario.nome,
    )
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario


def pega_usuario(db: Session, id_usuario: str):
    return db.query(models.User).filter(
        models.User.id_usuario == id_usuario).first()


def lista_usuarios(db: Session):
    return db.query(models.User).all()

def id_pega_disciplina(db: Session, id_disciplina: int):
    return db.query(models.Disciplina).filter(
        models.Disciplina.id_disciplina== id_disciplina).first()

def cria_nota(db: Session, nota: schemas.CriaNota):
    db_nota = models.Nota(
        id_nota= nota.id_nota,
        id_disciplina= nota.id_disciplina,
        identificador= nota.identificador,
        nota= nota.nota
    )
    db.add(db_nota)
    db.commit()
    db.refresh(db_nota)
    return db_nota

def pega_nota(db: Session, id_disciplina: int, identificador: str):
    return db.query(models.Nota).filter(
        models.Nota.id_disciplina == id_disciplina,
        models.Nota.identificador == identificador).first()

def lista_notas(db: Session, id_disciplina: int):
    return db.query(models.Nota).filter(
        models.Nota.id_disciplina == id_disciplina).all()

def deleta_nota(db: Session, id_disciplina: int, identificador: str):
    db_nota= db.query(models.Nota).filter(
        models.Nota.id_disciplina == id_disciplina,
        models.Nota.identificador == identificador).first()

    db.delete(db_nota)
    db.commit()
    return "deletado"

def pega_notas(db: Session, id_nota: int):
    return db.query(models.Nota).filter(
        models.Nota.id_nota == id_nota).first()

def atualiza_nota(db: Session, nota: float , nota_id: int):
    db_nota = db.query(models.Nota).filter(
        models.Nota.id_nota == nota_id)
    db_nota.update({
        'nota': nota,
    })
    db.commit()