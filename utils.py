def achar_disciplina(dicionario, usuario, disciplina):
    list_disc_usuario = dicionario[usuario]
    indice = 0
    for materia in list_disc_usuario:
        if materia.nome == disciplina:
            return materia, indice
        indice += 1
    return None