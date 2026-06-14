<script setup>
import { ref, onMounted } from 'vue'

const dados = ref({
  receita: 0,
  pipeline: 0,
  eventos: 0,
  saldo: 0
})

async function carregar() {
  const [rf, rp, re] = await Promise.all([
    fetch('http://127.0.0.1:8000/financeiro/resumo'),
    fetch('http://127.0.0.1:8000/propostas/'),
    fetch('http://127.0.0.1:8000/eventos/')
  ])
  const financeiro = await rf.json()
  const propostas = await rp.json()
  const eventos = await re.json()

  const pipeline = propostas
    .filter(p => ['enviada', 'negociando'].includes(p.status))
    .reduce((acc, p) => acc + (p.valor_total || 0), 0)

  dados.value = {
    receita: financeiro.receita,
    pipeline: pipeline,
    eventos: eventos.length,
    saldo: financeiro.saldo
  }
}

onMounted(carregar)
</script>

<template>
  <div>
    <div class="nl-cota">// PAINEL EXECUTIVO</div>
    <div class="nl-metrics">
      <div class="nl-metric">
        <div class="nl-metric-label">RECEITA CONFIRMADA</div>
        <div class="nl-metric-value">R$ {{ dados.receita.toLocaleString('pt-BR') }}</div>
      </div>
      <div class="nl-metric">
        <div class="nl-metric-label">PIPELINE ABERTO</div>
        <div class="nl-metric-value">R$ {{ dados.pipeline.toLocaleString('pt-BR') }}</div>
      </div>
      <div class="nl-metric">
        <div class="nl-metric-label">EVENTOS AGENDADOS</div>
        <div class="nl-metric-value">{{ dados.eventos }}</div>
      </div>
      <div class="nl-metric">
        <div class="nl-metric-label">SALDO EM CAIXA</div>
        <div class="nl-metric-value" :style="{ color: dados.saldo >= 0 ? '#3B6D11' : '#A32D2D' }">
          R$ {{ dados.saldo.toLocaleString('pt-BR') }}
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=DM+Mono:wght@400&display=swap');
.nl-cota { font-family: 'DM Mono', monospace; font-size: 8px; color: #BA7517; letter-spacing: 2px; margin-bottom: 20px; }
.nl-metrics { display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; }
.nl-metric { background: #fff; border: 1px solid #E8E6E1; padding: 20px; }
.nl-metric-label { font-size: 8px; font-family: 'DM Mono', monospace; color: #BA7517; letter-spacing: 2px; margin-bottom: 10px; }
.nl-metric-value { font-family: 'DM Mono', monospace; font-size: 24px; font-weight: 400; color: #111; letter-spacing: -0.5px; }
</style>