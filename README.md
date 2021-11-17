# Projeto 1 - Megadados - Projeto SQL
## Integrantes:
Fernando Fincatti

Gabriela Moreno Boriero

Lais Nascimento

## Instalação:
$ pip install fastapi

$ pip install "uvicorn[standard]"

$ pip install sqlalchemy_utils

$ pip install pymysql

## Rodar:
$ uvicorn main:app --reload

## Acessar via browser:
http://127.0.0.1:8000/docs#/

## Tables:
### User:
| id_usuario | nome |
| :---: | :---: | 
| String | String |

### Disciplina:
| id_disciplina | id_usuario | nome | prof | anotacao|
| :---: | :---: |  :---: | :---: | :---: | 
| Int | String |String |String |String |

### Nota:
| id_nota | id_disciplina | identificador | nota |
| :---: | :---: |  :---: | :---: | 
| Int | Int |String |Float|
