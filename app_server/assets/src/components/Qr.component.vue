<script setup lang="ts">
defineProps<{
  qr: string;
  url: string;
}>();
</script>

<template>
  <div class="qr-container">
    <h2>Сканируй для оплаты</h2>
    <div v-html="qr" class="qr"></div>
    <a :href="url" target="_blank">Открыть в приложении банка</a>
  </div>
</template>

<style scoped lang="scss">
.qr-container {
  background-color: #d0c2a0;
  width: 230px;
  border-radius: 20px;
  padding: 15px;
  color: #261623;
  margin: 10px auto;
  overflow: hidden;

  h2 {
    margin-bottom: 0;
    font-weight: 800;
    line-height: 1.8rem;
  }

  a {
    display: block;
    font-size: 0.9rem;
    font-weight: 600;
    line-height: 0.9rem;
    color: #534681;
  }

  .qr {
    background: white;
    width: 185px;
    margin: 10px auto;
    padding: 5px;
    border-radius: 10px;
  }
}
</style>
