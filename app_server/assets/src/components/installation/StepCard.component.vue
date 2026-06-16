<script setup lang="ts">
export type StepCardState = 'active' | 'done' | 'locked';

const props = defineProps<{
  stepNumber: number;
  label: string;
  title: string;
  desc: string;
  state: StepCardState;
  disabled?: boolean;
}>();

const emit = defineEmits<{
  (e: 'click'): void;
}>();

const onClick = () => {
  if (props.disabled) return;
  emit('click');
};
</script>

<template>
  <button
    class="step"
    :class="`step--${state}`"
    type="button"
    :disabled="!!disabled"
    :aria-disabled="disabled ? 'true' : 'false'"
    @click="onClick"
  >
    <div class="step-num">
      <span class="step-num-text">{{ stepNumber }}</span>
      <svg
        class="step-num-check"
        viewBox="0 0 24 24"
        fill="none"
        stroke="currentColor"
        stroke-width="3"
        stroke-linecap="round"
        stroke-linejoin="round"
        aria-hidden="true"
      >
        <polyline points="20 6 9 17 4 12" />
      </svg>
    </div>

    <div class="step-body">
      <div class="step-label">{{ label }}</div>
      <div class="step-title">{{ title }}</div>
      <div class="step-desc">
        {{ desc }}
        <slot name="descSuffix" />
      </div>
    </div>

    <div class="step-arrow" aria-hidden="true">
      <svg
        viewBox="0 0 24 24"
        fill="none"
        stroke="currentColor"
        stroke-width="2.2"
        stroke-linecap="round"
        stroke-linejoin="round"
      >
        <polyline points="9 18 15 12 9 6" />
      </svg>
    </div>
  </button>
</template>
