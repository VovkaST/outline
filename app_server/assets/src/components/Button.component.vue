<script setup lang="ts">
const props = withDefaults(
  defineProps<{
    isBusy?: boolean;
  }>(),
  { isBusy: false },
);
</script>

<template>
  <button class="button outline-button">
    <span
      v-if="isBusy"
      class="spinner-border spinner-border-sm"
      role="status"
      aria-hidden="true"
    ></span>
    <slot />
  </button>
</template>

<style scoped lang="scss">
.outline-button {
  background: linear-gradient(155deg, #51bf18, #2e366a, #bd6822);
  padding: 1.2rem 2rem;
  margin: 0.75rem 1.5px 0;
  color: aliceblue;
  font-size: 1.2rem;
  font-weight: 500;
  border-radius: 0.6rem;
  transition: all 250ms ease-in-out;
  cursor: pointer;
  border: 1px solid #ffffff00;

  &:active {
    border: 1px solid #ff6c6c;
  }

  &[disabled] {
    background: linear-gradient(155deg, #7a7a7a, #bdbdc1, #7a7a7a);
    color: #707070;
    cursor: not-allowed;
  }
}
</style>
