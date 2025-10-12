<script setup lang="ts"></script>

<template>
  <header>
    <div class="logo">Halal<span>_VPN</span></div>
    <h1>Тарифы и оплата</h1>
    <p class="subtitle">Выберите подходящий период. Без автопродления — оплата разовая.</p>
  </header>
</template>

<style scoped lang="scss">
header {
  padding: 30px 20px 15px;
  text-align: center;
  background: linear-gradient(135deg, var(--primary), var(--primary-dark));
  color: white;

  .logo {
    font-size: 1.8rem;
    font-weight: 700;
    margin-bottom: 12px;
    color: white;

    span {
      color: #10b981;
    }
  }

  h1 {
    font-size: 1.8rem;
    font-weight: 700;
    margin-bottom: 8px;
  }

  .subtitle {
    font-size: 1rem;
    opacity: 0.9;
    max-width: 600px;
    margin: 0 auto;
    line-height: 1.3;
  }
}
</style>
