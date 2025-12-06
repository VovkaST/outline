<script setup lang="ts">
import { Stat } from '@/components/tariffs';
</script>
<template>
  <div class="stats">
    <Stat number="10K+" text="Довольных клиентов" />
    <Stat number="24/7" text="Поддержка" />
  </div>
</template>
<style lang="scss" scoped>
.stats {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 8px;
  margin-top: 15px;
}
</style>
