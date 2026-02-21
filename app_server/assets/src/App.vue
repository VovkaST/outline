<script setup lang="ts">
import { useConfig } from '@/composables/useConfig';
import { watchEffect } from 'vue';
import { RouterView } from 'vue-router';

const config = useConfig();
watchEffect(() => {
  if (config.value?.site?.name) {
    document.title = config.value.site.title;
  }
});
</script>

<template>
  <RouterView />
</template>

<style scoped>
.logo {
  height: 6em;
  padding: 1.5em;
  will-change: filter;
  transition: filter 300ms;
}
.logo:hover {
  filter: drop-shadow(0 0 2em #646cffaa);
}
.logo.vue:hover {
  filter: drop-shadow(0 0 2em #42b883aa);
}
</style>
