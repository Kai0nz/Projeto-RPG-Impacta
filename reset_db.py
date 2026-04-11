from database import conectar

def resetar():
    try:
        conn = conectar()
        cursor = conn.cursor()
        # O comando CASCADE garante que tudo ligado à tabela também seja removido
        cursor.execute("DROP TABLE IF EXISTS personagem CASCADE;")
        conn.commit()
        cursor.close()
        conn.close()
        print("✅ Sucesso: Tabela 'personagem' apagada!")
        print("ℹ️ Agora, ao rodar o app.py, a nova estrutura será criada.")
    except Exception as e:
        print(f"❌ Erro ao resetar: {e}")

if __name__ == "__main__":
    resetar()