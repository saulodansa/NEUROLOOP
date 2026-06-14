from sqlalchemy import Column, Integer, String, Float, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class Cliente(Base):
    __tablename__ = "clientes"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    cnpj = Column(String)
    contato = Column(String)
    email = Column(String)
    telefone = Column(String)
    segmento = Column(String)
    origem = Column(String)
    criado_em = Column(DateTime, default=datetime.utcnow)
    propostas = relationship("Proposta", back_populates="cliente")

class Ativacao(Base):
    __tablename__ = "ativacoes"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    tipo = Column(String)
    descricao = Column(Text)
    valor_referencia = Column(Float)
    tempo_montagem_horas = Column(Integer)
    equipamentos = Column(Text)
    criado_em = Column(DateTime, default=datetime.utcnow)

class Evento(Base):
    __tablename__ = "eventos"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    data = Column(DateTime)
    local = Column(String)
    cliente_id = Column(Integer, ForeignKey("clientes.id"))
    criado_em = Column(DateTime, default=datetime.utcnow)

class Proposta(Base):
    __tablename__ = "propostas"
    id = Column(Integer, primary_key=True, index=True)
    cliente_id = Column(Integer, ForeignKey("clientes.id"))
    evento_id = Column(Integer, ForeignKey("eventos.id"))
    valor_total = Column(Float)
    status = Column(String, default="enviada")
    descricao = Column(Text)
    cliente_final = Column(String)
    criado_em = Column(DateTime, default=datetime.utcnow)
    cliente = relationship("Cliente", back_populates="propostas")

