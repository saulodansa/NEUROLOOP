from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Evento, Cliente
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

router = APIRouter(prefix="/eventos", tags=["eventos"])

class EventoCreate(BaseModel):
    nome: str
    data: Optional[datetime] = None
    local: Optional[str] = None
    cliente_id: Optional[int] = None

class EventoOut(BaseModel):
    id: int
    nome: str
    data: Optional[datetime]
    local: Optional[str]
    cliente_id: Optional[int]
    criado_em: datetime
    cliente_nome: Optional[str] = None

    class Config:
        from_attributes = True

@router.get("/", response_model=list[EventoOut])
def listar(db: Session = Depends(get_db)):
    eventos = db.query(Evento).all()
    result = []
    for e in eventos:
        cliente = db.query(Cliente).filter(Cliente.id == e.cliente_id).first()
        result.append(EventoOut(
            id=e.id,
            nome=e.nome,
            data=e.data,
            local=e.local,
            cliente_id=e.cliente_id,
            criado_em=e.criado_em,
            cliente_nome=cliente.nome if cliente else None
        ))
    return result

@router.post("/", response_model=EventoOut)
def criar(evento: EventoCreate, db: Session = Depends(get_db)):
    novo = Evento(**evento.model_dump())
    db.add(novo)
    db.commit()
    db.refresh(novo)
    cliente = db.query(Cliente).filter(Cliente.id == novo.cliente_id).first()
    return EventoOut(
        id=novo.id,
        nome=novo.nome,
        data=novo.data,
        local=novo.local,
        cliente_id=novo.cliente_id,
        criado_em=novo.criado_em,
        cliente_nome=cliente.nome if cliente else None
    )
@router.put("/{id}", response_model=EventoOut)
def atualizar(id: int, evento: EventoCreate, db: Session = Depends(get_db)):
    e = db.query(Evento).filter(Evento.id == id).first()
    if not e:
        raise HTTPException(status_code=404, detail="Não encontrado")
    for key, value in evento.model_dump().items():
        setattr(e, key, value)
    db.commit()
    db.refresh(e)
    cliente = db.query(Cliente).filter(Cliente.id == e.cliente_id).first()
    return EventoOut(
        id=e.id,
        nome=e.nome,
        data=e.data,
        local=e.local,
        cliente_id=e.cliente_id,
        criado_em=e.criado_em,
        cliente_nome=cliente.nome if cliente else None
    )
    
@router.delete("/{id}")
def deletar(id: int, db: Session = Depends(get_db)):
    evento = db.query(Evento).filter(Evento.id == id).first()
    if not evento:
        raise HTTPException(status_code=404, detail="Não encontrado")
    db.delete(evento)
    db.commit()
    return {"ok": True}