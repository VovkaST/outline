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
  <div id="plans" class="d-flex flex-column mt-1">
    <TariffCard :price="19900" :old-price="24900" :per-month="19900" @actionClick="onActionClick">
      <template v-slot:term> 1 месяц </template>
    </TariffCard>

    <TariffCard
      :price="49900"
      :old-price="59700"
      :per-month="16600"
      border="green"
      @actionClick="onActionClick"
    >
      <template v-slot:term> 3 месяца </template>
      <template v-slot:badge> — Выгодно — </template>
    </TariffCard>

    <TariffCard :price="89900" :old-price="139300" :per-month="12800" @actionClick="onActionClick">
      <template v-slot:term> 6 месяцев <span class="gift">+ 1 в подарок 🎁</span> </template>
    </TariffCard>

    <TariffCard :price="199900" :old-price="208500" :per-month="13300" @actionClick="onActionClick">
      <template v-slot:term> 12 месяцев <span class="gift">+ 3 в подарок 🎁</span> </template>
    </TariffCard>
  </div>
</template>
<style lang="scss" scoped>
#plans {
  gap: 1rem;
}
</style>
