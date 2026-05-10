from flask import Flask, render_template, request, redirect, jsonify
import os
from werkzeug.utils import secure_filename
from database import (criar_tabela, inserir_personagem, listar_personagens, 
                      buscar_personagem, deletar_personagem, conectar)

app = Flask(__name__)

UPLOAD_FOLDER = "static/uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Garante que a tabela exista ao iniciar
criar_tabela()

@app.route("/")
def index():
    personagens = listar_personagens()
    return render_template("index.html", personagens=personagens)

@app.route("/adicionar", methods=["POST"])
def adicionar():
    nome = request.form["nome"]
    jogador = request.form["jogador"]
    raca = request.form["raca"]
    classe = request.form["classe"]
    origem = request.form["origem"]

    aparencia = request.form.get("aparencia", "")
    personalidade = request.form.get("personalidade", "")
    historico = request.form.get("historico", "")
    objetivo = request.form.get("objetivo", "")

    inserir_personagem(
        nome, jogador, raca, classe, origem,
        1, 10,  # nível e HP padrão
        10, 10, 10, 10, 10, 10,  # atributos padrão
        10,  # CA padrão
        aparencia, personalidade, historico, objetivo,
        ""  # imagem vazia inicial
    )
    return redirect("/")

@app.route("/personagem/<int:id>")
def detalhes(id):
    personagem = buscar_personagem(id)
    return render_template("detalhes.html", personagem=personagem)

@app.route("/upload_foto/<int:id>", methods=["POST"])
def upload_foto(id):
    if "foto" not in request.files:
        return redirect(f"/personagem/{id}")

    file = request.files["foto"]
    if file.filename == "":
        return redirect(f"/personagem/{id}")

    filename = secure_filename(file.filename)
    caminho = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    file.save(caminho)

    caminho_salvar = "/static/uploads/" + filename

    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("UPDATE personagem SET imagem = %s WHERE id = %s", (caminho_salvar, id))
    conn.commit()
    cursor.close()
    conn.close()

    return redirect(f"/personagem/{id}")

@app.route("/deletar/<int:id>")
def deletar(id):
    deletar_personagem(id)
    return redirect("/")

@app.route("/editar_campo", methods=["POST"])
def editar_campo():
    dados = request.get_json()
    id_personagem = dados["id"]
    campo = dados["campo"]
    valor = dados["valor"]

    campos_permitidos = [
        "nome", "jogador", "raca", "classe", "origem", "nivel", "hp",
        "forca", "destreza", "constituicao", "inteligencia", "sabedoria", "carisma",
        "ca", "aparencia", "personalidade", "historico", "objetivo", "inventario", "habilidades"
    ]

    if campo not in campos_permitidos:
        return jsonify({"status": "erro", "message": "Campo inválido"}), 400

    conn = conectar()
    cursor = conn.cursor()
    try:
        query = f"UPDATE personagem SET {campo} = %s WHERE id = %s"
        cursor.execute(query, (valor, id_personagem))
        conn.commit()
        return jsonify({"status": "ok"})
    except Exception as e:
        print(f"Erro ao salvar: {e}")
        return jsonify({"status": "erro"}), 500
    finally:
        cursor.close()
        conn.close()

# O app.run deve ser sempre a última coisa do arquivo
if __name__ == "__main__":
    app.run(debug=True)