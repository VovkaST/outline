<script setup lang="ts">
const props = defineProps<{
  id: string;
}>();
</script>

<template>
  <div class="form-check">
    <input type="checkbox" :id="id" class="form-check-input" />
    <label :for="id" class="form-check-label">
      <slot />
    </label>
  </div>
</template>

<style scoped lang="scss"></style>
