<script setup lang="ts">
import { computed } from 'vue';

const props = defineProps<{
  subscriptionNumber: string;
}>();

const UUID_REGEX = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i;

const isUuid = computed(() => UUID_REGEX.test(props.subscriptionNumber));
</script>

<template>
  <div class="sub-ref" :class="{ 'sub-ref--stacked': isUuid }">
    <div class="sub-ref-label">Оплата подписки</div>
    <div class="sub-ref-number">№ {{ subscriptionNumber }}</div>
  </div>
</template>

<style lang="scss" scoped>
.sub-ref {
  background: var(--bg-soft);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 14px 18px;
  margin-bottom: 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 12px;
}

.sub-ref-label {
  font-size: 13px;
  color: var(--ink-dim);
  font-weight: 500;
}

.sub-ref--stacked {
  flex-direction: column;
  align-items: flex-start;
  justify-content: flex-start;
}

.sub-ref-number {
  font-size: 15px;
  font-weight: 700;
  color: var(--primary);
  font-feature-settings: 'tnum';
  letter-spacing: 0.3px;
}

.sub-ref--stacked .sub-ref-number {
  word-break: break-all;
}
</style>
