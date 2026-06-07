from pathlib import Path

from flask import Flask, redirect, render_template, request, url_for
from werkzeug.datastructures import FileStorage

from database import get_connection, init_db

app = Flask(__name__)

UPLOAD_FOLDER = Path("static/uploads")
UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)


@app.route("/")
def home() -> str:
    with get_connection() as conn:
        planos = conn.execute(
            "SELECT * FROM planos WHERE ativo = 1 ORDER BY id DESC"
        ).fetchall()

    return render_template("index.html", planos=planos)


@app.route("/adm", methods=["GET", "POST"])
def admin() -> str:
    if request.method == "POST":
        operadora = request.form["operadora"]
        titulo = request.form["titulo"]
        descricao = request.form["descricao"]
        faixa_etaria = request.form["faixa_etaria"]
        valor = request.form["valor"]

        imagem_file: FileStorage | None = request.files.get("imagem")
        imagem_nome: str | None = None

        if imagem_file and imagem_file.filename:
            imagem_nome = imagem_file.filename
            imagem_file.save(UPLOAD_FOLDER / imagem_nome)

        with get_connection() as conn:
            conn.execute(
                """
                INSERT INTO planos
                (operadora, titulo, descricao, faixa_etaria, valor, imagem)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (operadora, titulo, descricao, faixa_etaria, valor, imagem_nome),
            )
            conn.commit()

        return redirect(url_for("admin"))

    with get_connection() as conn:
        planos = conn.execute(
    """
    SELECT * FROM planos
    WHERE ativo = 1
    ORDER BY id DESC
    """
).fetchall()

    return render_template("admin.html", planos=planos)


@app.route("/adm/desativar/<int:plano_id>")
def desativar_plano(plano_id: int) -> str:
    with get_connection() as conn:
        conn.execute("UPDATE planos SET ativo = 0 WHERE id = ?", (plano_id,))
        conn.commit()

    return redirect(url_for("admin"))


if __name__ == "__main__":
    init_db()
    app.run(debug=True)