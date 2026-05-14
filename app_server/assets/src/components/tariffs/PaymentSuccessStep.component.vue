<script setup lang="ts">
defineProps<{
  stepNumber: number;
}>();
</script>

<template>
  <div class="payment-success-step">
    <div class="step-num" aria-hidden="true">{{ stepNumber }}</div>
    <div class="step-body">
      <div class="step-title">
        <slot name="title" />
      </div>
      <div class="step-desc">
        <slot name="description" />
      </div>
      <div v-if="$slots.below" class="step-below">
        <slot name="below" />
      </div>
    </div>
  </div>
</template>

<style scoped lang="scss">
.payment-success-step {
  display: flex;
  gap: 14px;
  background: var(--bg-soft);
  border: 1px solid var(--border);
  border-radius: 14px;
  padding: 16px 18px;
  text-align: left;
  transition:
    border-color 0.2s,
    transform 0.2s;
}

.payment-success-step:hover {
  border-color: var(--primary);
  transform: translateY(-1px);
}

.step-num {
  flex-shrink: 0;
  width: 32px;
  height: 32px;
  background: var(--primary);
  color: #fff;
  border-radius: 50%;
  display: grid;
  place-items: center;
  font-weight: 800;
  font-size: 15px;
  box-shadow: 0 4px 10px rgba(201, 169, 97, 0.35);
}

.step-body {
  flex: 1;
  min-width: 0;
}

.step-title {
  font-size: 15px;
  font-weight: 700;
  color: var(--ink);
  margin-bottom: 4px;
  letter-spacing: -0.2px;
  display: flex;
  align-items: center;
  gap: 6px;
  flex-wrap: wrap;
}

.step-desc {
  font-size: 13.5px;
  line-height: 1.5;
  color: var(--ink-dim);
}

.step-below {
  margin-top: 12px;
}

@media (max-width: 380px) {
  .payment-success-step {
    padding: 14px 14px;
    gap: 12px;
  }

  .step-num {
    width: 28px;
    height: 28px;
    font-size: 14px;
  }

  .step-title {
    font-size: 14px;
  }

  .step-desc {
    font-size: 13px;
  }
}

@media (prefers-color-scheme: dark) {
  .payment-success-step {
    background: rgba(30, 41, 59, 0.95);
    border-color: rgba(148, 163, 184, 0.25);
  }

  .step-desc {
    color: rgba(255, 255, 255, 0.85);
  }

  .step-title {
    color: #fff;
  }
}
</style>
