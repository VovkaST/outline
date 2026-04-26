<script setup lang="ts">
import { Modal } from '@/components';
import {
  ConfidentialPolicy,
  PublicOffer,
  UserAgreement,
} from '@/components/tariffs/legal-documents';
import { useToggle } from '@vueuse/core';

const [isPublicOfferShow, isPublicOfferShowToggle] = useToggle(false);
const [isUserAgreementShow, isUserAgreementShowToggle] = useToggle(false);
const [isConfidentialPolicyShow, isConfidentialPolicyShowToggle] = useToggle(false);

const onPublicOfferClick = () => isPublicOfferShowToggle(true);
const onPublicOfferClose = () => isPublicOfferShowToggle(false);

const onUserAgreementClick = () => isUserAgreementShowToggle(true);
const onUserAgreementClose = () => isUserAgreementShowToggle(false);

const onConfidentialPolicyClick = () => isConfidentialPolicyShowToggle(true);
const onConfidentialPolicyClose = () => isConfidentialPolicyShowToggle(false);
</script>

<template>
  <div class="legal-links">
    <button class="offer-link" type="button" @click="onPublicOfferClick">Публичная оферта</button>
    <span class="legal-sep">·</span>
    <button class="offer-link" type="button" @click="onUserAgreementClick">
      Пользовательское соглашение
    </button>
    <span class="legal-sep">·</span>
    <button class="offer-link" type="button" @click="onConfidentialPolicyClick">
      Политика конфиденциальности
    </button>

    <Modal
      key="publicOffer"
      title="Публичная оферта"
      :show="isPublicOfferShow"
      closeOnEsc
      closeOnClickOutside
      @close="onPublicOfferClose"
    >
      <template #title>Публичная оферта</template>
      <template #body><PublicOffer /></template>
    </Modal>

    <Modal
      key="userAgreement"
      title="Пользовательское соглашение"
      :show="isUserAgreementShow"
      closeOnEsc
      closeOnClickOutside
      @close="onUserAgreementClose"
    >
      <template #title>Пользовательское соглашение</template>
      <template #body><UserAgreement /></template>
    </Modal>

    <Modal
      key="confidentialPolicy"
      title="Политика конфиденциальности"
      :show="isConfidentialPolicyShow"
      closeOnEsc
      closeOnClickOutside
      @close="onConfidentialPolicyClose"
    >
      <template #title>Политика конфиденциальности</template>
      <template #body><ConfidentialPolicy /></template>
    </Modal>
  </div>
</template>

<style scoped lang="scss">
.legal-links {
  margin-top: 20px;
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  align-items: center;
  gap: 6px;
  line-height: 1.6;
}

.legal-sep {
  color: var(--ink-faint);
  font-size: 11px;
}

.offer-link {
  background: none;
  border: none;
  color: var(--ink-faint);
  font-family: inherit;
  font-size: 11px;
  cursor: pointer;
  text-decoration: underline;
  text-underline-offset: 2px;
  transition: color 0.15s;
  padding: 4px 2px;
}

.offer-link:hover {
  color: var(--primary);
}

@media (max-width: 380px) {
  .legal-links {
    flex-direction: column;
    gap: 2px;
  }

  .legal-sep {
    display: none;
  }
}
</style>
