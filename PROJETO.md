# NEUROLOOP OS — Documentação do Projeto

## Visão Geral
Sistema de gestão interno para a NEUROLOOP, empresa de ativações tecnológicas em eventos corporativos.
Desenvolvido por Saulo e Jasmin. Início: 14/06/2026 às 23h00.

## Sócios
- Saulo — técnico, criativo, desenvolvedor
- Jasmin — comercial, relacionamento, operações

## Stack
- Backend: Python 3.11 + FastAPI + SQLAlchemy
- Frontend: Vue.js 3 + Vue Router + Pinia
- Banco: PostgreSQL 17
- Deploy futuro: VPS (DigitalOcean)

## Estrutura de Pastas
D:\NEUROLOOP\
├── backend\
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── rotas_clientes.py
│   ├── rotas_ativacoes.py
│   ├── rotas_propostas.py
│   ├── rotas_eventos.py
│   ├── rotas_financeiro.py
│   ├── rotas_ativos.py
│   ├── rotas_contratos.py
│   ├── .env
│   └── venv\
└── frontend\
    └── src\
        ├── App.vue
        ├── router\index.js
        ├── components\
        │   └── Layout.vue
        └── views\
            ├── Dashboard.vue
            ├── Clientes.vue
            ├── Portfolio.vue
            ├── Propostas.vue
            ├── Eventos.vue
            ├── Financeiro.vue
            ├── Ativos.vue
            └── Contratos.vue

## Modelos do Banco

### Cliente
- id, nome, cnpj, contato, email, telefone, segmento, origem, criado_em

### Ativacao
- id, nome, tipo, descricao, valor_referencia, tempo_montagem_horas, equipamentos, criado_em

### Evento
- id, nome, data, local, cliente_id, criado_em

### Proposta
- id, cliente_id, evento_id, valor_total, status, descricao, cliente_final, criado_em
- status: enviada | negociando | aprovada | perdida

### Lancamento (financeiro)
- id, proposta_id, descricao, tipo, valor, data, criado_em
- tipo: receita | custo

### Ativo
- id, nome, categoria, status, numero_serie, observacoes, criado_em
- status: disponivel | em_uso | manutencao

### Contrato
- id, proposta_id, cliente_nome, descricao, valor, data_inicio, data_fim, condicoes_pagamento, status, criado_em
- status: ativo | encerrado | cancelado

## API — Endpoints Ativos
- GET/POST /clientes/
- GET/PUT/DELETE /clientes/{id}
- GET/POST /ativacoes/
- DELETE /ativacoes/{id}
- GET/POST /propostas/
- PUT /propostas/{id}/status
- DELETE /propostas/{id}
- GET/POST /eventos/
- DELETE /eventos/{id}
- GET/POST /financeiro/
- GET /financeiro/resumo
- DELETE /financeiro/{id}
- GET/POST /ativos/
- PUT /ativos/{id}/status
- DELETE /ativos/{id}
- GET/POST /contratos/
- PUT /contratos/{id}/status
- DELETE /contratos/{id}

## Módulos Concluídos
- [x] Painel executivo com dados reais
- [x] Clientes
- [x] Portfólio de ativações
- [x] Propostas com cliente pagador e marca/stand
- [x] Eventos
- [x] Financeiro (caixa)
- [x] Ativos físicos
- [x] Contratos

## Módulos Pendentes
- [ ] Contas a receber
- [ ] Edição de registros
- [ ] Deploy em VPS

## Decisões de Arquitetura
- Campo cliente_final na proposta para marca/stand diferente do cliente pagador
- Layout: menu/header pretos, área de trabalho em #F6F5F3
- Fonte display: Syne 800, corpo: DM Sans, técnico: DM Mono
- Acento âmbar: #f59e0b / #BA7517
- Modelos Lancamento, Ativo e Contrato definidos nos próprios arquivos de rotas
- ALTER TABLE manual necessário ao adicionar colunas em tabelas existentes

## Tempo de Desenvolvimento
- Início: 14/06/2026 às 23h00
- Em andamento