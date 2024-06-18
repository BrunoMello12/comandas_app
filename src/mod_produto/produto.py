from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO
from flask import send_file
from flask import send_file
from flask import Blueprint, render_template, request, jsonify
import requests
import base64
from mod_login.login import validaToken
from settings import getHeadersAPI, ENDPOINT_PRODUTO

bp_produto = Blueprint('produto', __name__, url_prefix="/produto", template_folder='templates')

@bp_produto.route('/insert', methods=['POST'])
@validaToken
def insert():
    try:
        id_produto = request.form['id']
        nome = request.form['nome']
        descricao = request.form['descricao']
        valor_unitario = request.form['valor_unitario']
        foto = "data:" + request.files['foto'].content_type + ";base64," + str(base64.b64encode(request.files['foto'].read()), "utf-8")
        payload = {'id_produto': id_produto, 'nome': nome, 'descricao': descricao, 'foto': foto, 'valor_unitario': valor_unitario}
        response = requests.post(ENDPOINT_PRODUTO, headers=getHeadersAPI(), json=payload)
        result = response.json()
        if response.status_code != 200 or result[1] != 200:
            raise Exception(result)
        return jsonify(erro=False, msg=result[0])
    except Exception as e:
        return jsonify(erro=True, msgErro=e.args[0])

@bp_produto.route('/edit', methods=['POST'])
@validaToken
def edit():
    try:
        id_produto = request.form['id']
        nome = request.form['nome']
        descricao = request.form['descricao']
        valor_unitario = request.form['valor_unitario']
        foto = "data:" + request.files['foto'].content_type + ";base64," + str(base64.b64encode(request.files['foto'].read()), "utf-8")
        payload = {'id_produto': id_produto, 'nome': nome, 'descricao': descricao, 'foto': foto, 'valor_unitario': valor_unitario}
        response = requests.put(ENDPOINT_PRODUTO + id_produto, headers=getHeadersAPI(), json=payload)
        result = response.json()
        if response.status_code != 200 or result[1] != 200:
            raise Exception(result)
        return jsonify(erro=False, msg=result[0])
    except Exception as e:
        return jsonify(erro=True, msgErro=e.args[0])

@bp_produto.route('/delete', methods=['POST'])
@validaToken
def delete():
    try:
        id_produto = request.form['id_produto']
        response = requests.delete(ENDPOINT_PRODUTO + id_produto, headers=getHeadersAPI())
        result = response.json()
        if response.status_code != 200 or result[1] != 200:
            raise Exception(result)
        return jsonify(erro=False, msg=result[0])
    except Exception as e:
        return jsonify(erro=True, msgErro=e.args[0])

@bp_produto.route('/form-produto/', methods=['GET', 'POST'])
@validaToken
def formProduto():
    return render_template('formProduto.html')

@bp_produto.route('/form-edit-produto', methods=['POST','GET'])
@validaToken
def formEditProduto():
    try:
        id_produto = request.form['id']
        response = requests.get(ENDPOINT_PRODUTO + id_produto, headers=getHeadersAPI())
        result = response.json()
        if response.status_code != 200:
            raise Exception(result)
        return render_template('formProduto.html', result=result[0])
    except Exception as e:
        return render_template('formListaProduto.html', msgErro=e.args[0])

# Adicionando a rota faltante
@bp_produto.route('/form-lista-produto', methods=['GET'])
@validaToken
def formListaProduto():
    try:
        response = requests.get(ENDPOINT_PRODUTO, headers=getHeadersAPI())
        result = response.json()

        print(result) # para teste
        print(response.status_code) # para teste

        if (response.status_code != 200):
            raise Exception(result)

        return render_template('formListaProduto.html', result=result[0])
    except Exception as e:
        return render_template('formListaProduto.html', msgErro=e.args[0])

@bp_produto.route('/gerar_pdf', methods=['POST'])
@validaToken
def gerar_pdf():
    try:
        response = requests.get(ENDPOINT_PRODUTO, headers=getHeadersAPI())
        result = response.json()

        if response.status_code != 200:
            raise Exception(result)

        buffer = BytesIO()
        pdf = canvas.Canvas(buffer, pagesize=letter)
        pdf.setTitle("Lista de Produtos")
        pdf.drawString(100, 750, "Lista de Produtos")

        y = 720
        for produto in result[0]:
            pdf.drawString(100, y, f"ID: {produto['id_produto']}, Nome: {produto['nome']}, Descrição: {produto['descricao']}, Valor: {produto['valor_unitario']}")
            y -= 20

        pdf.save()
        buffer.seek(0)
        return send_file(buffer, as_attachment=True, download_name='produtos.pdf', mimetype='application/pdf')
    except Exception as e:
        return render_template('formListaProduto.html', msgErro=e.args[0])

