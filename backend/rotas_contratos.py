from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text
from database import get_db, Base
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Contrato(Base):
    __tablename__ = "contratos"
    id = Column(Integer, primary_key=True, index=True)
    proposta_id = Column(Integer, ForeignKey("propostas.id"), nullable=True)
    cliente_nome = Column(String)
    descricao = Column(Text)
    valor = Column(Float)
    data_inicio = Column(DateTime)
    data_fim = Column(DateTime)
    condicoes_pagamento = Column(Text)
    status = Column(String, default="ativo")
    criado_em = Column(DateTime, default=datetime.utcnow)

router = APIRouter(prefix="/contratos", tags=["contratos"])

class ContratoCreate(BaseModel):
    proposta_id: Optional[int] = None
    cliente_nome: Optional[str] = None
    descricao: Optional[str] = None
    valor: Optional[float] = None
    data_inicio: Optional[datetime] = None
    data_fim: Optional[datetime] = None
    condicoes_pagamento: Optional[str] = None
    status: Optional[str] = "ativo"

class ContratoOut(BaseModel):
    id: int
    proposta_id: Optional[int]
    cliente_nome: Optional[str]
    descricao: Optional[str]
    valor: Optional[float]
    data_inicio: Optional[datetime]
    data_fim: Optional[datetime]
    condicoes_pagamento: Optional[str]
    status: Optional[str]
    criado_em: datetime

    class Config:
        from_attributes = True

@router.get("/", response_model=list[ContratoOut])
def listar(db: Session = Depends(get_db)):
    return db.query(Contrato).order_by(Contrato.criado_em.desc()).all()

@router.post("/", response_model=ContratoOut)
def criar(contrato: ContratoCreate, db: Session = Depends(get_db)):
    novo = Contrato(**contrato.model_dump())
    db.add(novo)
    db.commit()
    db.refresh(novo)
    return novo

@router.put("/{id}/status")
def atualizar_status(id: int, status: str, db: Session = Depends(get_db)):
    contrato = db.query(Contrato).filter(Contrato.id == id).first()
    if not contrato:
        raise HTTPException(status_code=404, detail="Não encontrado")
    contrato.status = status
    db.commit()
    return {"ok": True}

@router.delete("/{id}")
def deletar(id: int, db: Session = Depends(get_db)):
    contrato = db.query(Contrato).filter(Contrato.id == id).first()
    if not contrato:
        raise HTTPException(status_code=404, detail="Não encontrado")
    db.delete(contrato)
    db.commit()
    return {"ok": True}