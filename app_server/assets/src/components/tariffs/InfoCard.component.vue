<script setup lang="ts">
withDefaults(defineProps<{ gold?: boolean }>(), { gold: false });
</script>

<template>
  <div class="info-card" :class="{ 'info-card--gold': gold }">
    <div class="info-card__icon" aria-hidden="true">
      <slot name="icon" />
    </div>
    <div class="info-card__text">
      <slot />
    </div>
  </div>
</template>

<style lang="scss" scoped>
.info-card {
  display: flex;
  align-items: center;
  gap: 12px;
  min-height: 76px;
  padding: 14px 16px;
  background: var(--bg-soft);
  border: 1px solid var(--border);
  border-radius: 12px;
  text-align: left;
}

.info-card--gold {
  background: linear-gradient(170deg, #fff9eb 0%, #ffffff 100%);
  border: 1px solid #dcc090;
  box-shadow: 0 2px 8px rgba(201, 169, 97, 0.12);
}

.info-card__icon {
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 24px;
  height: 24px;
  color: var(--primary);
}

.info-card__icon :deep(svg) {
  width: 22px;
  height: 22px;
}

.info-card__text {
  font-size: var(--sm);
  color: var(--ink-dim);
  line-height: 1.5;
}

.info-card__text :deep(strong) {
  color: var(--ink);
  font-weight: 600;
}

.info-card__text :deep(.phone) {
  color: var(--ink);
  font-weight: 600;
  font-feature-settings: 'tnum';
}
</style>
