<script setup lang="ts">
const props = defineProps<{
  stepNumber: number;
  title: string;
  instruction?: string;
}>();

const stepId = `step${props.stepNumber}Title`;
</script>

<template>
  <div class="step" role="region" :aria-labelledby="stepId">
    <div class="step-header">
      <div class="step-number" aria-hidden="true">{{ stepNumber }}</div>
      <h2 class="step-title" :id="stepId">{{ title }}</h2>
    </div>

    <p v-if="instruction" class="instruction-text">{{ instruction }}</p>

    <slot />
  </div>
</template>

<style scoped lang="scss">
.step {
  background: var(--card-bg, rgba(255, 255, 255, 0.98));
  border-radius: 16px;
  padding: 24px;
  margin-bottom: 20px;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
  display: block;
  -webkit-user-select: none;
  user-select: none;
  animation: fadeIn 0.3s ease;
}

.step-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 20px;
}

.step-number {
  width: 36px;
  height: 36px;
  background: linear-gradient(135deg, var(--primary), var(--primary-dark));
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 16px;
  color: white;
  flex-shrink: 0;
}

.step-title {
  font-size: 20px;
  font-weight: 700;
  color: var(--dark);
  line-height: 1.3;
}

.instruction-text {
  color: var(--gray);
  font-size: 14px;
  line-height: 1.5;
  margin-bottom: 18px;
  -webkit-user-select: text;
  user-select: text;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@media (max-width: 360px) {
  .step {
    padding: 20px;
  }

  .step-title {
    font-size: 18px;
  }
}

@media (min-height: 900px) {
  .step {
    padding: 28px;
  }
}

@media (prefers-color-scheme: dark) {
  .step {
    background: rgba(30, 41, 59, 0.98);
  }

  .instruction-text {
    color: rgba(255, 255, 255, 0.9);
  }
}
</style>
