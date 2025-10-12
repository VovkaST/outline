<script setup lang="ts">
import { MainButton } from '@/components/tariffs';
import { decimalNumberFormat } from '@/utils';
import { computed } from 'vue';

const props = withDefaults(
  defineProps<{
    price: number;
    oldPrice: number;
    perMonth?: number;
    wait?: boolean;
    isPopular?: boolean;
  }>(),
  { wait: false, isPopular: false },
);

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

defineExpose({ price: props.price });
</script>

<template>
  <div class="tariff" :class="{ popular: isPopular }">
    <div v-if="isPopular" class="popular-badge">Выгодно</div>
    <div class="tariff-header">
      <div class="period">
        <slot name="term" />
      </div>
      <div class="price-container">
        <div class="price-old">{{ _oldPrice }} ₽</div>
        <div class="price-new">{{ _price }} ₽</div>
        <div class="price-per-month">({{ _perMonth }} ₽/мес)</div>
      </div>
    </div>
    <ul class="features">
      <slot name="features" />
    </ul>
    <MainButton @click="onActionClick" :wait="wait" :color="isPopular ? 'green' : 'default'">
      Оплатить сейчас
    </MainButton>
  </div>
</template>

<style scoped lang="scss">
.tariff {
  background: white;
  border-radius: 15px;
  padding: 25px 20px;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.05);
  transition: all 0.3s ease;
  border: 1px solid var(--border);
  position: relative;
  display: flex;
  flex-direction: column;

  &:hover {
    transform: translateY(-5px);
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
  }

  &.popular {
    border: 2px solid var(--secondary);

    &:hover {
      transform: translateY(-5px);
    }

    .popular-badge {
      position: absolute;
      top: -12px;
      left: 50%;
      transform: translateX(-50%);
      background: var(--secondary);
      color: white;
      padding: 6px 16px;
      border-radius: 20px;
      font-size: 0.8rem;
      font-weight: 600;
      box-shadow: 0 4px 10px rgba(16, 185, 129, 0.3);
    }
  }

  &-header {
    text-align: center;
    margin-bottom: 15px;
    padding-bottom: 15px;
    border-bottom: 1px solid var(--border);

    .period {
      font-size: 1.2rem;
      font-weight: 600;
      color: var(--dark);
      margin-bottom: 8px;
    }

    .price-container {
      display: flex;
      flex-direction: column;
      align-items: center;
      margin-bottom: 8px;

      .price-old {
        font-size: 0.9rem;
        color: var(--gray);
        text-decoration: line-through;
        margin-bottom: 3px;
      }

      .price-new {
        font-size: 1.8rem;
        font-weight: 700;
        color: var(--primary);
        line-height: 1;
      }

      .price-per-month {
        font-size: 0.85rem;
        color: var(--gray);
        margin-top: 3px;
      }
    }
  }
  .features {
    list-style: none;
    margin: 15px 0;
    flex-grow: 1;
  }
}

@media (max-width: 768px) {
  .tariff {
    padding: 20px 15px;

    .period {
      font-size: 1.1rem;
    }

    .price-new {
      font-size: 1.6rem;
    }
  }
}

@media (max-width: 480px) {
  .tariff {
    padding: 18px 12px;

    .period {
      font-size: 1rem;
    }

    .price-new {
      font-size: 1.5rem;
    }
  }
}
</style>
