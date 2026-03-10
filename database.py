import psycopg2

def conectar():
    conn = psycopg2.connect(
        host="localhost",
        database="rpg_site",
        user="postgres",
        password="1001"
    )
    return conn


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
    conn.close()


def inserir_personagem(
    nome, jogador, raca, classe, origem,
    nivel, hp,
    forca, destreza, constituicao,
    inteligencia, sabedoria, carisma,
    ca,
    aparencia, personalidade, historico, objetivo
):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO personagem (
            nome, jogador, raca, classe, origem,
            nivel, hp,
            forca, destreza, constituicao,
            inteligencia, sabedoria, carisma,
            ca,
            aparencia, personalidade, historico, objetivo
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        nome, jogador, raca, classe, origem,
        nivel, hp,
        forca, destreza, constituicao,
        inteligencia, sabedoria, carisma,
        ca,
        aparencia, personalidade, historico, objetivo
    ))

    conn.commit()
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
    conn.close()


def deletar_personagem(id):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM personagem WHERE id = %s", (id,))
    
    conn.commit()
    conn.close()