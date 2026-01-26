<script setup lang="ts">
import { computed } from 'vue';

const props = defineProps<{
  currentStep: number;
  totalSteps?: number;
}>();

const totalSteps = computed<number>(() => props.totalSteps || 4);

const progressPercentage = computed<number>(() => {
  return ((props.currentStep - 1) / (totalSteps.value - 1)) * 100;
});

const isStepActive = (step: number): boolean => {
  return step <= props.currentStep;
};
</script>

<template>
  <div class="progress-bar">
    <div class="progress-line">
      <div class="progress-line-inner" :style="{ width: `${progressPercentage}%` }"></div>
    </div>
    <div
      v-for="step in totalSteps"
      :key="step"
      class="progress-step"
      :class="{ active: isStepActive(step) }"
    >
      {{ step }}
    </div>
  </div>
</template>

<style scoped lang="scss">
$stepSize: 40px;
$progressBarPaddingLR: 8px;
$progressBarLR: calc($stepSize / 2 + $progressBarPaddingLR);

.progress-bar {
  display: flex;
  justify-content: space-between;
  position: relative;
  margin-bottom: 32px;
  max-width: 360px;
  margin-left: auto;
  margin-right: auto;
  padding: 0 $progressBarPaddingLR;
}

.progress-line {
  position: absolute;
  top: 50%;
  left: $progressBarLR;
  right: $progressBarLR;
  height: 3px;
  background: rgba(255, 255, 255, 0.3);
  transform: translateY(-50%);
  z-index: 2;
  border-radius: 2px;
  transition: width 0.3s ease;

  .progress-line-inner {
    height: 100%;
    background: white;
  }
}

.progress-step {
  width: $stepSize;
  height: $stepSize;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.3);
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 15px;
  color: rgba(255, 255, 255, 0.9);
  z-index: 3;
  transition: all 0.2s ease;

  &.active {
    background: white;
    color: var(--primary);
    transform: scale(1.05);
    box-shadow: 0 4px 12px rgba(255, 255, 255, 0.3);
  }
}

@media (max-width: 360px) {
  .progress-step {
    width: 36px;
    height: 36px;
    font-size: 14px;
  }
}
</style>
