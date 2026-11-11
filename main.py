from db import (
    criar_tabela_estudantes,
    criar_tabela_matriculas,
    criar_estudante,
    criar_matricula,
    listar_estudantes,
    listar_matriculas,
)

if __name__ == '__main__':
    criar_tabela_estudantes()
    criar_tabela_matriculas()
    criar_estudante('Ana', 20)
    criar_estudante('Bruno', 22)
    criar_matricula(1, 'Matemática')
    criar_matricula(2, 'História')
    listar_estudantes()
    listar_matriculas()