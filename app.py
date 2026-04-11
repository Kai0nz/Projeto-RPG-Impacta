from flask import Flask, render_template, request, redirect
import os
from werkzeug.utils import secure_filename
from database import criar_tabela, inserir_personagem, listar_personagens
from database import buscar_personagem
from database import atualizar_personagem
from database import deletar_personagem
from database import conectar

app = Flask(__name__)

UPLOAD_FOLDER = "static/uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

criar_tabela()

@app.route("/")
def index():
    personagens = listar_personagens()
    return render_template("index.html", personagens=personagens)


@app.route("/adicionar", methods=["POST"])
def adicionar():
    # Coleta os dados básicos
    nome = request.form["nome"]
    jogador = request.form["jogador"]
    raca = request.form["raca"]
    classe = request.form["classe"]
    origem = request.form["origem"]

    # Coleta os novos campos de 'Toques Finais'
    aparencia = request.form.get("aparencia", "")
    personalidade = request.form.get("personalidade", "")
    historico = request.form.get("historico", "")
    objetivo = request.form.get("objetivo", "")

    # CHAMA A FUNÇÃO COM TODOS OS ARGUMENTOS (Incluindo a imagem vazia no final)
    inserir_personagem(
        nome, jogador, raca, classe, origem,
        1, 10,  # nível e HP padrão
        10, 10, 10, 10, 10, 10,  # atributos padrão
        10,  # CA padrão
        aparencia, personalidade, historico, objetivo,
        ""  # <--- Aqui entra a imagem (vazia por enquanto)
    )

    return redirect("/")


@app.route("/personagem/<int:id>")
def detalhes(id):
    personagem = buscar_personagem(id)
    return render_template("detalhes.html", personagem=personagem)


@app.route("/editar/<int:id>")
def editar(id):
    personagem = buscar_personagem(id)
    return render_template("editar.html", personagem=personagem)


@app.route("/atualizar/<int:id>", methods=["POST"])
def atualizar(id):
    nome = request.form["nome"]
    classe = request.form["classe"]
    nivel = request.form["nivel"]
    hp = request.form["hp"]

    atualizar_personagem(id, nome, classe, nivel, hp)

    return redirect(f"/personagem/{id}")


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

    cursor.execute(
        "UPDATE personagem SET imagem = %s WHERE id = %s",
        (caminho_salvar, id)
    )

    conn.commit()
    cursor.close()
    conn.close()

    return redirect(f"/personagem/{id}")


@app.route("/deletar/<int:id>")
def deletar(id):
    deletar_personagem(id)
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)