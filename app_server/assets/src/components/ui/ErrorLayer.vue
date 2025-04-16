<script setup lang="ts"></script>

<template>
  <div
    class="error-layer position-absolute d-flex align-items-center justify-content-center w-100 h-100"
  >
    <h2>
      <slot />
    </h2>
  </div>
</template>

<style scoped lang="scss">
$red_color: #ffd5d5;
$red_bg_1: #ffffff00;
$red_bg_2: #8d231d66;
$red_bg_3: #970404;

.error-layer {
  color: $red_color;
  background: linear-gradient(135deg, $red_bg_1, $red_bg_2, $red_bg_3, $red_bg_2, $red_bg_1);
  border-radius: 0 var(--block-border-radius);
}
</style>
