from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import Proposta
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

router = APIRouter(prefix="/financeiro", tags=["financeiro"])

class LancamentoCreate(BaseModel):
    proposta_id: Optional[int] = None
    descricao: str
    tipo: str
    valor: float
    data: Optional[datetime] = None

class LancamentoOut(BaseModel):
    id: int
    proposta_id: Optional[int]
    descricao: str
    tipo: str
    valor: float
    data: Optional[datetime]
    criado_em: datetime

    class Config:
        from_attributes = True

from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from database import Base

class Lancamento(Base):
    __tablename__ = "lancamentos"
    id = Column(Integer, primary_key=True, index=True)
    proposta_id = Column(Integer, ForeignKey("propostas.id"), nullable=True)
    descricao = Column(String, nullable=False)
    tipo = Column(String, nullable=False)
    valor = Column(Float, nullable=False)
    data = Column(DateTime, nullable=True)
    criado_em = Column(DateTime, default=datetime.utcnow)

@router.get("/", response_model=list[LancamentoOut])
def listar(db: Session = Depends(get_db)):
    from sqlalchemy import text
    db.execute(text("SELECT 1"))
    lancamentos = db.query(Lancamento).order_by(Lancamento.data.desc()).all()
    return lancamentos

@router.post("/", response_model=LancamentoOut)
def criar(lancamento: LancamentoCreate, db: Session = Depends(get_db)):
    novo = Lancamento(**lancamento.model_dump())
    db.add(novo)
    db.commit()
    db.refresh(novo)
    return novo

@router.delete("/{id}")
def deletar(id: int, db: Session = Depends(get_db)):
    from fastapi import HTTPException
    l = db.query(Lancamento).filter(Lancamento.id == id).first()
    if not l:
        raise HTTPException(status_code=404, detail="Não encontrado")
    db.delete(l)
    db.commit()
    return {"ok": True}

@router.get("/resumo")
def resumo(db: Session = Depends(get_db)):
    lancamentos = db.query(Lancamento).all()
    receita = sum(l.valor for l in lancamentos if l.tipo == "receita")
    custo = sum(l.valor for l in lancamentos if l.tipo == "custo")
    return {
        "receita": receita,
        "custo": custo,
        "saldo": receita - custo
    }