from flask import Flask, session
import os
from settings import HOST, PORT, DEBUG
from flask import Flask, render_template
from mod_funcionario.funcionario import bp_funcionario
from mod_index.index import bp_index
from mod_cliente.cliente import bp_cliente
from mod_produto.produto import bp_produto
from mod_login.login import bp_login
from mod_erro.erro import bp_erro

#BRUNO VINICIUS MELLO

app = Flask(__name__)

# gerando uma chave randômica para secret_key
app.secret_key = os.urandom(12).hex()

# registro das rotas do blueprint
app.register_blueprint(bp_funcionario)
app.register_blueprint(bp_index)
app.register_blueprint(bp_cliente)
app.register_blueprint(bp_produto)
app.register_blueprint(bp_login)
app.register_blueprint(bp_erro)

if __name__ == "__main__":
    """ Inicia o aplicativo WEB Flask """
    app.run(host=HOST, port=PORT, debug=DEBUG)