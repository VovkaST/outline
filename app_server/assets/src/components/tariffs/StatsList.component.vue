<script setup lang="ts">
import { Stat } from '@/components/tariffs';
const supportMode = 'с 10<sup>00</sup> до 22<sup>00</sup> МСК';
</script>
<template>
  <div class="stats">
    <Stat number="10K+" text="Довольных клиентов" />
    <Stat :number="supportMode" text="Поддержка" />
  </div>
</template>
<style lang="scss" scoped>
.stats {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 8px;
  margin-top: 15px;

  :deep(sup) {
    font-size: 0.8rem;
  }
}
</style>
