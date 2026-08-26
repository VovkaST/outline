<script setup lang="ts">
const props = defineProps<{
  showIcon?: boolean;
}>();
</script>

<template>
  <div class="success-card">
    <div v-if="showIcon" class="success-icon" aria-hidden="true">
      <svg
        viewBox="0 0 24 24"
        fill="none"
        stroke-width="3"
        stroke-linecap="round"
        stroke-linejoin="round"
      >
        <polyline points="20 6 9 17 4 12" />
      </svg>
    </div>
    <h1 v-if="$slots['title']" class="success-heading"><slot name="title" /></h1>
    <p class="success-lead"><slot name="description" /></p>
  </div>
</template>

<style scoped lang="scss">
.success-card {
  background: linear-gradient(180deg, var(--success-soft) 0%, var(--bg) 100%);
  border: 1px solid color-mix(in srgb, var(--success) 30%, var(--border));
  border-radius: 18px;
  padding: 28px 22px 24px;
  margin-bottom: 28px;
  text-align: center;
  box-shadow: 0 6px 20px color-mix(in srgb, var(--success) 12%, transparent);
}

.success-icon {
  width: 64px;
  height: 64px;
  margin: 0 auto 14px;
  background: var(--success);
  border-radius: 50%;
  display: grid;
  place-items: center;
  box-shadow: 0 8px 20px rgba(19, 194, 150, 0.35);
  animation: pop 0.5s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.success-icon svg {
  width: 32px;
  height: 32px;
  stroke: #fff;
}

@keyframes pop {
  0% {
    transform: scale(0);
    opacity: 0;
  }
  100% {
    transform: scale(1);
    opacity: 1;
  }
}

.success-heading {
  font-size: 22px;
  font-weight: 600;
  line-height: 1.3;
  letter-spacing: -0.5px;
  color: color-mix(in srgb, var(--success) 55%, var(--ink));
}

.success-heading + .success-lead {
  margin-top: 6px;
}

.success-lead {
  font-size: 14px;
  line-height: 1.5;
  color: var(--ink-dim);
}

.success-lead:empty {
  display: none;
}

@media (max-width: 380px) {
  .success-card {
    padding: 24px 18px 20px;
  }

  .success-heading {
    font-size: 20px;
  }
}

@media (prefers-color-scheme: dark) {
  .success-card {
    background: linear-gradient(
      180deg,
      color-mix(in srgb, var(--success) 14%, transparent) 0%,
      rgba(30, 41, 59, 0.98) 100%
    );
    border-color: color-mix(in srgb, var(--success) 35%, transparent);
    box-shadow: 0 6px 20px color-mix(in srgb, var(--success) 18%, transparent);
  }

  .success-lead {
    color: rgba(255, 255, 255, 0.82);
  }

  .success-heading {
    color: color-mix(in srgb, var(--success) 70%, #fff);
  }
}
</style>
