from flask import Flask, render_template, redirect, url_for, request, flash
from sqlalchemy import select
from models import db_session, Jogador, Clube, Campeonato

app = Flask(__name__)

app.config['SECRET_KEY'] = 'secret!'


@app.route('/')
def index():
    return redirect('/base')


@app.route('/base')
def home():
    return render_template("base.html")


@app.route('/jogador', methods=['GET'])
def jogador_func():
    lista_jogador = select(Jogador)
    lista_jogador = db_session.execute(lista_jogador).scalars().all()
    result = [jogador.serialize_jogador() for jogador in lista_jogador]
    print('Nome dos jogadores:', result)
    return render_template("jogador.html", lista_jogador=result)


@app.route('/novo_jogador', methods=["POST", "GET"])
def cadastro_jogador():
    if request.method == "POST":
        campos_obrigatorios = ["form_nome", "form_sobrenome", "form_cpf", "form_numero", "form_id_clube"]

        for campo in campos_obrigatorios:
            if not request.form.get(campo):
                flash("Preencher todos os campos", "error")
                return redirect(url_for('cadastro_jogador'))

        try:
            novo_jogador = Jogador(
                nome=request.form["form_nome"],
                sobrenome=request.form["form_sobrenome"],
                cpf=request.form["form_cpf"],
                numero=int(request.form["form_numero"]),
                id_clube=int(request.form["form_id_clube"])
            )
            novo_jogador.save()
            flash("Jogador cadastrado com sucesso. Seja bem-vindo ao time!", "success")
            return redirect(url_for('jogador_func'))
        except Exception as e:
            flash(f"Erro ao cadastrar jogador: {str(e)}", "error")

    return render_template('novo_jogador.html')


@app.route('/clube', methods=["GET"])
def clube():
    lista_clube = select(Clube)
    lista_clube = db_session.execute(lista_clube).scalars().all()
    result = [clube.serialize_clube() for clube in lista_clube]
    return render_template('clube.html', lista=result)


@app.route('/novo_clube', methods=["POST", "GET"])
def cadastro_clube():
    if request.method == "POST":
        if not request.form.get("form_nome_clube"):
            flash("Preencher o nome do clube", "error")
            return redirect(url_for('cadastro_clube'))

        try:
            novo_clube = Clube(
                nome_clube=request.form["form_nome_clube"]
            )
            novo_clube.save()
            flash("Clube cadastrado com sucesso!", "success")
            return redirect(url_for('clube'))
        except Exception as e:
            flash(f"Erro ao cadastrar clube: {str(e)}", "error")

    return render_template('novo_clube.html')


@app.route('/campeonato', methods=["GET"])
def campeonato():
    lista_campeonato = select(Campeonato)
    lista_campeonato = db_session.execute(lista_campeonato).scalars().all()
    result = [camp.serialize_campeonato() for camp in lista_campeonato]
    return render_template('capeonatos.html', lista=result)


@app.route('/novo_campeonato', methods=["POST", "GET"])
def cadastro_campeonato():
    if request.method == "POST":
        if not request.form.get("form_nome_campeonato") or not request.form.get("form_descricao_campeonato"):
            flash("Preencher todos os campos", "error")
            return redirect(url_for('cadastro_campeonato'))

        try:
            novo_campeonato = Campeonato(
                nome_campeonato=request.form["form_nome_campeonato"],
                descricao_campeonato=request.form["form_descricao_campeonato"]
            )
            novo_campeonato.save()
            flash("Campeonato cadastrado com sucesso!", "success")
            return redirect(url_for('campeonato'))
        except Exception as e:
            flash(f"Erro ao cadastrar campeonato: {str(e)}", "error")

    return render_template('novo_campeonato.html')


if __name__ == '__main__':
    app.run(debug=True)
