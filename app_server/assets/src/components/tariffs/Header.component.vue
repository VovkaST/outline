<script setup lang="ts"></script>

<template>
  <header class="d-flex flex-column align-items-center">
    <div class="logo d-flex justify-content-center align-items-center">PAY</div>
    <h1>Тарифы и оплата</h1>
    <p class="lead">Выберите подходящий период. Без автопродления — оплата разовая.</p>
    <button
      class="hero-cta"
      onclick="document.getElementById('plans').scrollIntoView({behavior:'smooth'})"
    >
      Оплатить сейчас
    </button>
  </header>
</template>

<style scoped lang="scss">
header {
  text-align: center;
  margin-bottom: 24px;

  .logo {
    width: 56px;
    height: 56px;
    border-radius: 10px;
    margin-bottom: 12px;
    background: linear-gradient(135deg, var(--green-color), var(--dark-green-color));
    font-weight: 700;
    color: #041004;
  }

  h1 {
    font-size: 22px;
    font-weight: 700;
    margin: 0;
  }

  p.lead {
    font-size: 16px;
    font-weight: 400;
    color: var(--muted-color);
    margin: 6px 0 0;
  }

  .hero-cta {
    background: linear-gradient(90deg, var(--green-color), var(--dark-green-color));
    padding: 12px 16px;
    border-radius: 10px;
    color: #041004;
    font-size: 0.85rem;
    font-weight: 700;
    line-height: normal;
    border: none;
    cursor: pointer;
    margin-top: 16px;
  }
}
</style>
