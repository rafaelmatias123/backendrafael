from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from urllib.parse import unquote
from sqlalchemy.exc import IntegrityError
from sqlalchemy import asc
from flask import request

from model import Session, Encomenda

from schemas.encomenda import *
from schemas.error import ErrorSchema

from flask_cors import CORS


info = Info(title="minhaapi", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)
if __name__ == '__main__':
    app.run(debug=True)

# definindo tags
home_tag = Tag(name="Documentação",
               description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
encomenda_tag = Tag(
    name="Encomenda", description="Consultar, incluir e excluir a encomenda do cadastro")


@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi')

@app.post('/encomenda', tags=[encomenda_tag], 
          responses={"200": EncomendaViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_encomenda(form: EncomendaSchema):
    """Cadastra nova encomenda

    Retorna uma representação da encomenda cadastrado.
    """
    encomenda = Encomenda(
        nome=form.nome,
        casa=form.casa,
        quantidade_p=form.quantidade_p,
        pacote=form.pacote
    )

    try:
        session = Session()
        # adicionando encomenda
        session.add(encomenda)
        session.commit()
        return apresenta_encomenda(encomenda), 200

    except IntegrityError as e:
        session.rollback()
        msg = "Encomenda de'" + \
            encomenda.nome + "' já existente, verifique!"
        print(str(e))
        return {"mensagem": msg}, 409

    except Exception as e:
        session.rollback()
        msg = "Erro ao gravar a encomenda."
        print(str(e))
        return {"mensagem": msg}, 400


@app.get('/listar_encomendas', tags=[encomenda_tag],
         responses={"200": ListagemEncomendasSchema, "404": ErrorSchema})
def listar_encomendas():
    """Apresenta as encomendas cadastrados

    Retorna uma lista de encomendas.
    """
    # Crie uma sessão
    session = Session()

    # Consulta para obter todas as encomendas por data de validade
    encomendas = session.query(Encomenda).order_by(
        asc(Encomenda.nome)).all()

    # Feche a sessão
    # session.close()

    if not encomendas:
        # se não há encomendas cadastradas
        return {"encomendas": []}, 200
    else:
        # retorna a representação da encomenda
        return apresenta_encomendas(encomendas), 200


@app.delete('/encomenda', tags=[encomenda_tag],
            responses={"200": EncomendaDelSchema, "404": ErrorSchema})
def del_encomenda(query: EncomendaBuscaSchema):
    """Deleta uma encomenda a partir do nome informado

    Retorna uma mensagem de confirmação da remoção.
    """
    encomenda_nome = unquote(unquote(query.nome))

    # criando conexão com a base
    session = Session()

    # exclui a encomenda
    count = session.query(Encomenda).filter(
        Encomenda.nome == encomenda_nome).delete()

    session.commit()

    if count:
        # retorna a representação da mensagem de confirmação
        return {"mensagem": "encomenda removida", "nome": encomenda_nome}, 200
    else:
        # se a encomenda não foi encontrado
        return {"mensagem": "encomenda não existente!"}, 404
