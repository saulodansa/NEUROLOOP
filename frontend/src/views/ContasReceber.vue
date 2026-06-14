<script setup>
import { ref, onMounted, computed } from 'vue'

const propostas = ref([])
const lancamentos = ref([])

async function carregar() {
  const [rp, rl] = await Promise.all([
    fetch('https://neuroloop-production-841a.up.railway.app/propostas/'),
    fetch('https://neuroloop-production-841a.up.railway.app/financeiro/')
  ])
  propostas.value = await rp.json()
  lancamentos.value = await rl.json()
}

const contasAReceber = computed(() => {
  const propostasAprovadas = propostas.value.filter(p => p.status === 'aprovada')
  return propostasAprovadas.map(p => {
    const recebido = lancamentos.value
      .filter(l => l.proposta_id === p.id && l.tipo === 'receita')
      .reduce((acc, l) => acc + l.valor, 0)
    const pendente = (p.valor_total || 0) - recebido
    return { ...p, recebido, pendente }
  })
})

const totalPendente = computed(() =>
  contasAReceber.value.reduce((acc, p) => acc + p.pendente, 0)
)

const totalRecebido = computed(() =>
  contasAReceber.value.reduce((acc, p) => acc + p.recebido, 0)
)

async function registrarRecebimento(proposta) {
  await fetch('https://neuroloop-production-841a.up.railway.app/financeiro/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      proposta_id: proposta.id,
      descricao: `Recebimento — ${proposta.cliente_nome}`,
      tipo: 'receita',
      valor: proposta.pendente,
      data: new Date().toISOString()
    })
  })
  carregar()
}

onMounted(carregar)
</script>

<template>
  <div class="nl-page">
    <div class="nl-page-header">
      <div>
        <div class="nl-cota">// FINANCEIRO</div>
        <div class="nl-page-title">Contas a Receber</div>
      </div>
    </div>

    <div class="nl-metrics">
      <div class="nl-metric">
        <div class="nl-metric-label">TOTAL A RECEBER</div>
        <div class="nl-metric-value" style="color:#854F0B">
          R$ {{ totalPendente.toLocaleString('pt-BR') }}
        </div>
      </div>
      <div class="nl-metric">
        <div class="nl-metric-label">JÁ RECEBIDO</div>
        <div class="nl-metric-value" style="color:#3B6D11">
          R$ {{ totalRecebido.toLocaleString('pt-BR') }}
        </div>
      </div>
      <div class="nl-metric">
        <div class="nl-metric-label">PROPOSTAS APROVADAS</div>
        <div class="nl-metric-value">{{ contasAReceber.length }}</div>
      </div>
    </div>

    <div class="nl-table-wrap">
      <table class="nl-table">
        <thead>
          <tr>
            <th>CLIENTE</th>
            <th>DESCRIÇÃO</th>
            <th>VALOR TOTAL</th>
            <th>JÁ RECEBIDO</th>
            <th>PENDENTE</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          <tr v-if="contasAReceber.length === 0">
            <td colspan="6" style="text-align:center; color:#aaa; padding:40px;">
              Nenhuma proposta aprovada com valor pendente
            </td>
          </tr>
          <tr v-for="p in contasAReceber" :key="p.id">
            <td style="font-weight:500">{{ p.cliente_nome }}</td>
            <td style="color:#666">{{ p.descricao || '—' }}</td>
            <td style="font-family:'DM Mono',monospace">
              R$ {{ (p.valor_total || 0).toLocaleString('pt-BR') }}
            </td>
            <td style="font-family:'DM Mono',monospace; color:#3B6D11">
              R$ {{ p.recebido.toLocaleString('pt-BR') }}
            </td>
            <td style="font-family:'DM Mono',monospace; color:#854F0B; font-weight:500">
              R$ {{ p.pendente.toLocaleString('pt-BR') }}
            </td>
            <td>
              <button
                v-if="p.pendente > 0"
                class="nl-btn-sm"
                @click="registrarRecebimento(p)"
              >
                RECEBER
              </button>
              <span v-else style="font-family:'DM Mono',monospace; font-size:9px; color:#3B6D11">
                QUITADO
              </span>
            </td>
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
.nl-metrics { display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; margin-bottom: 24px; }
.nl-metric { background: #fff; border: 1px solid #E8E6E1; padding: 20px; }
.nl-metric-label { font-size: 8px; font-family: 'DM Mono', monospace; color: #BA7517; letter-spacing: 2px; margin-bottom: 10px; }
.nl-metric-value { font-family: 'DM Mono', monospace; font-size: 22px; font-weight: 400; color: #111; letter-spacing: -0.5px; }
.nl-table-wrap { background: #fff; border: 1px solid #E8E6E1; }
.nl-table { width: 100%; border-collapse: collapse; font-size: 13px; }
.nl-table th { font-family: 'DM Mono', monospace; font-size: 8px; letter-spacing: 2px; color: #BA7517; padding: 12px 16px; text-align: left; border-bottom: 1px solid #E8E6E1; background: #F6F5F3; }
.nl-table td { padding: 13px 16px; border-bottom: 1px solid #F0EEE9; color: #222; }
.nl-table tr:last-child td { border-bottom: none; }
.nl-table tr:hover td { background: #F9F8F6; }
.nl-btn-sm { background: #000; border: none; color: #f59e0b; font-family: 'DM Mono', monospace; font-size: 8px; letter-spacing: 1px; padding: 5px 12px; cursor: pointer; }
.nl-btn-sm:hover { background: #1a1a1a; }
</style>
