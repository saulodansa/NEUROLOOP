from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Ativacao
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

router = APIRouter(prefix="/ativacoes", tags=["ativacoes"])

class AtivacaoCreate(BaseModel):
    nome: str
    tipo: Optional[str] = None
    descricao: Optional[str] = None
    valor_referencia: Optional[float] = None
    tempo_montagem_horas: Optional[int] = None
    equipamentos: Optional[str] = None

class AtivacaoOut(BaseModel):
    id: int
    nome: str
    tipo: Optional[str]
    descricao: Optional[str]
    valor_referencia: Optional[float]
    tempo_montagem_horas: Optional[int]
    equipamentos: Optional[str]
    criado_em: datetime

    class Config:
        from_attributes = True

@router.get("/", response_model=list[AtivacaoOut])
def listar(db: Session = Depends(get_db)):
    return db.query(Ativacao).all()

@router.post("/", response_model=AtivacaoOut)
def criar(ativacao: AtivacaoCreate, db: Session = Depends(get_db)):
    nova = Ativacao(**ativacao.model_dump())
    db.add(nova)
    db.commit()
    db.refresh(nova)
    return nova

@router.delete("/{id}")
def deletar(id: int, db: Session = Depends(get_db)):
    ativacao = db.query(Ativacao).filter(Ativacao.id == id).first()
    if not ativacao:
        raise HTTPException(status_code=404, detail="Não encontrado")
    db.delete(ativacao)
    db.commit()
    return {"ok": True}