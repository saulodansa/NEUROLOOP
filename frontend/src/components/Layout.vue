<script setup>
import { useRouter, useRoute } from 'vue-router'
const router = useRouter()
const route = useRoute()
</script>

<template>
  <div class="nl-root">
    <div class="nl-header">
      <div>
        <div class="nl-logo" @click="router.push('/')">NEUROLOOP</div>
        <div class="nl-tag">// SISTEMA DE GESTÃO v0.1</div>
      </div>
      <div class="nl-status">
        <div class="nl-dot"></div>
        ONLINE
      </div>
    </div>

    <div class="nl-grid">
      <div class="nl-nav">
        <div class="nl-nav-section">// PRINCIPAL</div>
        <div class="nl-nav-item" :class="{ active: route.path === '/' }" @click="router.push('/')">PAINEL</div>
        <div class="nl-nav-item" :class="{ active: route.path === '/clientes' }" @click="router.push('/clientes')">CLIENTES</div>
        <div class="nl-nav-item" :class="{ active: route.path === '/propostas' }" @click="router.push('/propostas')">PROPOSTAS</div>
        <div class="nl-nav-item" :class="{ active: route.path === '/eventos' }" @click="router.push('/eventos')">EVENTOS</div>
        <div class="nl-nav-section">// OPERAÇÃO</div>
        <div class="nl-nav-item" :class="{ active: route.path === '/portfolio' }" @click="router.push('/portfolio')">PORTFÓLIO</div>
        <div class="nl-nav-item" :class="{ active: route.path === '/ativos' }" @click="router.push('/ativos')">ATIVOS</div>
        <div class="nl-nav-item" :class="{ active: route.path === '/contratos' }" @click="router.push('/contratos')">CONTRATOS</div>
        <div class="nl-nav-section">// FINANCEIRO</div>
        <div class="nl-nav-item" :class="{ active: route.path === '/financeiro' }" @click="router.push('/financeiro')">CAIXA</div>
        <div class="nl-nav-item" :class="{ active: route.path === '/contas-receber' }" @click="router.push('/contas-receber')">CONTAS A RECEBER</div>
      </div>

      <div class="nl-content">
        <slot />  
      </div>
    </div>
  </div>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=DM+Sans:wght@300;400;500&family=DM+Mono:wght@400&display=swap');
.nl-root { background: #000; color: #fff; min-height: 100vh; font-family: 'DM Sans', sans-serif; }
.nl-header { display: flex; align-items: center; justify-content: space-between; padding: 18px 28px; border-bottom: 1px solid rgba(255,255,255,0.07); }
.nl-logo { font-family: 'Syne', sans-serif; font-size: 18px; font-weight: 800; letter-spacing: 3px; cursor: pointer; }
.nl-tag { font-family: 'DM Mono', monospace; font-size: 11px; color: rgba(245,158,11,0.6); letter-spacing: 2px; margin-top: 2px; }
.nl-status { display: flex; align-items: center; gap: 6px; font-size: 12px; color: rgba(255,255,255,0.3); font-family: 'DM Mono', monospace; letter-spacing: 1px; }
.nl-dot { width: 5px; height: 5px; border-radius: 50%; background: #f59e0b; animation: pulse 2s infinite; }
@keyframes pulse { 0%,100%{opacity:1} 50%{opacity:0.3} }
.nl-grid { display: grid; grid-template-columns: 220px 1fr; min-height: calc(100vh - 60px); }
.nl-nav { border-right: 1px solid rgba(255,255,255,0.07); padding: 24px 0; }
.nl-nav-section { font-size: 10px; color: rgba(245,158,11,0.35); letter-spacing: 3px; padding: 16px 24px 6px; font-family: 'DM Mono', monospace; }
.nl-nav-item { padding: 10px 24px; font-size: 13px; font-family: 'DM Mono', monospace; letter-spacing: 2px; color: rgba(255,255,255,0.3); cursor: pointer; border-left: 2px solid transparent; transition: all 0.2s; }
.nl-nav-item:hover { color: rgba(255,255,255,0.7); }
.nl-nav-item.active { color: #f59e0b; border-left-color: #f59e0b; }
.nl-content { padding: 28px; overflow-y: auto; background: #F6F5F3; }
</style>