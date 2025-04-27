<script setup lang="ts">
import Agreement from './Agreement.component.vue';
import FooterComponent from './Footer.component.vue';
import OwnerInfo from './OwnerInfo.component.vue';
import Receipt from './Receipt.component.vue';
import SectionTitle from './Title.component.vue';
</script>

<template>
  <div class="subscribe position-relative d-flex flex-column justify-content-between">
    <div class="head d-flex flex-column align-items-start justify-content-between">
      <section-title class="mb-2">Оформить подписку</section-title>
      <p class="mb-0">
        Мы&nbsp;&mdash; рекламная компания, которая предоставляет услуги по&nbsp;продвижению вашего
        бизнеса в&nbsp;мессенджере Telegram по&nbsp;г.&nbsp;Махачкала.
      </p>
      <p>Стоимость подписки составляет 200 рублей в месяц.</p>
    </div>
    <receipt :items="[{ name: 'Подписка', price: 20000 }]" />
    <agreement class="mt-3" />
    <owner-info class="mt-3" />
  </div>
  <footer-component class="mt-3" />
</template>

<style scoped lang="scss">
.subscribe {
  font-family: var(--font-family-secondary);
  border-radius: 36px;
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
@media (max-width: 991.98px) {
  .subscribe {
    margin-top: 0;
  }
}
</style>
