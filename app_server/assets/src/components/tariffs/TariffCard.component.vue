<script setup lang="ts">
import { MainButton } from '@/components/tariffs';
import { decimalNumberFormat } from '@/utils';
import { computed } from 'vue';

const props = withDefaults(
  defineProps<{
    price: number;
    discount?: string;
    oldPrice: number;
    perMonth?: number;
    economy?: number;
    wait?: boolean;
    isPopular?: boolean;
    guaranteeIcon?: 'shield-alt' | 'crown' | 'gem' | 'star';
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
  <div class="tariff" :class="{ popular: props.isPopular }">
    <div v-if="props.isPopular" class="popular-badge text-xsmall">🔥 ВЫГОДНЕЕ ВСЕХ</div>
    <div v-if="props.discount" class="discount-badge text-xsmall">{{ props.discount }}</div>
    <div class="tariff-header">
      <div class="period">
        <slot name="term" />
      </div>
      <div class="price-container">
        <div class="price-old text-small">{{ _oldPrice }} ₽</div>
        <div class="price-new">{{ _price }} ₽</div>
        <div v-if="props.economy" class="economy text-xsmall">Экономия {{ props.economy }} ₽</div>
        <div class="price-per-month text-small">({{ _perMonth }} ₽/мес)</div>
      </div>
    </div>
    <ul class="features">
      <slot name="features" />
    </ul>
    <MainButton @click="onActionClick" :wait="wait" :color="isPopular ? 'green' : 'default'">
      <slot name="buttonText"> Оплатить сейчас </slot>
    </MainButton>
    <div v-if="$slots.guarantee" class="guarantee text-xsmall">
      <i class="fas" :class="`fa-${props.guaranteeIcon}`"></i>
      <span><slot name="guarantee" /></span>
    </div>
  </div>
</template>

<style scoped lang="scss">
.tariff {
  background: white;
  border-radius: 14px;
  padding: 16px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
  transition: all 0.3s ease;
  border: 2px solid #e5e7eb;
  position: relative;
  display: flex;
  flex-direction: column;

  &:active {
    transform: scale(0.98);
  }

  &.popular {
    border: 2px solid var(--secondary);
    background: var(--light);

    .popular-badge {
      position: absolute;
      top: -10px;
      left: 50%;
      transform: translateX(-50%);
      background: var(--secondary);
      color: white;
      padding: 5px 12px;
      border-radius: 15px;
      font-weight: 700;
      box-shadow: 0 3px 10px rgba(16, 185, 129, 0.3);
      white-space: nowrap;
      max-width: 90%;
    }
  }

  &-header {
    text-align: center;
    margin-bottom: 12px;
    padding-bottom: 12px;
    border-bottom: 1px solid #e5e7eb;
    position: relative;
    min-height: 80px;
    display: flex;
    flex-direction: column;
    justify-content: center;

    .price-container {
      display: flex;
      flex-direction: column;
      align-items: center;
      margin-bottom: 6px;

      .price-old {
        color: #6b7280;
        text-decoration: line-through;
        margin-bottom: 2px;
      }

      .price-new {
        font-size: 1.5rem;
        font-weight: 800;
        color: var(--primary);
        line-height: 1;
      }

      .economy {
        color: #dc2626;
        font-weight: 700;
        margin-top: 2px;
        background: #fef2f2;
        padding: 2px 6px;
        border-radius: 6px;
      }

      .price-per-month {
        color: #6b7280;
        margin-top: 2px;
      }
    }
  }

  .discount-badge {
    position: absolute;
    top: 12px;
    right: 12px;
    background: #dc2626;
    color: white;
    padding: 3px 8px;
    border-radius: 10px;
    font-weight: 700;
  }

  .features {
    list-style: none;
    margin: 15px 0;
    flex-grow: 1;
  }

  .guarantee {
    text-align: center;
    padding: 8px;
    background: #f0fdf4;
    border-radius: 6px;
    margin-top: 10px;
    border: 1px solid #bbf7d0;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 4px;

    i {
      color: var(--secondary);
    }
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
