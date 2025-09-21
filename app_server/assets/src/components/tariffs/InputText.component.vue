<script setup lang="ts">
withDefaults(
  defineProps<{
    type: 'text' | 'email';
    placeholder?: string;
    name?: string;
    disabled: boolean;
    errors: string[];
  }>(),
  {
    type: 'text',
    disabled: false,
    errors: () => [],
  },
);
const modelValue = defineModel();
</script>
<template>
  <div class="input-container d-flex flex-column">
    <input
      :name="name"
      :type="type"
      :disabled="disabled"
      :placeholder="placeholder"
      v-model="modelValue"
    />
    <ul v-if="errors.length" class="errors-list mt-2 mb-3">
      <li v-for="error in errors" v-html="error" class="error-item"></li>
    </ul>
  </div>
</template>
<style lang="scss" scoped>
input {
  padding: 10px;
  border-radius: 8px;
  border: 1px solid rgba(255, 255, 255, 0.06);
  background: transparent;
  font-size: 0.8rem;
  color: #fff;
}
.errors-list {
  list-style: none;
  padding-left: 1rem;
  color: var(--error-color);
  font-size: 0.8rem;
}
</style>
