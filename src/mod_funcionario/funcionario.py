from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO
from flask import send_file
from flask import Blueprint, render_template, request, redirect, url_for, jsonify
import requests
from funcoes import Funcoes
from settings import getHeadersAPI, ENDPOINT_FUNCIONARIO
from mod_login.login import validaToken

bp_funcionario = Blueprint('funcionario', __name__, url_prefix="/funcionario", template_folder='templates')

''' rotas dos formulários '''

@bp_funcionario.route('/', methods=['GET', 'POST'])
@validaToken
def formListaFuncionario():
    try:
        response = requests.get(ENDPOINT_FUNCIONARIO, headers=getHeadersAPI())
        result = response.json()

        print(result) # para teste
        print(response.status_code) # para teste

        if (response.status_code != 200):
            raise Exception(result)

        return render_template('formListaFuncionario.html', result=result[0])
    except Exception as e:
        return render_template('formListaFuncionario.html', msgErro=e.args[0])

@bp_funcionario.route('/insert', methods=['POST'])
def insert():
    try:
        # dados enviados via FORM
        id_funcionario = request.form['id']
        nome = request.form['nome']
        matricula = request.form['matricula']
        cpf = request.form['cpf']
        telefone = request.form['telefone']
        grupo = request.form['grupo']
        senha = Funcoes.get_password_hash(request.form['senha'])
        # monta o JSON para envio a API
        payload = {'id_funcionario': id_funcionario, 'nome': nome, 'matricula': matricula, 'cpf': cpf, 'telefone': telefone, 'grupo': grupo, 'senha': senha}
        # executa o verbo POST da API e armazena seu retorno
        response = requests.post(ENDPOINT_FUNCIONARIO, headers=getHeadersAPI(), json=payload)
        result = response.json()
        print(result) # [{'msg': 'Cadastrado com sucesso!', 'id': 13}, 200]
        print(response.status_code) # 200
        if (response.status_code != 200 or result[1] != 200):
            raise Exception(result)
        return redirect(url_for('funcionario.formListaFuncionario', msg=result[0]))
    except Exception as e:
        return render_template('formListaFuncionario.html', msgErro=e.args[0])

@bp_funcionario.route("/form-edit-funcionario", methods=['POST'])
def formEditFuncionario():
    try:
        # ID enviado via FORM
        id_funcionario = request.form['id']
        # executa o verbo GET da API buscando somente o funcionário selecionado,
        # obtendo o JSON do retorno
        response = requests.get(ENDPOINT_FUNCIONARIO + id_funcionario, headers=getHeadersAPI())
        result = response.json()
        if (response.status_code != 200):
            raise Exception(result)
        # renderiza o form passando os dados retornados
        return render_template('formFuncionario.html', result=result[0])
    except Exception as e:
        return render_template('formListaFuncionario.html', msgErro=e.args[0])

@bp_funcionario.route('/edit', methods=['POST'])
def edit():
    try:
        # dados enviados via FORM
        id_funcionario = request.form['id']
        nome = request.form['nome']
        matricula = request.form['matricula']
        cpf = request.form['cpf']
        telefone = request.form['telefone']
        grupo = request.form['grupo']
        senha = request.form['senha']
        # monta o JSON para envio a API
        payload = {'id_funcionario': id_funcionario, 'nome': nome, 'matricula': matricula, 'cpf': cpf, 'telefone': telefone, 'grupo':
        grupo, 'senha': senha}
        # executa o verbo PUT da API e armazena seu retorno
        response = requests.put(ENDPOINT_FUNCIONARIO + id_funcionario, headers=getHeadersAPI(), json=payload)
        result = response.json()
        if (response.status_code != 200 or result[1] != 200):
            raise Exception(result)
        return redirect(url_for('funcionario.formListaFuncionario', msg=result[0]))
    except Exception as e:
        return render_template('formListaFuncionario.html', msgErro=e.args[0])

@bp_funcionario.route('/delete', methods=['POST'])
def delete():
    try:
        # dados enviados via FORM
        id_funcionario = request.form['id']
        # executa o verbo DELETE da API e armazena seu retorno
        response = requests.delete(ENDPOINT_FUNCIONARIO + id_funcionario, headers=getHeadersAPI())
        result = response.json()

        if (response.status_code != 200 or result[1] != 200):
            raise Exception(result)
        return jsonify(erro=False, msg=result[0])
    except Exception as e:
        return jsonify(erro=True, msgErro=e.args[0])

@bp_funcionario.route('/form-funcionario/', methods=['POST'])
def formFuncionario():
    return render_template('formFuncionario.html')

@bp_funcionario.route('/gerar-pdf', methods=['POST'])
def gerar_pdf():
    try:
        response = requests.get(ENDPOINT_FUNCIONARIO, headers=getHeadersAPI())
        result = response.json()

        if response.status_code != 200:
            raise Exception(result)

        buffer = BytesIO()
        c = canvas.Canvas(buffer, pagesize=letter)
        width, height = letter

        c.drawString(30, height - 40, "Relatório de Funcionários")
        c.drawString(30, height - 60, "ID, Nome, Matrícula, CPF, Telefone, Grupo")

        y = height - 80
        for row in result[0]:
            text = f"{row['id_funcionario']}, {row['nome']}, {row['matricula']}, {row['cpf']}, {row['telefone']}, {row['grupo']}"
            c.drawString(30, y, text)
            y -= 20
            if y < 40:
                c.showPage()
                y = height - 40

        c.save()
        buffer.seek(0)
        return send_file(buffer, as_attachment=True, download_name="relatorio_funcionarios.pdf", mimetype='application/pdf')
    except Exception as e:
        return render_template('formListaFuncionario.html', msgErro=e.args[0])