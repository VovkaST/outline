<script setup lang="ts"></script>
<template>
  <div class="pay-box">
    <p>💳 <strong>Карта, Qiwi, ЮMoney</strong></p>
    <p>⚡ Подключение за 60 сек</p>
    <div class="ssl-row">
      <i class="fas fa-shield-alt"></i>
      <span>SSL защита · Безопасные платежи</span>
    </div>
  </div>
</template>

<style scoped lang="scss">
.pay-box {
  background: var(--light);
  border: 1px solid var(--border);
  border-radius: 10px;
  padding: 14px;
  margin-bottom: 14px;
  text-align: center;

  p {
    font-size: var(--sm);
    font-weight: 400;
    color: var(--t2);
    margin-bottom: 4px;
    line-height: 1.55;

    strong {
      font-weight: 700;
    }
  }

  .ssl-row {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 5px;
    margin-top: 8px;
    color: var(--g);
    font-size: var(--sm);
    font-weight: 600;
  }
}

@media (prefers-color-scheme: dark) {
  .pay-box {
    background: var(--bg-slate);
    border-color: var(--border);

    p {
      color: var(--t2);
    }
  }
}
</style>
