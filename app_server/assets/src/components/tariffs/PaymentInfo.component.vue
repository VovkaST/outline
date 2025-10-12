<script setup lang="ts"></script>
<template>
  <div class="payment-info">
    <p>Оплата осуществляется через защищенный шлюз ЮКасса</p>
    <p>Мы принимаем: банковские карты, электронные кошельки, интернет-банкинг</p>
    <div class="secure-payment">
      <i class="fas fa-shield-alt"></i>
      <span>Безопасная оплата</span>
    </div>
  </div>
</template>
<style scoped lang="scss">
.payment-info {
  text-align: center;
  padding: 18px;
  background: var(--light);
  border-radius: 10px;
  margin-top: 25px;
  border: 1px solid var(--border);

  p {
    margin-bottom: 8px;
    color: var(--gray);
    line-height: 1.3;
    font-size: 0.9rem;
  }

  .secure-payment {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
    margin-top: 10px;
    color: var(--secondary);
    font-weight: 600;
    font-size: 0.9rem;
  }
}

@media (max-width: 768px) {
  .payment-info {
    padding: 15px;
    margin-top: 20px;
  }
}
</style>
