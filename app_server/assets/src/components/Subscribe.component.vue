<script setup lang="ts">
import Agreement from './Agreement.component.vue';
import OwnerInfo from './OwnerInfo.component.vue';
import Receipt from './Receipt.component.vue';
import SectionTitle from './Title.component.vue';
</script>

<template>
  <div class="subscribe position-relative d-flex flex-column justify-content-between">
    <div class="head d-flex flex-column align-items-start justify-content-between">
      <section-title class="mb-2">Оформить подписку</section-title>
      <p class="mb-0">Услуги на подключение к нашим серверам бота TRIO на 1 месяц.</p>
      <p>
        Описание: Вы оплачиваете ключ, который выдал вам бот, для доступа к нашему VPN сервису в
        течение 1 месяца.
      </p>
    </div>
    <receipt :items="[{ name: 'Подписка', price: 15000 }]" />
    <agreement class="mt-3" />
    <owner-info class="mt-3" />
  </div>
</template>

<style scoped lang="scss">
.subscribe {
  font-family: var(--font-family-secondary);
  border-radius: 36px;
  min-width: 1032px;
  max-width: 1200px;
  padding: 20px 1rem 1rem;
  margin: max(50px, 4em) auto 0;
  box-shadow: 0 4px 14px 2px rgba(0, 0, 0, 0.1);
  background: #15172170;
  border: 1px solid #414765;
  backdrop-filter: blur(6px);

  .head {
    color: #767577;
  }
}
</style>
