<script setup lang="ts">
import Contacts from './Contacts.component.vue';
</script>

<template>
  <footer class="d-flex flex-column align-items-center">
    <div id="cancel-subscription">
      Для отмены подписки нажмите <a href="#">сюда</a> или свяжитесь с нами по данным из раздела
      Контакты
    </div>
    <contacts class="mt-3" />
  </footer>
</template>

<style scoped lang="scss">
footer {
  margin: 0 auto;
  padding: 10px 10px 30px;
  background-color: #151721e8;
  backdrop-filter: blur(12px);
  gap: 20px;
  border-top-left-radius: 12px;
  border-top-right-radius: 12px;
}
</style>
