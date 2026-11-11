import sqlite3

def conectar():
    conn = sqlite3.connect('escola.db')
    return conn

def criar_tabela_estudantes():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        '''
        CREATE TABLE IF NOT EXISTS estudantes(
        id INTEGER PRIMARY KEY,
        nome TEXT,
        idade INTEGER)
        '''
    )
    conn.commit()
    conn.close()


def criar_tabela_matriculas():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        '''
        CREATE TABLE IF NOT EXISTS matriculas(
        id INTEGER PRIMARY KEY,
        nome_disciplina TEXT,
        estudante_id INTEGER,
        FOREIGN KEY (estudante_id) REFERENCES estudantes(id))
        '''
    )
    conn.commit()
    conn.close()


def criar_estudante(nome, idade):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        '''
        INSERT INTO estudantes (nome, idade) \
        VALUES (?, ?)
        ''', (nome, idade)
    )
    conn.commit()
    conn.close()


def listar_estudantes():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        '''
        SELECT * FROM estudantes
        '''
    )
    estudantes = cursor.fetchall()
    for estudante in estudantes:
        print(estudante)
    conn.close()


if __name__ == '__main__':
    criar_tabela_estudantes()
    criar_tabela_matriculas()
    criar_estudante('Ana', 20)
    criar_estudante('Bruno', 22)
    listar_estudantes()
    