<script setup>
import { ref, onMounted } from 'vue'

const ativacoes = ref([])
const mostrarForm = ref(false)
const form = ref({
  nome: '', tipo: '', descricao: '', valor_referencia: null, tempo_montagem_horas: null, equipamentos: ''
})

async function carregar() {
  const res = await fetch('https://neuroloop-production-841a.up.railway.app/ativacoes/')
  ativacoes.value = await res.json()
}

async function salvar() {
  await fetch('https://neuroloop-production-841a.up.railway.app/ativacoes/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(form.value)
  })
  form.value = { nome: '', tipo: '', descricao: '', valor_referencia: null, tempo_montagem_horas: null, equipamentos: '' }
  mostrarForm.value = false
  carregar()
}

async function deletar(id) {
  await fetch(`https://neuroloop-production-841a.up.railway.app/ativacoes/${id}`, { method: 'DELETE' })
  carregar()
}

onMounted(carregar)
</script>

<template>
  <div class="nl-page">
    <div class="nl-page-header">
      <div>
        <div class="nl-cota">// OPERAÇÃO</div>
        <div class="nl-page-title">Portfólio de Ativações</div>
      </div>
      <button class="nl-btn" @click="mostrarForm = !mostrarForm">+ NOVA ATIVAÇÃO</button>
    </div>

    <div v-if="mostrarForm" class="nl-form">
      <div class="nl-cota" style="margin-bottom:16px">// NOVA ATIVAÇÃO</div>
      <div class="nl-form-grid">
        <div class="nl-field">
          <label>NOME *</label>
          <input v-model="form.nome" placeholder="Ex: Robô Humanoide Stand" />
        </div>
        <div class="nl-field">
          <label>TIPO</label>
          <input v-model="form.tipo" placeholder="Ex: Portfólio / Customizada" />
        </div>
        <div class="nl-field">
          <label>VALOR REFERÊNCIA (R$)</label>
          <input v-model="form.valor_referencia" type="number" placeholder="0" />
        </div>
        <div class="nl-field">
          <label>TEMPO MONTAGEM (horas)</label>
          <input v-model="form.tempo_montagem_horas" type="number" placeholder="0" />
        </div>
        <div class="nl-field" style="grid-column: span 2">
          <label>DESCRIÇÃO</label>
          <input v-model="form.descricao" placeholder="Descrição da ativação" />
        </div>
        <div class="nl-field" style="grid-column: span 3">
          <label>EQUIPAMENTOS</label>
          <input v-model="form.equipamentos" placeholder="Ex: Robô, notebook, câmera, cabo HDMI" />
        </div>
      </div>
      <button class="nl-btn" @click="salvar">SALVAR</button>
    </div>

    <div class="nl-cards">
      <div v-if="ativacoes.length === 0" style="color: rgba(255,255,255,0.2); font-family: 'DM Mono', monospace; font-size: 12px;">
        Nenhuma ativação cadastrada
      </div>
      <div v-for="a in ativacoes" :key="a.id" class="nl-card">
        <div class="nl-card-header">
          <div>
            <div class="nl-card-nome">{{ a.nome }}</div>
            <div class="nl-card-tipo">{{ a.tipo }}</div>
          </div>
          <span class="nl-del" @click="deletar(a.id)">✕</span>
        </div>
        <div class="nl-card-desc">{{ a.descricao }}</div>
        <div class="nl-card-footer">
          <div>
            <div class="nl-card-label">VALOR REF.</div>
            <div class="nl-card-val">R$ {{ a.valor_referencia?.toLocaleString('pt-BR') || '—' }}</div>
          </div>
          <div>
            <div class="nl-card-label">MONTAGEM</div>
            <div class="nl-card-val">{{ a.tempo_montagem_horas || '—' }}h</div>
          </div>
        </div>
        <div v-if="a.equipamentos" class="nl-card-equip">
          <span class="nl-card-label">EQUIPAMENTOS</span>
          <span class="nl-card-equip-val">{{ a.equipamentos }}</span>
        </div>
      </div>
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
.nl-cards { display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; }
.nl-card { background: #fff; border: 1px solid #E8E6E1; padding: 20px; }
.nl-card-header { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 12px; }
.nl-card-nome { font-family: 'Syne', sans-serif; font-size: 14px; font-weight: 700; color: #111; }
.nl-card-tipo { font-family: 'DM Mono', monospace; font-size: 8px; color: #BA7517; letter-spacing: 1px; margin-top: 3px; }
.nl-card-desc { font-size: 12px; color: #666; margin-bottom: 16px; line-height: 1.5; }
.nl-card-footer { display: flex; gap: 24px; margin-bottom: 12px; }
.nl-card-label { font-family: 'DM Mono', monospace; font-size: 7px; color: #BA7517; letter-spacing: 1px; margin-bottom: 3px; }
.nl-card-val { font-family: 'Syne', sans-serif; font-size: 16px; font-weight: 700; color: #111; }
.nl-card-equip { border-top: 1px solid #F0EEE9; padding-top: 10px; }
.nl-card-equip-val { font-size: 11px; color: #888; margin-left: 8px; }
.nl-del { color: #ccc; cursor: pointer; font-size: 11px; }
.nl-del:hover { color: #111; }
</style>
