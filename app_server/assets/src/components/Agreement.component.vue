<script setup lang="ts">
import CheckBox from './CheckBox.component.vue';
import ButtonComponent from './Button.component.vue';
</script>

<template>
  <div class="agreement">
    <check-box id="offer"> Согласен с условиями оферты </check-box>
    <check-box id="personal"> Согласен с обработкой персональных данных </check-box>
    <check-box id="subscription"> Согласен с подпиской </check-box>
    <div class="text-center">
      <button-component>Оплатить по карте</button-component>
      <button-component>Оплатить по QR</button-component>
    </div>
  </div>
</template>

<style scoped lang="scss">
.outline-button {
  width: calc(40% - 40px);
}
</style>
