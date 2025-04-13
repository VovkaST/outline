<script setup lang="ts"></script>

<template>
  <div class="contacts">
    <h2 class="mb-3">Контакты</h2>
    <div class="d-flex">
      <a href="tel:+79654910011">+7 (965) 491-00-11</a>
      <a href="mailto:mukhammad_368300@mail.ru">mukhammad_368300@mail.ru</a>
    </div>
  </div>
</template>

<style scoped lang="scss">
.contacts {
  h2 {
    font-size: 3.2rem;
    line-height: 1.1;
    text-align: center;
  }

  div {
    column-gap: 20px;

    a {
      color: #808080ff;
      font-size: 18px;
    }
  }
}
</style>
