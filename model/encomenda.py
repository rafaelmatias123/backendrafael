from sqlalchemy import Column, String, Integer, DateTime
from datetime import datetime
from typing import Union

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from model import Base

class Encomenda(Base):
    __tablename__ = 'encomenda'

    id = Column("encomenda_id", Integer, primary_key=True)
    nome = Column(String(150), unique=False)
    casa = Column(String(100))  # Número da casa como inteiro
    quantidade_p = Column(Integer)  # Quantidade de pacotes como inteiro
    pacote = Column(String(10))  
    #Se o pacote for pequeno = P. Se for grande = G. Se for médio = M
    data_cadastro = Column(DateTime, default=datetime.now())

    def __init__(self, nome: str, casa: str, quantidade_p: int,
                 pacote: str, data_cadastro: Union[DateTime, None] = None):

        self.nome = nome
        self.casa = casa
        self.quantidade_p = quantidade_p
        self.pacote = pacote
        if data_cadastro:
            self.data_cadastro = data_cadastro

