from pydantic import BaseModel
from typing import List
from model.encomenda import Encomenda


class EncomendaSchema(BaseModel):
    """ Define como uma nova encomenda a ser inserida deve ser representada """
    nome: str = "Rafael--Oliveira"
    casa: str = "1A"  # Número da casa (pode ser alfanumérico)
    quantidade_p: int = 5  # Quantidade de pacotes
    pacote: str = "P"  # Tipo de pacote (ex: "P" para pacote pequeno)


class EncomendaBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. A busca será
        feita apenas com base no nome da encomenda.
    """
    nome: str = "Teste"


class ListagemEncomendasSchema(BaseModel):
    """ Define como uma listagem de encomendas será retornada. """
    encomendas: List[EncomendaSchema]


class EncomendaViewSchema(BaseModel):
    """ Define como uma encomenda será retornada: encomenda + detalhes. """
    id: int = 1
    nome: str = "Rafael-Oliveira"
    casa: str = "1A"
    quantidade_p: int = 5
    pacote: str = "P"  # Tipo de pacote (ex: "P" para pacote pequeno)


class EncomendaDelSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição
        de remoção.
    """
    mensagem: str
    nome: str


def apresenta_encomenda(encomenda: Encomenda):
    """ Retorna uma representação da encomenda seguindo o schema definido em
        EncomendaViewSchema.
    """
    return {
        "id": encomenda.id,
        "nome": encomenda.nome,
        "casa": encomenda.casa,
        "quantidade_p": encomenda.quantidade_p,
        "pacote": encomenda.pacote,
    }


def apresenta_encomendas(encomendas: List[Encomenda]):
    """ Retorna uma representação das encomendas cadastradas seguindo o schema definido em
        EncomendaViewSchema.
    """
    result = []
    for encomenda in encomendas:
        result.append({
            "nome": encomenda.nome,
            "casa": encomenda.casa,
            "quantidade_p": encomenda.quantidade_p,
            "pacote": encomenda.pacote,
        })

    return {"encomendas": result}
