import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

def conectar():
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
            nome TEXT NOT NULL,           -- 1
            jogador TEXT,                -- 2
            raca TEXT NOT NULL,           -- 3
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

# Adicionei inventario e habilidades aqui para evitar erros de coluna
def inserir_personagem(nome, jogador, raca, classe, origem, nivel, hp, forca, destreza, constituicao, inteligencia, sabedoria, carisma, ca, aparencia, personalidade, historico, objetivo, imagem):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO personagem (
            nome, jogador, raca, classe, origem, nivel, hp, forca, destreza, constituicao, 
            inteligencia, sabedoria, carisma, ca, aparencia, personalidade, historico, objetivo, imagem, inventario, habilidades
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, '', '')
    """, (nome, jogador, raca, classe, origem, nivel, hp, forca, destreza, constituicao, inteligencia, sabedoria, carisma, ca, aparencia, personalidade, historico, objetivo, imagem))
    conn.commit()
    cursor.close()
    conn.close()

def listar_personagens():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM personagem ORDER BY id DESC") # Order para os novos aparecerem primeiro
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

# Esta função agora é completa, caso você precise salvar um formulário inteiro no futuro
def atualizar_personagem(id, nome, classe, nivel, hp, forca, destreza, constituicao, inteligencia, sabedoria, carisma, ca, aparencia, personalidade, historico, objetivo, inventario, habilidades):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE personagem
        SET nome = %s, classe = %s, nivel = %s, hp = %s, forca = %s, destreza = %s, 
            constituicao = %s, inteligencia = %s, sabedoria = %s, carisma = %s, ca = %s,
            aparencia = %s, personalidade = %s, historico = %s, objetivo = %s, inventario = %s, habilidades = %s
        WHERE id = %s
    """, (nome, classe, nivel, hp, forca, destreza, constituicao, inteligencia, sabedoria, carisma, ca, aparencia, personalidade, historico, objetivo, inventario, habilidades, id))
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