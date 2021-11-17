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
