<script setup>
import { ref, onMounted } from 'vue'

const propostas = ref([])
const clientes = ref([])
const mostrarForm = ref(false)
const editandoId = ref(null)
const formEdicao = ref({})
const form = ref({
  cliente_id: '', valor_total: null, status: 'enviada', descricao: '', cliente_final: ''
})

const statusLabels = {
  enviada: 'ENVIADA',
  negociando: 'NEGOCIANDO',
  aprovada: 'APROVADA',
  perdida: 'PERDIDA'
}

const statusColors = {
  enviada: { bg: '#F1EFE8', color: '#5F5E5A' },
  negociando: { bg: '#FAEEDA', color: '#854F0B' },
  aprovada: { bg: '#EAF3DE', color: '#3B6D11' },
  perdida: { bg: '#FCEBEB', color: '#A32D2D' }
}

async function carregar() {
  const [rp, rc] = await Promise.all([
    fetch('http://127.0.0.1:8000/propostas/'),
    fetch('http://127.0.0.1:8000/clientes/')
  ])
  propostas.value = await rp.json()
  clientes.value = await rc.json()
}

async function salvar() {
  await fetch('http://127.0.0.1:8000/propostas/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(form.value)
  })
  form.value = { cliente_id: '', valor_total: null, status: 'enviada', descricao: '', cliente_final: '' }
  mostrarForm.value = false
  carregar()
}

async function atualizarStatus(id, status) {
  await fetch(`http://127.0.0.1:8000/propostas/${id}/status?status=${status}`, { method: 'PUT' })
  carregar()
}

async function deletar(id) {
  await fetch(`http://127.0.0.1:8000/propostas/${id}`, { method: 'DELETE' })
  carregar()
}

function iniciarEdicao(p) {
  editandoId.value = p.id
  formEdicao.value = { ...p }
}

function cancelarEdicao() {
  editandoId.value = null
  formEdicao.value = {}
}

async function salvarEdicao(id) {
  await fetch(`http://127.0.0.1:8000/propostas/${id}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      cliente_id: formEdicao.value.cliente_id,
      valor_total: formEdicao.value.valor_total,
      status: formEdicao.value.status,
      descricao: formEdicao.value.descricao,
      cliente_final: formEdicao.value.cliente_final
    })
  })
  editandoId.value = null
  carregar()
}

onMounted(carregar)
</script>

<template>
  <div class="nl-page">
    <div class="nl-page-header">
      <div>
        <div class="nl-cota">// COMERCIAL</div>
        <div class="nl-page-title">Propostas</div>
      </div>
      <button class="nl-btn" @click="mostrarForm = !mostrarForm">+ NOVA PROPOSTA</button>
    </div>

    <div v-if="mostrarForm" class="nl-form">
      <div class="nl-cota" style="margin-bottom:16px">// NOVA PROPOSTA</div>
      <div class="nl-form-grid">
        <div class="nl-field">
          <label>CLIENTE *</label>
          <select v-model="form.cliente_id">
            <option value="">Selecione</option>
            <option v-for="c in clientes" :key="c.id" :value="c.id">{{ c.nome }}</option>
          </select>
        </div>
        <div class="nl-field">
          <label>VALOR TOTAL (R$)</label>
          <input v-model="form.valor_total" type="number" placeholder="0" />
        </div>
        <div class="nl-field">
          <label>STATUS</label>
          <select v-model="form.status">
            <option value="enviada">Enviada</option>
            <option value="negociando">Negociando</option>
            <option value="aprovada">Aprovada</option>
            <option value="perdida">Perdida</option>
          </select>
        </div>
        <div class="nl-field" style="grid-column: span 3">
          <label>DESCRIÇÃO</label>
          <input v-model="form.descricao" placeholder="Descrição da proposta" />
        </div>
        <div class="nl-field" style="grid-column: span 3">
          <label>CLIENTE FINAL / MARCA DO STAND</label>
          <input v-model="form.cliente_final" placeholder="Ex: Firjan, Petrobras, etc" />
        </div>
      </div>
      <button class="nl-btn" @click="salvar">SALVAR</button>
    </div>

    <div class="nl-table-wrap">
      <table class="nl-table">
        <thead>
          <tr>
            <th>#</th>
            <th>CLIENTE</th>
            <th>DESCRIÇÃO</th>
            <th>MARCA/STAND</th>
            <th>VALOR</th>
            <th>STATUS</th>
            <th>DATA</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          <tr v-if="propostas.length === 0">
            <td colspan="8" style="text-align:center; color:#aaa; padding:40px;">Nenhuma proposta cadastrada</td>
          </tr>
          <template v-for="p in propostas" :key="p.id">
            <tr v-if="editandoId !== p.id" @dblclick="iniciarEdicao(p)">
              <td style="color:#aaa; font-family:'DM Mono',monospace; font-size:11px">#{{ p.id }}</td>
              <td style="font-weight:500">{{ p.cliente_nome }}</td>
              <td style="color:#666">{{ p.descricao }}</td>
              <td style="color:#666">{{ p.cliente_final || '—' }}</td>
              <td style="font-family:'DM Mono',monospace">{{ p.valor_total ? 'R$ ' + p.valor_total.toLocaleString('pt-BR') : '—' }}</td>
              <td>
                <select :value="p.status" @change="atualizarStatus(p.id, $event.target.value)"
                  :style="{ background: statusColors[p.status]?.bg, color: statusColors[p.status]?.color, border: 'none', fontFamily: 'DM Mono, monospace', fontSize: '9px', letterSpacing: '1px', padding: '3px 8px', cursor: 'pointer' }">
                  <option v-for="(label, key) in statusLabels" :key="key" :value="key">{{ label }}</option>
                </select>
              </td>
              <td style="color:#aaa; font-size:12px">{{ new Date(p.criado_em).toLocaleDateString('pt-BR') }}</td>
              <td><span class="nl-del" @click="deletar(p.id)">✕</span></td>
            </tr>
            <tr v-else class="nl-editando">
              <td style="color:#aaa">#{{ p.id }}</td>
              <td style="font-weight:500">{{ p.cliente_nome }}</td>
              <td><input v-model="formEdicao.descricao" class="nl-input-inline" /></td>
              <td><input v-model="formEdicao.cliente_final" class="nl-input-inline" /></td>
              <td><input v-model="formEdicao.valor_total" type="number" class="nl-input-inline" /></td>
              <td>
                <select v-model="formEdicao.status" class="nl-input-inline">
                  <option v-for="(label, key) in statusLabels" :key="key" :value="key">{{ label }}</option>
                </select>
              </td>
              <td></td>
              <td style="display:flex; gap:8px; align-items:center;">
                <span class="nl-save" @click="salvarEdicao(p.id)">✓</span>
                <span class="nl-del" @click="cancelarEdicao">✕</span>
              </td>
            </tr>
          </template>
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
.nl-editando td { background: #FAEEDA !important; padding: 6px 16px; }
.nl-input-inline { width: 100%; background: #fff; border: 1px solid #BA7517; color: #111; padding: 5px 8px; font-family: 'DM Sans', sans-serif; font-size: 13px; outline: none; }
.nl-del { color: #ccc; cursor: pointer; font-size: 11px; }
.nl-del:hover { color: #111; }
.nl-save { color: #3B6D11; cursor: pointer; font-size: 14px; font-weight: 500; }
.nl-save:hover { color: #27500A; }
</style>