<script setup lang="ts">
import { decimalNumberFormat } from '@/utils';
import { computed } from 'vue';

const props = defineProps<{
  price: number;
}>();

const formattedPrice = computed<string>(() =>
  decimalNumberFormat({ value: props.price, fractionDigits: 0 }),
);
</script>

<template>
  <div class="dummy-price-badge">
    <span class="dummy-price-badge__icon" aria-hidden="true">
      <svg viewBox="0 0 24 24">
        <path d="M7.5 18h9.2a4.3 4.3 0 0 0 .3-8.6A5.8 5.8 0 0 0 6 7.8 4.6 4.6 0 0 0 7.5 18Z" />
        <path d="m9.5 13 2.5-2.5 2.5 2.5M12 10.8v4.7" />
      </svg>
    </span>

    <span>
      1 камера — <strong>{{ formattedPrice }} ₽ / месяц</strong>
    </span>
  </div>
</template>

<style scoped lang="scss">
.dummy-price-badge {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  padding: 9px 15px;
  border: 2px solid #d0aa50;
  border-radius: 14px;
  background: rgba(15, 26, 40, 0.25);
  color: #fff;
  font-size: 17px;
  font-weight: 700;
}

.dummy-price-badge strong {
  color: #f3cf72;
}

.dummy-price-badge__icon {
  display: grid;
  width: 25px;
  height: 25px;
  place-items: center;
  color: #f3cf72;
}

.dummy-price-badge__icon svg {
  width: 24px;
  height: 24px;
  fill: none;
  stroke: currentColor;
  stroke-linecap: round;
  stroke-linejoin: round;
  stroke-width: 1.8;
}

@media (max-width: 640px) {
  .dummy-price-badge {
    max-width: 100%;
    padding: 8px 12px;
    font-size: 15px;
  }
}
</style>
