from flask import Flask, render_template, request, redirect
from database import criar_tabela, inserir_personagem, listar_personagens
from database import buscar_personagem
from database import atualizar_personagem
from database import deletar_personagem

app = Flask(__name__)

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

    inserir_personagem(
        nome, jogador, raca, classe, origem,
        1, 10,  # nível e HP padrão

        10, 10, 10, 10, 10, 10,  # atributos padrão
        10,  # CA padrão

        "", "", "", ""  # aparencia, personalidade, historico, objetivo
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


@app.route("/deletar/<int:id>")
def deletar(id):
    deletar_personagem(id)
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)