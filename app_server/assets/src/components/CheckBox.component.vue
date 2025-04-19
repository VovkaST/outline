<script setup lang="ts">
const props = defineProps<{
  id: string;
}>();

const model = defineModel<boolean>({ default: false });
</script>

<template>
  <div class="form-check">
    <input type="checkbox" :id="id" class="form-check-input" v-model="model" />
    <label :for="id" class="form-check-label">
      <slot />
    </label>
  </div>
</template>

<style scoped lang="scss"></style>
