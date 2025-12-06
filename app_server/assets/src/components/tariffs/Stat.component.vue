<script setup lang="ts">
const props = defineProps<{
  number: string;
  text: string;
}>();
</script>
<template>
  <div class="stat">
    <div class="stat-number text-large">{{ props.number }}</div>
    <div class="stat-text text-xsmall">{{ props.text }}</div>
  </div>
</template>
<style lang="scss" scoped>
.stat {
  padding: 12px 8px;
  background: white;
  border-radius: 10px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  text-align: center;

  &-number {
    font-weight: 800;
    color: var(--primary);
    margin-bottom: 2px;
    line-height: 1;
  }
}
</style>
