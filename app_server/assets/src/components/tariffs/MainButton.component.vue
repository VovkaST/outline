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
    display: block;
    width: 100%;
    padding: 12px;
    background: linear-gradient(135deg, var(--primary), #7c3aed);
    color: white;
    text-decoration: none;
    border-radius: 10px;
    text-align: center;
    font-weight: 700;
    border: none;
    cursor: pointer;
    transition: all 0.3s ease;
    box-shadow: 0 4px 12px rgba(139, 92, 246, 0.3);
    margin-top: auto;
    min-height: 44px;
    display: flex;
    align-items: center;
    justify-content: center;

    &:hover {
      background: linear-gradient(135deg, var(--primary-dark), var(--primary));
      transform: scale(0.96);
      transform: translateY(-2px);
      box-shadow: 0 2px 8px rgba(139, 92, 246, 0.4);
    }

    :active {
      transform: scale(0.96);
      box-shadow: 0 2px 8px rgba(139, 92, 246, 0.4);
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
