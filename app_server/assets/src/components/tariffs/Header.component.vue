<script setup lang="ts">
import { MainButton } from '@/components/tariffs';

const emit = defineEmits<{
  (e: 'headerButtonClick'): void;
}>();
</script>

<template>
  <header class="d-flex flex-column align-items-center">
    <div class="logo d-flex justify-content-center align-items-center">PAY</div>
    <h1>Тарифы и оплата</h1>
    <p class="lead">Выберите подходящий период. Без автопродления — оплата разовая.</p>
    <MainButton class="mt-3" @click="emit('headerButtonClick')">Оплатить сейчас</MainButton>
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
}
</style>
