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
    <button class="btn btn-primary" :class="`${color}`" :disabled="isDisabled">
      <slot></slot>
    </button>
  </div>
</template>

<style lang="scss" scoped>
.button-container {
  position: relative;

  button {
    display: block;
    width: 100%;
    padding: 16px;
    background: linear-gradient(135deg, var(--primary), var(--primary-dark));
    color: white;
    text-decoration: none;
    border-radius: 10px;
    text-align: center;
    font-weight: 600;
    font-size: 1rem;
    border: none;
    cursor: pointer;
    transition: all 0.3s ease;
    box-shadow: 0 4px 15px rgba(99, 102, 241, 0.3);
    margin-top: auto;

    &:hover {
      background: linear-gradient(135deg, var(--primary-dark), var(--primary));
      transform: translateY(-2px);
      box-shadow: 0 6px 20px rgba(99, 102, 241, 0.4);
    }

    &[disabled] {
      color: lightgray;
    }

    &.green {
      background: linear-gradient(135deg, var(--secondary), #0da271);
      box-shadow: 0 4px 15px rgba(16, 185, 129, 0.3);

      &:hover {
        background: linear-gradient(135deg, #0da271, var(--secondary));
      }
    }
  }
  .wait-spinner {
    position: absolute;
    top: calc(50% - 1rem);
    left: calc(50% - 1rem);
  }
}

@media (max-width: 768px) {
  button {
    padding: 12px;
    font-size: 0.95rem;
  }
}
</style>
