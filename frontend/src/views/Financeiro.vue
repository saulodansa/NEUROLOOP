<script setup>
import { ref, onMounted, computed } from 'vue'

const lancamentos = ref([])
const resumo = ref({ receita: 0, custo: 0, saldo: 0 })
const mostrarForm = ref(false)
const form = ref({
  descricao: '', tipo: 'receita', valor: null, data: '', proposta_id: null
})

async function carregar() {
  const [rl, rr] = await Promise.all([
    fetch('http://127.0.0.1:8000/financeiro/'),
    fetch('http://127.0.0.1:8000/financeiro/resumo')
  ])
  lancamentos.value = await rl.json()
  resumo.value = await rr.json()
}

async function salvar() {
  const payload = {
    descricao: form.value.descricao,
    tipo: form.value.tipo,
    valor: form.value.valor,
    proposta_id: form.value.proposta_id || null,
    data: form.value.data ? new Date(form.value.data).toISOString() : null
  }
  await fetch('http://127.0.0.1:8000/financeiro/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload)
  })
  form.value = { descricao: '', tipo: 'receita', valor: null, data: '', proposta_id: null }
  mostrarForm.value = false
  carregar()
}

async function deletar(id) {
  await fetch(`http://127.0.0.1:8000/financeiro/${id}`, { method: 'DELETE' })
  carregar()
}

onMounted(carregar)
</script>

<template>
  <div class="nl-page">
    <div class="nl-page-header">
      <div>
        <div class="nl-cota">// FINANCEIRO</div>
        <div class="nl-page-title">Caixa</div>
      </div>
      <button class="nl-btn" @click="mostrarForm = !mostrarForm">+ NOVO LANÇAMENTO</button>
    </div>

    <div class="nl-metrics">
      <div class="nl-metric">
        <div class="nl-metric-label">RECEITA TOTAL</div>
        <div class="nl-metric-value">R$ {{ resumo.receita.toLocaleString('pt-BR') }}</div>
      </div>
      <div class="nl-metric">
        <div class="nl-metric-label">CUSTOS TOTAIS</div>
        <div class="nl-metric-value" style="color:#A32D2D">R$ {{ resumo.custo.toLocaleString('pt-BR') }}</div>
      </div>
      <div class="nl-metric">
        <div class="nl-metric-label">SALDO</div>
        <div class="nl-metric-value" :style="{ color: resumo.saldo >= 0 ? '#3B6D11' : '#A32D2D' }">
          R$ {{ resumo.saldo.toLocaleString('pt-BR') }}
        </div>
      </div>
    </div>

    <div v-if="mostrarForm" class="nl-form">
      <div class="nl-cota" style="margin-bottom:16px">// NOVO LANÇAMENTO</div>
      <div class="nl-form-grid">
        <div class="nl-field" style="grid-column: span 2">
          <label>DESCRIÇÃO *</label>
          <input v-model="form.descricao" placeholder="Ex: Pagamento Petrobras - Expo Rio" />
        </div>
        <div class="nl-field">
          <label>TIPO</label>
          <select v-model="form.tipo">
            <option value="receita">Receita</option>
            <option value="custo">Custo</option>
          </select>
        </div>
        <div class="nl-field">
          <label>VALOR (R$)</label>
          <input v-model="form.valor" type="number" placeholder="0" />
        </div>
        <div class="nl-field">
          <label>DATA</label>
          <input v-model="form.data" type="date" />
        </div>
      </div>
      <button class="nl-btn" @click="salvar">SALVAR</button>
    </div>

    <div class="nl-table-wrap">
      <table class="nl-table">
        <thead>
          <tr>
            <th>DESCRIÇÃO</th>
            <th>TIPO</th>
            <th>VALOR</th>
            <th>DATA</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          <tr v-if="lancamentos.length === 0">
            <td colspan="5" style="text-align:center; color:#aaa; padding:40px;">Nenhum lançamento cadastrado</td>
          </tr>
          <tr v-for="l in lancamentos" :key="l.id">
            <td style="font-weight:500">{{ l.descricao }}</td>
            <td>
              <span class="nl-badge" :class="l.tipo === 'receita' ? 'ok' : 'danger'">
                {{ l.tipo === 'receita' ? 'RECEITA' : 'CUSTO' }}
              </span>
            </td>
            <td style="font-family:'DM Mono',monospace" :style="{ color: l.tipo === 'receita' ? '#3B6D11' : '#A32D2D' }">
              {{ l.tipo === 'custo' ? '- ' : '+ ' }}R$ {{ l.valor.toLocaleString('pt-BR') }}
            </td>
            <td style="color:#aaa; font-size:12px">
              {{ l.data ? new Date(l.data).toLocaleDateString('pt-BR') : '—' }}
            </td>
            <td><span class="nl-del" @click="deletar(l.id)">✕</span></td>
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
.nl-metrics { display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; margin-bottom: 24px; }
.nl-metric { background: #fff; border: 1px solid #E8E6E1; padding: 20px; }
.nl-metric-label { font-size: 8px; font-family: 'DM Mono', monospace; color: #BA7517; letter-spacing: 2px; margin-bottom: 10px; }
.nl-metric-value { font-family: 'DM Mono', monospace; font-size: 22px; font-weight: 400; color: #111; letter-spacing: -0.5px; }
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
.nl-badge { display: inline-block; font-size: 8px; font-family: 'DM Mono', monospace; padding: 2px 8px; letter-spacing: 1px; }
.nl-badge.ok { background: #EAF3DE; color: #3B6D11; }
.nl-badge.danger { background: #FCEBEB; color: #A32D2D; }
.nl-del { color: #ccc; cursor: pointer; font-size: 11px; }
.nl-del:hover { color: #111; }
</style>