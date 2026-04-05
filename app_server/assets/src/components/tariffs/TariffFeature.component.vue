<script setup lang="ts">
const props = withDefaults(
  defineProps<{
    bold?: boolean;
  }>(),
  { bold: false },
);
</script>

<template>
  <li :class="{ bold: props.bold }">
    <span>
      <strong v-if="props.bold"><slot /></strong>
      <slot v-else />
    </span>
  </li>
</template>

<style scoped lang="scss">
li {
  display: flex;
  align-items: flex-start;
  gap: 8px;
  font-size: var(--md);
  font-weight: 400;
  color: var(--t2);
  padding: 4px 0;
  line-height: 1.5;

  &::before {
    content: '';
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: var(--g);
    flex-shrink: 0;
    margin-top: 7px;
  }

  &.bold span strong {
    color: var(--t1);
    font-weight: 600;
  }
}
</style>
