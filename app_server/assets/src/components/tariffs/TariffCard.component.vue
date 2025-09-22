<script setup lang="ts">
import { MainButton } from '@/components/tariffs';
import { decimalNumberFormat } from '@/utils';
import { computed } from 'vue';

const props = defineProps<{
  price: number;
  oldPrice: number;
  perMonth?: number;
  border?: 'green';
}>();

const emit = defineEmits<{
  (e: 'actionClick', price: number): void;
}>();

const formatPrice = (value: number) => {
  return decimalNumberFormat({ value: value / 100, fractionDigits: 0 });
};
const _price = computed<string>(() => formatPrice(props.price));
const _oldPrice = computed<string>(() => formatPrice(props.oldPrice));
const _perMonth = computed<string>(() => formatPrice(props.perMonth ?? 0));

const onActionClick = () => {
  emit('actionClick', props.price);
};
</script>

<template>
  <div :class="['card', border ? `border-${border}` : null]">
    <div class="badge">
      <slot name="badge"></slot>
    </div>
    <div class="term mb-2">
      <slot name="term">
        <span class="gift"></span>
      </slot>
    </div>
    <div class="price-old">{{ _oldPrice }} ₽</div>
    <div class="price-now mt-1">
      {{ _price }} ₽
      <span v-if="perMonth" class="per-month mt-1">({{ _perMonth }} ₽/мес)</span>
    </div>
    <div class="actions d-flex flex-column">
      <MainButton @click="onActionClick">Купить</MainButton>
    </div>
  </div>
</template>

<style scoped lang="scss">
.card {
  background: var(--bg-card);
  color: var(--color-default);
  border-radius: 12px;
  padding: 18px;
  border: 1px solid rgba(255, 255, 255, 0.04);
  backdrop-filter: blur(6px);
  box-shadow: 0 6px 18px rgba(2, 6, 2, 0.6);
  position: relative;
  overflow: hidden;

  &.border-green {
    border: 2px solid var(--green-color);
    transform: translateY(0);
  }

  .badge {
    position: absolute;
    top: 0.75rem;
    right: 0.75rem;
    background: var(--accent-color);
    color: #041004;
    padding: 6px 9px;
    border-radius: 10px;
    font-size: 0.8rem;
  }

  .term {
    font-size: 0.95rem;
    color: var(--muted-color);

    :deep(.gift) {
      display: inline-block;
      margin-left: 0.5rem;
    }
  }

  .price-old {
    color: rgba(255, 255, 255, 0.35);
    text-decoration: line-through;
    font-weight: 600;
  }

  .price-now {
    font-size: 1.25rem;
    font-weight: 800;

    .per-month {
      font-size: 0.85rem;
      color: var(--muted-color);
      font-weight: 600;
    }
  }

  .actions {
    margin-top: 0.75rem;
    gap: 8px;
  }
}
</style>
