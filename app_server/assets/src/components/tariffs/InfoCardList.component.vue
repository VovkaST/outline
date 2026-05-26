<template>
  <section class="info-list">
    <slot />
  </section>
</template>

<style lang="scss" scoped>
.info-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-bottom: 16px;
}
</style>
