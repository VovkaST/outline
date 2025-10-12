<script setup lang="ts"></script>

<template>
  <li>
    <i class="fas fa-check"></i>
    <slot />
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
</style>
