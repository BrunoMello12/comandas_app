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
    return render_template('formListaProduto.html')

