<script setup lang="ts">
const props = withDefaults(
  defineProps<{
    bold?: boolean;
  }>(),
  { bold: false },
);
</script>

<template>
  <li class="text-small">
    <i class="fas fa-check"></i>
    <strong v-if="props.bold"><slot /></strong>
    <slot v-else />
  </li>
</template>

<style scoped lang="scss">
li {
  padding: 6px 0;
  display: flex;
  align-items: center;
  line-height: 1.3;
  font-size: 0.95rem;

  i {
    color: var(--secondary);
    margin-right: 8px;
    font-size: 0.95rem;
    min-width: 16px;
  }
}

@media (max-width: 768px) {
  li {
    font-size: 0.9rem;
  }
}
</style>
