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
  <div class="tariff" :class="{ pop: props.isPopular }">
    <div v-if="props.isPopular" class="pop-badge">⭐ ВЫГОДНЕЕ ВСЕХ</div>
    <div v-if="props.discount" class="disc-badge">{{ props.discount }}</div>

    <div class="t-period" :class="{ 't-period--pop': props.isPopular }">
      <slot name="term" />
    </div>

    <div class="t-old" v-if="props.oldPrice">{{ _oldPrice }} ₽</div>
    <div class="t-price">{{ _price }} ₽</div>

    <div v-if="props.economy" class="t-save">Экономия {{ props.economy }} ₽</div>

    <div class="t-per">{{ _perMonth }} ₽/месяц</div>

    <div class="t-divider"></div>

    <ul class="feats">
      <slot name="features" />
    </ul>

    <MainButton
      @click="onActionClick"
      :wait="wait"
      :color="isPopular ? 'green' : 'default'"
      class="btn"
    >
      <slot name="buttonText"> Выбрать тариф </slot>
    </MainButton>

    <div v-if="$slots.guarantee" class="t-label">
      <slot name="guarantee" />
    </div>
  </div>
</template>

<style scoped lang="scss">
.tariff {
  background: #fff;
  border-radius: 14px;
  border: 1.5px solid var(--border);
  padding: 16px;
  display: flex;
  flex-direction: column;
  position: relative;
  overflow: visible;
  transition: transform 0.15s;
  text-align: center;

  &:active {
    transform: scale(0.985);
  }

  &.pop {
    border-color: var(--g);
    border-width: 2px;
    margin-top: 8px;
  }

  .pop-badge {
    position: absolute;
    top: -11px;
    left: 50%;
    transform: translateX(-50%);
    background: var(--g);
    color: #fff;
    font-size: var(--xs);
    font-weight: 600;
    letter-spacing: 0.2px;
    padding: 3px 14px;
    border-radius: 20px;
    white-space: nowrap;
    z-index: 10;
    max-width: calc(100% - 20px);
  }

  .disc-badge {
    position: absolute;
    top: 10px;
    right: 10px;
    background: var(--r);
    color: #fff;
    font-size: var(--xs);
    font-weight: 600;
    padding: 2px 7px;
    border-radius: 7px;
  }

  .t-period {
    font-size: var(--sm);
    font-weight: 600;
    color: var(--t2);
    margin-bottom: 6px;
    padding-top: 4px;

    &--pop {
      padding-top: 12px;
    }
  }

  .t-old {
    font-size: var(--sm);
    font-weight: 400;
    color: var(--t3);
    text-decoration: line-through;
    margin-bottom: 2px;
  }

  .t-price {
    font-size: var(--xl);
    font-weight: 700;
    color: var(--p);
    letter-spacing: -1.5px;
    line-height: 1;
    margin-bottom: 4px;
  }

  .t-save {
    font-size: var(--xs);
    font-weight: 600;
    color: var(--r);
    background: #fef2f2;
    padding: 2px 7px;
    border-radius: 5px;
    display: inline-block;
    margin: 0 auto 4px;
  }

  .t-per {
    font-size: var(--sm);
    font-weight: 400;
    color: var(--t3);
    margin-bottom: 14px;
  }

  .feats {
    list-style: none;
    flex: 1;
    margin-bottom: 14px;
    padding: 0;
    text-align: left;
  }

  .t-divider {
    height: 1px;
    background: var(--border);
    margin-bottom: 12px;
  }

  .t-label {
    text-align: center;
    font-size: var(--xs);
    font-weight: 400;
    color: var(--t3);
    margin-top: 8px;
  }
}

@media (max-width: 360px) {
  .t-price {
    font-size: 30px;
  }
}

@media (prefers-color-scheme: dark) {
  .tariff {
    background: var(--bg-slate);
    border-color: var(--border);

    &.pop {
      border-color: var(--g);
    }

    .t-period {
      color: var(--t2);
    }

    .t-old,
    .t-per {
      color: var(--t3);
    }

    .t-price {
      color: var(--p);
    }

    .t-save {
      background: rgba(239, 68, 68, 0.2);
    }

    .t-divider {
      background: var(--border);
    }

    .t-label {
      color: var(--t3);
    }
  }
}
</style>
