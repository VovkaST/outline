<script setup lang="ts">
import { computed } from 'vue';

const props = withDefaults(
  defineProps<{
    disabled?: boolean;
    wait?: boolean;
    color?: 'default' | 'green';
  }>(),
  {
    disabled: false,
    wait: false,
    color: 'default',
  },
);

const isDisabled = computed<boolean>(() => props.disabled || props.wait);
</script>

<template>
  <div class="button-container">
    <button class="btn btn-primary text-medium" :class="`${color}`" :disabled="isDisabled">
      <slot></slot>
    </button>
  </div>
</template>

<style lang="scss" scoped>
.button-container {
  position: relative;

  button {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 100%;
    min-height: 48px;
    background: var(--p);
    color: #fff;
    border: none;
    border-radius: 12px;
    font-size: var(--md);
    font-weight: 600;
    cursor: pointer;
    text-decoration: none;
    transition: opacity 0.15s;

    &:active {
      opacity: 0.82;
    }

    &[disabled] {
      opacity: 0.5;
      cursor: not-allowed;
    }

    &.green {
      background: #10b981;
    }
  }

  .wait-spinner {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
  }
}

@media (max-width: 768px) {
  button {
    padding: 12px;
    font-size: 0.95rem;
  }
}
</style>
