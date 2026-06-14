<script setup>
import { ref, onMounted } from 'vue'

const clientes = ref([])
const mostrarForm = ref(false)
const editandoId = ref(null)
const formEdicao = ref({})
const form = ref({
  nome: '', cnpj: '', contato: '', email: '', telefone: '', segmento: '', origem: ''
})

async function carregarClientes() {
  const res = await fetch('https://neuroloop-production-841a.up.railway.app/clientes/')
  clientes.value = await res.json()
}

async function salvarCliente() {
  await fetch('https://neuroloop-production-841a.up.railway.app/clientes/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(form.value)
  })
  form.value = { nome: '', cnpj: '', contato: '', email: '', telefone: '', segmento: '', origem: '' }
  mostrarForm.value = false
  carregarClientes()
}

async function deletarCliente(id) {
  await fetch(`https://neuroloop-production-841a.up.railway.app/clientes/${id}`, { method: 'DELETE' })
  carregarClientes()
}

function iniciarEdicao(cliente) {
  editandoId.value = cliente.id
  formEdicao.value = { ...cliente }
}

function cancelarEdicao() {
  editandoId.value = null
  formEdicao.value = {}
}

async function salvarEdicao(id) {
  await fetch(`https://neuroloop-production-841a.up.railway.app/clientes/${id}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(formEdicao.value)
  })
  editandoId.value = null
  carregarClientes()
}

onMounted(carregarClientes)
</script>

<template>
  <div class="nl-page">
    <div class="nl-page-header">
      <div>
        <div class="nl-cota">// CLIENTES</div>
        <div class="nl-page-title">Base de Clientes</div>
      </div>
      <button class="nl-btn" @click="mostrarForm = !mostrarForm">+ NOVO CLIENTE</button>
    </div>

    <div v-if="mostrarForm" class="nl-form">
      <div class="nl-cota" style="margin-bottom:16px">// NOVO CADASTRO</div>
      <div class="nl-form-grid">
        <div class="nl-field">
          <label>NOME *</label>
          <input v-model="form.nome" placeholder="Razão social" />
        </div>
        <div class="nl-field">
          <label>CNPJ</label>
          <input v-model="form.cnpj" placeholder="00.000.000/0000-00" />
        </div>
        <div class="nl-field">
          <label>CONTATO</label>
          <input v-model="form.contato" placeholder="Nome do responsável" />
        </div>
        <div class="nl-field">
          <label>EMAIL</label>
          <input v-model="form.email" placeholder="email@empresa.com" />
        </div>
        <div class="nl-field">
          <label>TELEFONE</label>
          <input v-model="form.telefone" placeholder="(21) 99999-9999" />
        </div>
        <div class="nl-field">
          <label>SEGMENTO</label>
          <input v-model="form.segmento" placeholder="Ex: Energia, Saúde, Tech" />
        </div>
        <div class="nl-field">
          <label>ORIGEM</label>
          <input v-model="form.origem" placeholder="Ex: Jasmin, Indicação" />
        </div>
      </div>
      <button class="nl-btn" @click="salvarCliente">SALVAR</button>
    </div>

    <div class="nl-table-wrap">
      <table class="nl-table">
        <thead>
          <tr>
            <th>NOME</th>
            <th>CONTATO</th>
            <th>SEGMENTO</th>
            <th>ORIGEM</th>
            <th>EMAIL</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          <tr v-if="clientes.length === 0">
            <td colspan="6" style="text-align:center; color:#aaa; padding:40px;">
              Nenhum cliente cadastrado
            </td>
          </tr>
          <template v-for="c in clientes" :key="c.id">
            <tr v-if="editandoId !== c.id" @dblclick="iniciarEdicao(c)">
              <td>{{ c.nome }}</td>
              <td>{{ c.contato }}</td>
              <td>{{ c.segmento }}</td>
              <td>{{ c.origem }}</td>
              <td>{{ c.email }}</td>
              <td><span class="nl-del" @click="deletarCliente(c.id)">✕</span></td>
            </tr>
            <tr v-else class="nl-editando">
              <td><input v-model="formEdicao.nome" class="nl-input-inline" /></td>
              <td><input v-model="formEdicao.contato" class="nl-input-inline" /></td>
              <td><input v-model="formEdicao.segmento" class="nl-input-inline" /></td>
              <td><input v-model="formEdicao.origem" class="nl-input-inline" /></td>
              <td><input v-model="formEdicao.email" class="nl-input-inline" /></td>
              <td style="display:flex; gap:8px; align-items:center;">
                <span class="nl-save" @click="salvarEdicao(c.id)">✓</span>
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
.nl-btn { background: #000; border: none; color: #f59e0b; font-family: 'DM Mono', monospace; font-size: 9px; letter-spacing: 2px; padding: 10px 20px; cursor: pointer; transition: all 0.2s; }
.nl-btn:hover { background: #1a1a1a; }
.nl-form { background: #fff; border: 1px solid #E8E6E1; padding: 24px; margin-bottom: 24px; }
.nl-form-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; margin-bottom: 20px; }
.nl-field label { display: block; font-family: 'DM Mono', monospace; font-size: 8px; color: #BA7517; letter-spacing: 2px; margin-bottom: 6px; }
.nl-field input { width: 100%; background: #F6F5F3; border: 1px solid #E8E6E1; color: #111; padding: 8px 12px; font-family: 'DM Sans', sans-serif; font-size: 13px; outline: none; }
.nl-field input:focus { border-color: #BA7517; }
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
