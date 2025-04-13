<script setup lang="ts">
import CheckBox from './CheckBox.component.vue';
import ButtonComponent from './Button.component.vue';
</script>

<template>
  <div class="agreement">
    <check-box id="offer">
      Согласен с <a href="/attachments/Оферта.pdf">условиями оферты</a>
    </check-box>
    <check-box id="personal">
      Согласен с
      <a
        href="/attachments/site1001033_Согласие%20на%20обработку%20персональных%20данных.docx"
        target="_blank"
        download
      >
        условиями обработки персональных данных
      </a>
    </check-box>
    <check-box id="subscription">
      Согласен с <a href="/attachments/Соглашение с подпиской т.pdf">условиями подписки</a>
    </check-box>
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
