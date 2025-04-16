<script setup lang="ts">
import type { ReceiptItem } from '../stores/types.ts';
import { computed } from 'vue';

const props = withDefaults(
  defineProps<{
    items: ReceiptItem[];
    currency?: string;
  }>(),
  { currency: '₽' },
);

const totalSum = computed<number>(() =>
  props.items.reduce((currentSum, item) => currentSum + item.price, 0),
);
</script>

<template>
  <div class="receipt d-flex flex-column align-items-center">
    <div class="sum" v-for="(item, i) in items" :key="i">
      <span>{{ item.name }}</span>
      <span>{{ item.price / 100 }} {{ currency }}</span>
    </div>
    <div class="sum">
      <span>Итого:</span>
      <span>{{ totalSum / 100 }} {{ currency }}</span>
    </div>
  </div>
</template>

<style scoped lang="scss">
.receipt {
  padding: 30px 45px 40px;
  background-color: #3e1d115b;
  color: #8e96a3;
  border-radius: var(--block-border-radius);

  .sum {
    display: flex;
    justify-content: space-between;
    width: 100%;
    border-bottom: 1px dashed #82938f;
    margin-top: 10px;

    &:first-child {
      margin-top: 0;
    }
  }
}
</style>
