<script setup lang="ts">
const props = defineProps<{
  price: number;
  oldPrice: number;
  perMonth?: number;
  border?: 'green';
}>();

const emit = defineEmits<{
  (e: 'actionClick', price: number): void;
}>();

const onActionClick = () => {
  emit('actionClick', props.price);
};
</script>

<template>
  <div :class="['card', border ? `border-${border}` : null]">
    <div class="badge">
      <slot name="badge"></slot>
    </div>
    <div class="term">
      <slot name="term">
        <span class="gift"></span>
      </slot>
    </div>
    <div class="price-old">{{ oldPrice }} ₽</div>
    <div class="price-now">
      {{ price }} ₽
      <span v-if="perMonth" class="per-month">({{ perMonth }} ₽/мес)</span>
    </div>
    <div class="actions d-flex flex-column">
      <a class="btn btn-primary" :data-amount="{ price }" @click.prevent="onActionClick">
        <slot name="actionText">Купить</slot>
      </a>
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
    top: 12px;
    right: 12px;
    background: var(--accent-color);
    color: #041004;
    padding: 6px 9px;
    border-radius: 9px;
    font-size: 0.8rem;
  }

  .term {
    font-size: 15px;
    color: var(--muted-color);
    margin-bottom: 8px;

    :deep(.gift) {
      display: inline-block;
      margin-left: 8px;
    }
  }

  .price-old {
    color: rgba(255, 255, 255, 0.35);
    text-decoration: line-through;
    font-weight: 600;
  }

  .price-now {
    font-size: 20px;
    font-weight: 800;
    margin-top: 6px;

    .per-month {
      font-size: 13px;
      color: var(--muted-color);
      font-weight: 600;
    }
  }

  .per-month {
    font-size: 13px;
    color: var(--muted-color);
    margin-top: 6px;
  }

  .actions {
    margin-top: 12px;
    gap: 8px;
  }
}

.actions {
  margin-top: 12px;
  gap: 8px;

  .btn {
    display: inline-block;
    padding: 10px 14px;
    border-radius: 10px;
    font-weight: 700;
    text-decoration: none;
    cursor: pointer;
    text-align: center;

    &.btn-primary {
      background: linear-gradient(90deg, var(--green-color), var(--dark-green-color));
      color: #041004;
      border: none;
    }
  }
}
</style>
