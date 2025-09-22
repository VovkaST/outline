<script setup lang="ts">
import { TariffCard } from '@/components/tariffs';
import { ref } from 'vue';

const props = withDefaults(
  defineProps<{
    wait?: boolean;
  }>(),
  { wait: false },
);

const selectedPrice = ref<number>(0);

const isTariffSelected = (price: number): boolean => props.wait && selectedPrice.value === price;

const emit = defineEmits<{
  (e: 'actionClick', price: number): void;
}>();

const onActionClick = (price: number) => {
  selectedPrice.value = price;
  emit('actionClick', price);
};
</script>
<template>
  <div id="plans" class="d-flex flex-column mt-1">
    <TariffCard
      :price="19900"
      :old-price="24900"
      :per-month="19900"
      :wait="isTariffSelected(19900)"
      @actionClick="onActionClick"
    >
      <template v-slot:term> 1 месяц </template>
    </TariffCard>

    <TariffCard
      :price="49900"
      :old-price="59700"
      :per-month="16600"
      :wait="isTariffSelected(49900)"
      @actionClick="onActionClick"
    >
      <template v-slot:term> 3 месяца </template>
      <template v-slot:badge> — Выгодно — </template>
    </TariffCard>

    <TariffCard
      :price="89900"
      :old-price="139300"
      :per-month="12800"
      :wait="isTariffSelected(89900)"
      @actionClick="onActionClick"
    >
      <template v-slot:term> 6 месяцев <span class="gift">+ 1 в подарок 🎁</span> </template>
    </TariffCard>

    <TariffCard
      :price="199900"
      :old-price="208500"
      :per-month="13300"
      :wait="isTariffSelected(199900)"
      @actionClick="onActionClick"
    >
      <template v-slot:term> 12 месяцев <span class="gift">+ 3 в подарок 🎁</span> </template>
    </TariffCard>
  </div>
</template>
<style lang="scss" scoped>
#plans {
  gap: 1rem;
}
</style>
