from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import Column, Integer, String, DateTime
from database import get_db, Base
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Ativo(Base):
    __tablename__ = "ativos"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    categoria = Column(String)
    status = Column(String, default="disponivel")
    numero_serie = Column(String)
    observacoes = Column(String)
    criado_em = Column(DateTime, default=datetime.utcnow)

router = APIRouter(prefix="/ativos", tags=["ativos"])

class AtivoCreate(BaseModel):
    nome: str
    categoria: Optional[str] = None
    status: Optional[str] = "disponivel"
    numero_serie: Optional[str] = None
    observacoes: Optional[str] = None

class AtivoOut(BaseModel):
    id: int
    nome: str
    categoria: Optional[str]
    status: Optional[str]
    numero_serie: Optional[str]
    observacoes: Optional[str]
    criado_em: datetime

    class Config:
        from_attributes = True

@router.get("/", response_model=list[AtivoOut])
def listar(db: Session = Depends(get_db)):
    return db.query(Ativo).all()

@router.post("/", response_model=AtivoOut)
def criar(ativo: AtivoCreate, db: Session = Depends(get_db)):
    novo = Ativo(**ativo.model_dump())
    db.add(novo)
    db.commit()
    db.refresh(novo)
    return novo

@router.put("/{id}/status")
def atualizar_status(id: int, status: str, db: Session = Depends(get_db)):
    ativo = db.query(Ativo).filter(Ativo.id == id).first()
    if not ativo:
        raise HTTPException(status_code=404, detail="Não encontrado")
    ativo.status = status
    db.commit()
    return {"ok": True}

@router.delete("/{id}")
def deletar(id: int, db: Session = Depends(get_db)):
    ativo = db.query(Ativo).filter(Ativo.id == id).first()
    if not ativo:
        raise HTTPException(status_code=404, detail="Não encontrado")
    db.delete(ativo)
    db.commit()
    return {"ok": True}
