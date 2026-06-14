<script setup>
import { ref, onMounted } from 'vue'

const contratos = ref([])
const clientes = ref([])
const mostrarForm = ref(false)
const form = ref({
  cliente_nome: '', descricao: '', valor: null,
  data_inicio: '', data_fim: '', condicoes_pagamento: '', status: 'ativo'
})

const statusColors = {
  ativo: { bg: '#EAF3DE', color: '#3B6D11' },
  encerrado: { bg: '#F1EFE8', color: '#5F5E5A' },
  cancelado: { bg: '#FCEBEB', color: '#A32D2D' }
}

const statusLabels = {
  ativo: 'ATIVO',
  encerrado: 'ENCERRADO',
  cancelado: 'CANCELADO'
}

async function carregar() {
  const [rc, rcl] = await Promise.all([
    fetch('http://127.0.0.1:8000/contratos/'),
    fetch('http://127.0.0.1:8000/clientes/')
  ])
  contratos.value = await rc.json()
  clientes.value = await rcl.json()
}

async function salvar() {
  const payload = {
    cliente_nome: form.value.cliente_nome,
    descricao: form.value.descricao,
    valor: form.value.valor,
    condicoes_pagamento: form.value.condicoes_pagamento,
    status: form.value.status,
    data_inicio: form.value.data_inicio ? new Date(form.value.data_inicio).toISOString() : null,
    data_fim: form.value.data_fim ? new Date(form.value.data_fim).toISOString() : null,
  }
  await fetch('http://127.0.0.1:8000/contratos/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload)
  })
  form.value = { cliente_nome: '', descricao: '', valor: null, data_inicio: '', data_fim: '', condicoes_pagamento: '', status: 'ativo' }
  mostrarForm.value = false
  carregar()
}

async function atualizarStatus(id, status) {
  await fetch(`http://127.0.0.1:8000/contratos/${id}/status?status=${status}`, { method: 'PUT' })
  carregar()
}

async function deletar(id) {
  await fetch(`http://127.0.0.1:8000/contratos/${id}`, { method: 'DELETE' })
  carregar()
}

onMounted(carregar)
</script>

<template>
  <div class="nl-page">
    <div class="nl-page-header">
      <div>
        <div class="nl-cota">// OPERAÇÃO</div>
        <div class="nl-page-title">Contratos</div>
      </div>
      <button class="nl-btn" @click="mostrarForm = !mostrarForm">+ NOVO CONTRATO</button>
    </div>

    <div v-if="mostrarForm" class="nl-form">
      <div class="nl-cota" style="margin-bottom:16px">// NOVO CONTRATO</div>
      <div class="nl-form-grid">
        <div class="nl-field" style="grid-column: span 2">
          <label>CLIENTE *</label>
          <select v-model="form.cliente_nome">
            <option value="">Selecione</option>
            <option v-for="c in clientes" :key="c.id" :value="c.nome">{{ c.nome }}</option>
          </select>
        </div>
        <div class="nl-field">
          <label>VALOR (R$)</label>
          <input v-model="form.valor" type="number" placeholder="0" />
        </div>
        <div class="nl-field">
          <label>DATA INÍCIO</label>
          <input v-model="form.data_inicio" type="date" />
        </div>
        <div class="nl-field">
          <label>DATA FIM</label>
          <input v-model="form.data_fim" type="date" />
        </div>
        <div class="nl-field">
          <label>STATUS</label>
          <select v-model="form.status">
            <option value="ativo">Ativo</option>
            <option value="encerrado">Encerrado</option>
            <option value="cancelado">Cancelado</option>
          </select>
        </div>
        <div class="nl-field" style="grid-column: span 2">
          <label>DESCRIÇÃO</label>
          <input v-model="form.descricao" placeholder="Objeto do contrato" />
        </div>
        <div class="nl-field" style="grid-column: span 3">
          <label>CONDIÇÕES DE PAGAMENTO</label>
          <input v-model="form.condicoes_pagamento" placeholder="Ex: 50% na assinatura, 50% na entrega" />
        </div>
      </div>
      <button class="nl-btn" @click="salvar">SALVAR</button>
    </div>

    <div class="nl-table-wrap">
      <table class="nl-table">
        <thead>
          <tr>
            <th>CLIENTE</th>
            <th>DESCRIÇÃO</th>
            <th>VALOR</th>
            <th>INÍCIO</th>
            <th>FIM</th>
            <th>STATUS</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          <tr v-if="contratos.length === 0">
            <td colspan="7" style="text-align:center; color:#aaa; padding:40px;">Nenhum contrato cadastrado</td>
          </tr>
          <tr v-for="c in contratos" :key="c.id">
            <td style="font-weight:500">{{ c.cliente_nome || '—' }}</td>
            <td style="color:#666">{{ c.descricao || '—' }}</td>
            <td style="font-family:'DM Mono',monospace">{{ c.valor ? 'R$ ' + c.valor.toLocaleString('pt-BR') : '—' }}</td>
            <td style="font-size:12px; color:#aaa">{{ c.data_inicio ? new Date(c.data_inicio).toLocaleDateString('pt-BR') : '—' }}</td>
            <td style="font-size:12px; color:#aaa">{{ c.data_fim ? new Date(c.data_fim).toLocaleDateString('pt-BR') : '—' }}</td>
            <td>
              <select
                :value="c.status"
                @change="atualizarStatus(c.id, $event.target.value)"
                :style="{ background: statusColors[c.status]?.bg, color: statusColors[c.status]?.color, border: 'none', fontFamily: 'DM Mono, monospace', fontSize: '9px', letterSpacing: '1px', padding: '3px 8px', cursor: 'pointer' }"
              >
                <option v-for="(label, key) in statusLabels" :key="key" :value="key">{{ label }}</option>
              </select>
            </td>
            <td><span class="nl-del" @click="deletar(c.id)">✕</span></td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=DM+Sans:wght@300;400;500&family=DM+Mono:wght@400&display=swap');
.nl-page { padding: 0; }
.nl-page-header { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 24px; }
.nl-cota { font-family: 'DM Mono', monospace; font-size: 8px; color: #BA7517; letter-spacing: 2px; margin-bottom: 4px; }
.nl-page-title { font-family: 'Syne', sans-serif; font-size: 22px; font-weight: 800; color: #111; }
.nl-btn { background: #000; border: none; color: #f59e0b; font-family: 'DM Mono', monospace; font-size: 9px; letter-spacing: 2px; padding: 10px 20px; cursor: pointer; }
.nl-btn:hover { background: #1a1a1a; }
.nl-form { background: #fff; border: 1px solid #E8E6E1; padding: 24px; margin-bottom: 24px; }
.nl-form-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; margin-bottom: 20px; }
.nl-field label { display: block; font-family: 'DM Mono', monospace; font-size: 8px; color: #BA7517; letter-spacing: 2px; margin-bottom: 6px; }
.nl-field input, .nl-field select { width: 100%; background: #F6F5F3; border: 1px solid #E8E6E1; color: #111; padding: 8px 12px; font-family: 'DM Sans', sans-serif; font-size: 13px; outline: none; }
.nl-field input:focus, .nl-field select:focus { border-color: #BA7517; }
.nl-table-wrap { background: #fff; border: 1px solid #E8E6E1; }
.nl-table { width: 100%; border-collapse: collapse; font-size: 13px; }
.nl-table th { font-family: 'DM Mono', monospace; font-size: 8px; letter-spacing: 2px; color: #BA7517; padding: 12px 16px; text-align: left; border-bottom: 1px solid #E8E6E1; background: #F6F5F3; }
.nl-table td { padding: 13px 16px; border-bottom: 1px solid #F0EEE9; color: #222; }
.nl-table tr:last-child td { border-bottom: none; }
.nl-table tr:hover td { background: #F9F8F6; }
.nl-del { color: #ccc; cursor: pointer; font-size: 11px; }
.nl-del:hover { color: #111; }
</style>