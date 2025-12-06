<script setup lang="ts">
const props = withDefaults(
  defineProps<{
    showModal: boolean;
  }>(),
  { showModal: false },
);
</script>
<template>
  <Teleport to="#app">
    <Transition name="fade" mode="out-in" appear>
      <div
        v-if="props.showModal"
        :key="props.showModal"
        :class="{ 'is-visible': props.showModal }"
        class="modal-wrapper"
        role="dialog"
        aria-hidden="false"
      >
        <slot />
      </div>
    </Transition>
  </Teleport>
</template>
<style lang="scss" scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s;
}
.fade-enter,
.fade-leave-to {
  opacity: 0;
}
</style>
