<script setup lang="ts">
defineProps<{
  qr: string;
}>();
</script>

<template>
  <div class="qr-container">
    <h2>Сканируй и плати</h2>
    <span>В приложении своего банка</span>
    <div v-html="qr" class="qr"></div>
  </div>
</template>

<style scoped lang="scss">
.qr-container {
  background-color: #d0c2a0;
  width: 230px;
  border-radius: 20px;
  padding: 15px;
  color: #261623;
  margin: 10px auto 0;

  h2 {
    margin-bottom: 0;
    font-weight: 800;
    line-height: 1.8rem;
  }

  span {
    font-size: 0.9rem;
  }

  .qr {
    background: white;
    width: 185px;
    margin: 10px auto 0;
    padding: 5px;
    border-radius: 10px;
  }
}
</style>
