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


def criar_tabela_matricula():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        '''
        CREATE TABLE IF NOT EXISTS matricula(
        id INTEGER PRIMARY KEY,
        nome_disciplina TEXT,
        estudante_id INTEGER,
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
    conn.commit()
    conn.close()

