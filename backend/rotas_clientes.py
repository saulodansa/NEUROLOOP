from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Cliente
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

router = APIRouter(prefix="/clientes", tags=["clientes"])

class ClienteCreate(BaseModel):
    nome: str
    cnpj: Optional[str] = None
    contato: Optional[str] = None
    email: Optional[str] = None
    telefone: Optional[str] = None
    segmento: Optional[str] = None
    origem: Optional[str] = None

class ClienteOut(BaseModel):
    id: int
    nome: str
    cnpj: Optional[str]
    contato: Optional[str]
    email: Optional[str]
    telefone: Optional[str]
    segmento: Optional[str]
    origem: Optional[str]
    criado_em: datetime

    class Config:
        from_attributes = True

@router.get("/", response_model=list[ClienteOut])
def listar_clientes(db: Session = Depends(get_db)):
    return db.query(Cliente).all()

@router.get("/{id}", response_model=ClienteOut)
def buscar_cliente(id: int, db: Session = Depends(get_db)):
    cliente = db.query(Cliente).filter(Cliente.id == id).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    return cliente

@router.post("/", response_model=ClienteOut)
def criar_cliente(cliente: ClienteCreate, db: Session = Depends(get_db)):
    novo = Cliente(**cliente.model_dump())
    db.add(novo)
    db.commit()
    db.refresh(novo)
    return novo

@router.put("/{id}", response_model=ClienteOut)
def atualizar_cliente(id: int, dados: ClienteCreate, db: Session = Depends(get_db)):
    cliente = db.query(Cliente).filter(Cliente.id == id).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    for key, value in dados.model_dump().items():
        setattr(cliente, key, value)
    db.commit()
    db.refresh(cliente)
    return cliente

@router.delete("/{id}")
def deletar_cliente(id: int, db: Session = Depends(get_db)):
    cliente = db.query(Cliente).filter(Cliente.id == id).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    db.delete(cliente)
    db.commit()
    return {"ok": True}