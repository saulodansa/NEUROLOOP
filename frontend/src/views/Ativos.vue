<script setup>
import { ref, onMounted } from 'vue'

const ativos = ref([])
const mostrarForm = ref(false)
const form = ref({
  nome: '', categoria: '', status: 'disponivel', numero_serie: '', observacoes: ''
})

const statusColors = {
  disponivel: { bg: '#EAF3DE', color: '#3B6D11' },
  em_uso: { bg: '#FAEEDA', color: '#854F0B' },
  manutencao: { bg: '#FCEBEB', color: '#A32D2D' }
}

const statusLabels = {
  disponivel: 'DISPONÍVEL',
  em_uso: 'EM USO',
  manutencao: 'MANUTENÇÃO'
}

async function carregar() {
  const res = await fetch('http://127.0.0.1:8000/ativos/')
  ativos.value = await res.json()
}

async function salvar() {
  await fetch('http://127.0.0.1:8000/ativos/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(form.value)
  })
  form.value = { nome: '', categoria: '', status: 'disponivel', numero_serie: '', observacoes: '' }
  mostrarForm.value = false
  carregar()
}

async function atualizarStatus(id, status) {
  await fetch(`http://127.0.0.1:8000/ativos/${id}/status?status=${status}`, { method: 'PUT' })
  carregar()
}

async function deletar(id) {
  await fetch(`http://127.0.0.1:8000/ativos/${id}`, { method: 'DELETE' })
  carregar()
}

onMounted(carregar)
</script>

<template>
  <div class="nl-page">
    <div class="nl-page-header">
      <div>
        <div class="nl-cota">// OPERAÇÃO</div>
        <div class="nl-page-title">Ativos</div>
      </div>
      <button class="nl-btn" @click="mostrarForm = !mostrarForm">+ NOVO ATIVO</button>
    </div>

    <div v-if="mostrarForm" class="nl-form">
      <div class="nl-cota" style="margin-bottom:16px">// NOVO ATIVO</div>
      <div class="nl-form-grid">
        <div class="nl-field" style="grid-column: span 2">
          <label>NOME *</label>
          <input v-model="form.nome" placeholder="Ex: Robô Humanoide v1" />
        </div>
        <div class="nl-field">
          <label>CATEGORIA</label>
          <input v-model="form.categoria" placeholder="Ex: Robótica, Display, Cabo" />
        </div>
        <div class="nl-field">
          <label>STATUS</label>
          <select v-model="form.status">
            <option value="disponivel">Disponível</option>
            <option value="em_uso">Em uso</option>
            <option value="manutencao">Manutenção</option>
          </select>
        </div>
        <div class="nl-field">
          <label>NÚMERO DE SÉRIE</label>
          <input v-model="form.numero_serie" placeholder="Ex: SN-2026-001" />
        </div>
        <div class="nl-field" style="grid-column: span 3">
          <label>OBSERVAÇÕES</label>
          <input v-model="form.observacoes" placeholder="Ex: Necessita calibração antes de uso" />
        </div>
      </div>
      <button class="nl-btn" @click="salvar">SALVAR</button>
    </div>

    <div class="nl-table-wrap">
      <table class="nl-table">
        <thead>
          <tr>
            <th>NOME</th>
            <th>CATEGORIA</th>
            <th>Nº SÉRIE</th>
            <th>STATUS</th>
            <th>OBSERVAÇÕES</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          <tr v-if="ativos.length === 0">
            <td colspan="6" style="text-align:center; color:#aaa; padding:40px;">Nenhum ativo cadastrado</td>
          </tr>
          <tr v-for="a in ativos" :key="a.id">
            <td style="font-weight:500">{{ a.nome }}</td>
            <td style="color:#666">{{ a.categoria || '—' }}</td>
            <td style="font-family:'DM Mono',monospace; font-size:11px; color:#aaa">{{ a.numero_serie || '—' }}</td>
            <td>
              <select
                :value="a.status"
                @change="atualizarStatus(a.id, $event.target.value)"
                :style="{ background: statusColors[a.status]?.bg, color: statusColors[a.status]?.color, border: 'none', fontFamily: 'DM Mono, monospace', fontSize: '9px', letterSpacing: '1px', padding: '3px 8px', cursor: 'pointer' }"
              >
                <option v-for="(label, key) in statusLabels" :key="key" :value="key">{{ label }}</option>
              </select>
            </td>
            <td style="color:#888; font-size:12px">{{ a.observacoes || '—' }}</td>
            <td><span class="nl-del" @click="deletar(a.id)">✕</span></td>
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