import os
import psycopg2
from dotenv import load_dotenv

# Carrega as variáveis do arquivo .env
load_dotenv()

def conectar():
    # Conecta ao PostgreSQL usando credenciais escondidas no .env
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )

def criar_tabela():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS personagem (
            id SERIAL PRIMARY KEY,
            nome TEXT NOT NULL,
            jogador TEXT,
            raca TEXT NOT NULL,
            classe TEXT NOT NULL,
            origem TEXT NOT NULL,
            nivel INTEGER NOT NULL,
            hp INTEGER NOT NULL,
            forca INTEGER,
            destreza INTEGER,
            constituicao INTEGER,
            inteligencia INTEGER,
            sabedoria INTEGER,
            carisma INTEGER,
            ca INTEGER,
            aparencia TEXT,
            personalidade TEXT,
            historico TEXT,
            objetivo TEXT
        )
    """)
    conn.commit()
    cursor.close()
    conn.close()

def inserir_personagem(nome, jogador, raca, classe, origem, nivel, hp, forca, destreza, constituicao, inteligencia, sabedoria, carisma, ca, aparencia, personalidade, historico, objetivo):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO personagem (
            nome, jogador, raca, classe, origem, nivel, hp, forca, destreza, constituicao, 
            inteligencia, sabedoria, carisma, ca, aparencia, personalidade, historico, objetivo
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (nome, jogador, raca, classe, origem, nivel, hp, forca, destreza, constituicao, inteligencia, sabedoria, carisma, ca, aparencia, personalidade, historico, objetivo))
    conn.commit()
    cursor.close()
    conn.close()

def listar_personagens():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM personagem")
    personagens = cursor.fetchall()
    conn.close()
    return personagens

def buscar_personagem(id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM personagem WHERE id = %s", (id,))
    personagem = cursor.fetchone()
    conn.close()
    return personagem

def atualizar_personagem(id, nome, classe, nivel, hp):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE personagem
        SET nome = %s, classe = %s, nivel = %s, hp = %s
        WHERE id = %s
    """, (nome, classe, nivel, hp, id))
    conn.commit()
    cursor.close()
    conn.close()

def deletar_personagem(id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM personagem WHERE id = %s", (id,))
    conn.commit()
    cursor.close()
    conn.close()