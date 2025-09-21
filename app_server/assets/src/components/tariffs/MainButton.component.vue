<script setup lang="ts">
import { Spinner } from '@/components/ui';
import { computed } from 'vue';

const props = withDefaults(
  defineProps<{
    disabled?: boolean;
    wait?: boolean;
  }>(),
  {
    disabled: false,
    wait: false,
  },
);

const isDisabled = computed<boolean>(() => props.disabled || props.wait);
</script>

<template>
  <div class="button-container">
    <button class="btn btn-primary" :disabled="isDisabled">
      <slot></slot>
    </button>
    <Spinner v-if="wait" class="wait-spinner" />
  </div>
</template>

<style lang="scss" scoped>
.button-container {
  position: relative;

  button {
    background: linear-gradient(90deg, var(--green-color), var(--dark-green-color));
    padding: 12px 16px;
    border-radius: 10px;
    width: 100%;
    color: #041004;
    font-size: 0.85rem;
    font-weight: 700;
    line-height: normal;
    border: none;
    cursor: pointer;
  }
  .wait-spinner {
    position: absolute;
    top: calc(50% - 1rem);
    left: calc(50% - 1rem);
  }
}
</style>
