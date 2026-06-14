<script setup>
import { ref, onMounted } from 'vue'

const eventos = ref([])
const clientes = ref([])
const mostrarForm = ref(false)
const editandoId = ref(null)
const formEdicao = ref({})
const form = ref({
  nome: '', data: '', local: '', cliente_id: ''
})

async function carregar() {
  const [re, rc] = await Promise.all([
    fetch('http://127.0.0.1:8000/eventos/'),
    fetch('http://127.0.0.1:8000/clientes/')
  ])
  eventos.value = await re.json()
  clientes.value = await rc.json()
}

async function salvar() {
  const payload = {
    nome: form.value.nome,
    local: form.value.local,
    cliente_id: form.value.cliente_id || null,
    data: form.value.data ? new Date(form.value.data).toISOString() : null
  }
  await fetch('http://127.0.0.1:8000/eventos/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload)
  })
  form.value = { nome: '', data: '', local: '', cliente_id: '' }
  mostrarForm.value = false
  carregar()
}

async function deletar(id) {
  await fetch(`http://127.0.0.1:8000/eventos/${id}`, { method: 'DELETE' })
  carregar()
}

function iniciarEdicao(e) {
  editandoId.value = e.id
  formEdicao.value = { ...e }
}

function cancelarEdicao() {
  editandoId.value = null
  formEdicao.value = {}
}

async function salvarEdicao(id) {
  const payload = {
    nome: formEdicao.value.nome,
    local: formEdicao.value.local,
    cliente_id: formEdicao.value.cliente_id || null,
    data: formEdicao.value.data ? new Date(formEdicao.value.data).toISOString() : null
  }
  await fetch(`http://127.0.0.1:8000/eventos/${id}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload)
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
        <div class="nl-cota">// AGENDA</div>
        <div class="nl-page-title">Eventos</div>
      </div>
      <button class="nl-btn" @click="mostrarForm = !mostrarForm">+ NOVO EVENTO</button>
    </div>

    <div v-if="mostrarForm" class="nl-form">
      <div class="nl-cota" style="margin-bottom:16px">// NOVO EVENTO</div>
      <div class="nl-form-grid">
        <div class="nl-field">
          <label>NOME DO EVENTO *</label>
          <input v-model="form.nome" placeholder="Ex: Expo Rio 2026" />
        </div>
        <div class="nl-field">
          <label>DATA</label>
          <input v-model="form.data" type="datetime-local" />
        </div>
        <div class="nl-field">
          <label>LOCAL</label>
          <input v-model="form.local" placeholder="Ex: Riocentro, Pavilhão 3" />
        </div>
        <div class="nl-field">
          <label>CLIENTE</label>
          <select v-model="form.cliente_id">
            <option value="">Selecione</option>
            <option v-for="c in clientes" :key="c.id" :value="c.id">{{ c.nome }}</option>
          </select>
        </div>
      </div>
      <button class="nl-btn" @click="salvar">SALVAR</button>
    </div>

    <div class="nl-table-wrap">
      <table class="nl-table">
        <thead>
          <tr>
            <th>EVENTO</th>
            <th>CLIENTE</th>
            <th>DATA</th>
            <th>LOCAL</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          <tr v-if="eventos.length === 0">
            <td colspan="5" style="text-align:center; color:#aaa; padding:40px;">Nenhum evento cadastrado</td>
          </tr>
          <template v-for="e in eventos" :key="e.id">
            <tr v-if="editandoId !== e.id" @dblclick="iniciarEdicao(e)">
              <td style="font-weight:500">{{ e.nome }}</td>
              <td>{{ e.cliente_nome || '—' }}</td>
              <td style="font-family:'DM Mono',monospace; font-size:12px">{{ e.data ? new Date(e.data).toLocaleDateString('pt-BR') : '—' }}</td>
              <td style="color:#666">{{ e.local || '—' }}</td>
              <td><span class="nl-del" @click="deletar(e.id)">✕</span></td>
            </tr>
            <tr v-else class="nl-editando">
              <td><input v-model="formEdicao.nome" class="nl-input-inline" /></td>
              <td>{{ e.cliente_nome || '—' }}</td>
              <td><input v-model="formEdicao.data" type="date" class="nl-input-inline" /></td>
              <td><input v-model="formEdicao.local" class="nl-input-inline" /></td>
              <td style="display:flex; gap:8px; align-items:center;">
                <span class="nl-save" @click="salvarEdicao(e.id)">✓</span>
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