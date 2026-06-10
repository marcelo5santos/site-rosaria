from pathlib import Path

from flask import Flask, redirect, render_template, request, url_for
from werkzeug.datastructures import FileStorage

from database import init_db
from models import (
    listar_planos_ativos,
    listar_planos_admin,
    criar_plano,
    desativar_plano_por_id,
)


app = Flask(__name__)

UPLOAD_FOLDER = Path("static/uploads")
UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)

init_db()


@app.route("/")
def index():
    planos = listar_planos_ativos()
    print("PLANOS ATIVOS:", planos)
    return render_template("index.html", planos=planos)


@app.route("/adm", methods=["GET", "POST"])
def admin():
    if request.method == "POST":
        operadora = request.form["operadora"]
        titulo = request.form["titulo"]
        descricao = request.form["descricao"]
        faixa_etaria = request.form["faixa_etaria"]
        valor = request.form["valor"]

        imagem_file: FileStorage | None = request.files.get("imagem")
        imagem_nome = None

        if imagem_file and imagem_file.filename:
            imagem_nome = imagem_file.filename
            imagem_file.save(UPLOAD_FOLDER / imagem_nome)

        criar_plano(
            operadora=operadora,
            titulo=titulo,
            descricao=descricao,
            faixa_etaria=faixa_etaria,
            valor=valor,
            imagem=imagem_nome,
        )

        return redirect(url_for("admin"))

    planos = listar_planos_admin()
    return render_template("admin.html", planos=planos)


@app.route("/adm/desativar/<int:plano_id>")
def desativar(plano_id):
    desativar_plano_por_id(plano_id)
    return redirect(url_for("admin"))


if __name__ == "__main__":
    app.run(debug=True)