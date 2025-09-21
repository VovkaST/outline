<script setup lang="ts">
import { Header, TariffCard, PayForm, Delimiter } from '@/components/tariffs';
</script>
<template>
  <div class="tariff-form-container">
    <Header />
    <div id="plans" class="d-flex flex-column">
      <TariffCard :price="199" :old-price="249" :per-month="199">
        <template v-slot:term> 1 месяц </template>
      </TariffCard>

      <TariffCard :price="499" :old-price="597" :per-month="166" border="green">
        <template v-slot:term> 3 месяца </template>
        <template v-slot:badge> — Выгодно — </template>
      </TariffCard>

      <TariffCard :price="899" :old-price="1393" :per-month="128">
        <template v-slot:term> 6 месяцев <span class="gift">+ 1 в подарок 🎁</span> </template>
      </TariffCard>

      <TariffCard :price="1999" :old-price="2085" :per-month="133">
        <template v-slot:term> 12 месяцев <span class="gift">+ 3 в подарок 🎁</span> </template>
      </TariffCard>
    </div>

    <Delimiter />

    <PayForm :amount="1000">
      <template v-slot:header>Оформление заказа</template>
      <template v-slot:description>
        Нажмите на выбранный тариф выше — сумма автоматически подставится в форму.
      </template>
      <template v-slot:footnote>
        Безопасные платежи. Никаких подписок, оплата разовая. Цены указаны с учётом акции.
      </template>
    </PayForm>
    <footer>© 2025 — Все права защищены</footer>
  </div>
</template>
<style lang="scss" scoped>
.tariff-form-container {
  max-width: 600px;
  margin: 0 auto;
  padding: 16px;

  #plans {
    gap: 16px;
    margin-top: 16px;
  }

  footer {
    margin-top: 40px;
    color: var(--muted-color);
    font-size: 13px;
    text-align: center;
  }
}
</style>
