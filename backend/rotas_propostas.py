from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Proposta, Cliente, Evento
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

router = APIRouter(prefix="/propostas", tags=["propostas"])

class PropostaCreate(BaseModel):
    cliente_id: int
    evento_id: Optional[int] = None
    valor_total: Optional[float] = None
    status: Optional[str] = "enviada"
    descricao: Optional[str] = None
    cliente_final: Optional[str] = None

class PropostaOut(BaseModel):
    id: int
    cliente_id: int
    evento_id: Optional[int]
    valor_total: Optional[float]
    status: Optional[str]
    descricao: Optional[str]
    cliente_final: Optional[str] = None
    criado_em: datetime
    cliente_nome: Optional[str] = None

    class Config:
        from_attributes = True

def montar_out(p, db):
    cliente = db.query(Cliente).filter(Cliente.id == p.cliente_id).first()
    return PropostaOut(
        id=p.id,
        cliente_id=p.cliente_id,
        evento_id=p.evento_id,
        valor_total=p.valor_total,
        status=p.status,
        descricao=p.descricao,
        cliente_final=p.cliente_final,
        criado_em=p.criado_em,
        cliente_nome=cliente.nome if cliente else None
    )

@router.get("/", response_model=list[PropostaOut])
def listar(db: Session = Depends(get_db)):
    return [montar_out(p, db) for p in db.query(Proposta).all()]

@router.post("/", response_model=PropostaOut)
def criar(proposta: PropostaCreate, db: Session = Depends(get_db)):
    nova = Proposta(**proposta.model_dump())
    db.add(nova)
    db.commit()
    db.refresh(nova)
    return montar_out(nova, db)

@router.put("/{id}", response_model=PropostaOut)
def atualizar(id: int, dados: PropostaCreate, db: Session = Depends(get_db)):
    p = db.query(Proposta).filter(Proposta.id == id).first()
    if not p:
        raise HTTPException(status_code=404, detail="Não encontrado")
    for key, value in dados.model_dump().items():
        setattr(p, key, value)
    db.commit()
    db.refresh(p)
    return montar_out(p, db)

@router.put("/{id}/status")
def atualizar_status(id: int, status: str, db: Session = Depends(get_db)):
    p = db.query(Proposta).filter(Proposta.id == id).first()
    if not p:
        raise HTTPException(status_code=404, detail="Não encontrado")
    p.status = status
    db.commit()
    return {"ok": True}

@router.delete("/{id}")
def deletar(id: int, db: Session = Depends(get_db)):
    p = db.query(Proposta).filter(Proposta.id == id).first()
    if not p:
        raise HTTPException(status_code=404, detail="Não encontrado")
    db.delete(p)
    db.commit()
    return {"ok": True}