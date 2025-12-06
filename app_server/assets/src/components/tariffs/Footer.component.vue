<script setup lang="ts">
const orgName = 'АЛИМУРЗАЕВ ГАДЖИ АЛИЕВИЧ';
const inn = '056003385136';
const bankAccount = '40802810700810195110';
</script>
<template>
  <div class="footer">
    <p class="text-xsmall">© 2024 Halal VPN — Ваша приватность под защитой</p>
    <div class="footer-links">
      <a href="https://site.whitemight.ru/#" id="offer-link" class="text-xsmall"
        >Публичная оферта</a
      >
    </div>
    <div class="requisites text-xsmall">
      <p>ИП {{ orgName }}</p>
      <p>ИНН: {{ inn }}</p>
      <p>Расчётный счёт: {{ bankAccount }}</p>
    </div>
  </div>
</template>
<style scoped lang="scss">
.footer {
  text-align: center;
  padding: 15px 12px;
  color: #6b7280;
  border-top: 1px solid #e5e7eb;

  &-links {
    margin-top: 6px;
    margin-bottom: 8px;

    a {
      color: var(--primary);
      text-decoration: none;
      margin: 0 6px;
    }
  }

  .requisites {
    line-height: 1.3;
    margin-top: 8px;
    padding: 0 5px;

    p {
      margin-bottom: 2px;
    }
  }
}
</style>
