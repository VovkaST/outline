<script setup lang="ts"></script>
<template>
  <div class="payment-info">
    <p class="text-small">💳 <strong>Оплата картой, Qiwi, Яндекс.Деньги, Crypto</strong></p>
    <p class="text-small">⚡ Подключение за 60 секунд • 🔒 Гарантия возврата</p>
    <div class="secure-payment text-small">
      <i class="fas fa-shield-alt"></i>
      <span>SSL защита • Безопасные платежи</span>
    </div>
  </div>
</template>
<style scoped lang="scss">
.payment-info {
  text-align: center;
  padding: 15px 12px;
  background: var(--light);
  border-radius: 10px;
  margin-top: 15px;
  border: 1px solid #e5e7eb;

  p {
    margin-bottom: 4px;
    color: #6b7280;
    line-height: 1.3;
  }

  .secure-payment {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 4px;
    margin-top: 6px;
    color: var(--secondary);
    font-weight: 600;

    i {
      font-size: 0.8rem;
    }
  }
}

@media (max-width: 768px) {
  .payment-info {
    padding: 15px;
    margin-top: 20px;
  }
}
</style>
