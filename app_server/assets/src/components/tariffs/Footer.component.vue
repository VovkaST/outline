<script setup lang="ts">
import { Modal } from '@/components';
import { PublicOffer } from '@/components/tariffs';
import { useConfig } from '@/composables/useConfig';
import { useToggle } from '@vueuse/core';

const config = useConfig();

const [isPublicOfferShow, isPublicOfferShowToggle] = useToggle(false);

const onPublicOfferClick = () => {
  isPublicOfferShowToggle(true);
};
const onPublicOfferClose = () => {
  isPublicOfferShowToggle(false);
};
</script>
<template>
  <div class="footer">
    <p class="text-xsmall">
      © {{ new Date().getFullYear() }} {{ config.site.name }}
      {{ config.site.copyrightSuffix ? ` — ${config.site.copyrightSuffix}` : '' }}
    </p>
    <div class="footer-links">
      <a href="#" id="offer-link" class="text-xsmall" @click.prevent="onPublicOfferClick">
        Публичная оферта
      </a>
    </div>
    <div class="requisites text-xsmall">
      <p>{{ config.organisation.fullName }}</p>
      <p>ИНН: {{ config.organisation.inn }}</p>
      <p>Расчётный счёт: {{ config.organisation.bankAccount }}</p>
    </div>
    <Modal
      key="publicOffer"
      title="Публичная оферта"
      :show="isPublicOfferShow"
      closeOnEsc
      closeOnClickOutside
      @close="onPublicOfferClose"
    >
      <template #title>Публичная оферта</template>
      <template #body> <PublicOffer /> </template>
    </Modal>
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
