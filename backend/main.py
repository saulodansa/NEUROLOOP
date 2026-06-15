from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine
from database import Base
import models
from rotas_clientes import router as clientes_router
from rotas_ativacoes import router as ativacoes_router
from rotas_propostas import router as propostas_router
from rotas_eventos import router as eventos_router
from rotas_financeiro import router as financeiro_router, Lancamento
from rotas_ativos import router as ativos_router, Ativo
from rotas_contratos import router as contratos_router, Contrato

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Neuroloop OS", version="0.1")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "https://rare-communication-production.up.railway.app", "https://neuroloop.up.railway.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(clientes_router)
app.include_router(ativacoes_router)
app.include_router(propostas_router)
app.include_router(eventos_router)
app.include_router(financeiro_router)
app.include_router(ativos_router)
app.include_router(contratos_router)

@app.get("/")
def root():
    return {"status": "online", "sistema": "Neuroloop OS"}