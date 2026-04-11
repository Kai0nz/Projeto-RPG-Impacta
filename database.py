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
            id SERIAL PRIMARY KEY,        -- 0
            nome TEXT NOT NULL,          -- 1
            jogador TEXT,                -- 2
            raca TEXT NOT NULL,          -- 3
            classe TEXT NOT NULL,        -- 4
            origem TEXT NOT NULL,        -- 5
            nivel INTEGER NOT NULL,      -- 6
            hp INTEGER NOT NULL,         -- 7
            forca INTEGER,               -- 8
            destreza INTEGER,            -- 9
            constituicao INTEGER,        -- 10
            inteligencia INTEGER,        -- 11
            sabedoria INTEGER,           -- 12
            carisma INTEGER,             -- 13
            ca INTEGER,                  -- 14
            aparencia TEXT,              -- 15
            personalidade TEXT,          -- 16
            historico TEXT,              -- 17
            objetivo TEXT,               -- 18
            imagem TEXT,                 -- 19
            inventario TEXT,             -- 20
            habilidades TEXT             -- 21
        )
    """)
    conn.commit()
    cursor.close()
    conn.close()

def inserir_personagem(nome, jogador, raca, classe, origem, nivel, hp, forca, destreza, constituicao, inteligencia, sabedoria, carisma, ca, aparencia, personalidade, historico, objetivo, imagem):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO personagem (
            nome, jogador, raca, classe, origem, nivel, hp, forca, destreza, constituicao, 
            inteligencia, sabedoria, carisma, ca, aparencia, personalidade, historico, objetivo, imagem
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s)
    """, (nome, jogador, raca, classe, origem, nivel, hp, forca, destreza, constituicao, inteligencia, sabedoria, carisma, ca, aparencia, personalidade, historico, objetivo, imagem))
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