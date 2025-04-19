<script setup lang="ts">
import { LayerTypes } from './types.ts';

const props = defineProps<{
  type: LayerTypes;
}>();
</script>

<template>
  <div
    class="overflow-layer position-absolute d-flex align-items-center justify-content-center w-100 h-100"
    :class="type"
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

$green_color: #c2ffca;
$green_bg_1: #ffffff00;
$green_bg_2: #398d1d66;
$green_bg_3: #049753;

.overflow-layer {
  border-radius: 0 var(--block-border-radius);

  &.error {
    color: $red_color;
    background: linear-gradient(135deg, $red_bg_1, $red_bg_2, $red_bg_3, $red_bg_2, $red_bg_1);
  }

  &.success {
    color: $green_color;
    background: linear-gradient(
      135deg,
      $green_bg_1,
      $green_bg_2,
      $green_bg_3,
      $green_bg_2,
      $green_bg_1
    );
  }
}
</style>
