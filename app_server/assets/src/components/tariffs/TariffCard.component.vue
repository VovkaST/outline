<script setup lang="ts">
import { decimalNumberFormat } from '@/utils';
import { computed } from 'vue';

const props = withDefaults(
  defineProps<{
    period: string;
    price: number;
    featured?: boolean;
    disabled?: boolean;
  }>(),
  { featured: false, disabled: false },
);

const emit = defineEmits<{
  (e: 'actionClick', price: number): void;
}>();

const formattedPrice = computed<string>(() =>
  decimalNumberFormat({ value: props.price, fractionDigits: 0 }),
);

const onClick = () => {
  if (props.disabled) return;
  emit('actionClick', props.price);
};
</script>

<template>
  <button type="button" class="btn" :class="{ featured }" :disabled="disabled" @click="onClick">
    <span class="btn-period">{{ period }}</span>
    <span class="btn-price">{{ formattedPrice }} ₽</span>
  </button>
</template>

<style scoped lang="scss">
.btn {
  width: 100%;
  background: #fff;
  border: 1.5px solid var(--border);
  padding: 18px 22px;
  border-radius: 12px;
  font-family: inherit;
  font-size: 15px;
  font-weight: 600;
  color: var(--ink);
  cursor: pointer;
  display: flex;
  justify-content: space-between;
  align-items: center;
  transition: all 0.15s ease;
}

.btn:hover:not(:disabled) {
  border-color: var(--primary);
  transform: translateY(-1px);
  box-shadow: 0 6px 18px rgba(201, 169, 97, 0.18);
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-period {
  color: var(--ink);
}

.btn-price {
  color: var(--primary);
  font-weight: 700;
}

.btn.featured {
  background: var(--primary);
  border-color: var(--primary);
  color: #fff;
  box-shadow: 0 4px 14px rgba(201, 169, 97, 0.35);
}

.btn.featured .btn-price {
  color: #fff;
}

.btn.featured:hover:not(:disabled) {
  background: var(--primary-hover);
}

@media (max-width: 380px) {
  .btn {
    padding: 16px 18px;
    font-size: 14px;
  }
}

@media (hover: none) {
  .btn:hover {
    border-color: var(--border);
    transform: none;
    box-shadow: none;
  }

  .btn.featured:hover {
    background: var(--primary);
  }

  .btn:active:not(:disabled) {
    transform: scale(0.98);
    transition: transform 0.1s;
  }
}
</style>
