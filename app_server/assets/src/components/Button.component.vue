<script setup lang="ts"></script>

<template>
  <button class="button outline-button">
    <slot />
  </button>
</template>

<style scoped lang="scss">
.outline-button {
  background: linear-gradient(155deg, #51bf18, #2e366a, #bd6822);
  padding: 1.2rem 2rem;
  margin: 0.75em 20px 0;
  color: aliceblue;
  font-size: 1.2em;
  font-weight: 500;
  border-radius: 0.6em;
  transition: all 250ms ease-in-out;
  cursor: pointer;
  border: 1px solid rgba(0, 0, 0, 0);

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
