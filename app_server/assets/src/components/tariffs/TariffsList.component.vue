<script setup lang="ts">
import { TariffCard } from '@/components/tariffs';

const emit = defineEmits<{
  (e: 'actionClick', price: number): void;
}>();

const onActionClick = (price: number) => {
  emit('actionClick', price);
};
</script>
<template>
  <div id="plans" class="d-flex flex-column">
    <TariffCard :price="199" :old-price="249" :per-month="199" @actionClick="onActionClick">
      <template v-slot:term> 1 месяц </template>
    </TariffCard>

    <TariffCard
      :price="499"
      :old-price="597"
      :per-month="166"
      border="green"
      @actionClick="onActionClick"
    >
      <template v-slot:term> 3 месяца </template>
      <template v-slot:badge> — Выгодно — </template>
    </TariffCard>

    <TariffCard :price="899" :old-price="1393" :per-month="128" @actionClick="onActionClick">
      <template v-slot:term> 6 месяцев <span class="gift">+ 1 в подарок 🎁</span> </template>
    </TariffCard>

    <TariffCard :price="1999" :old-price="2085" :per-month="133" @actionClick="onActionClick">
      <template v-slot:term> 12 месяцев <span class="gift">+ 3 в подарок 🎁</span> </template>
    </TariffCard>
  </div>
</template>
<style lang="scss" module></style>
