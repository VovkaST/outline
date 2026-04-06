<script setup lang="ts">
import { Modal } from '@/components';
import {
  PublicOffer,
  UserAgreement,
  ConfidentialPolicy,
} from '@/components/tariffs/legal-documents';
import { useConfig } from '@/composables/useConfig';
import { useToggle } from '@vueuse/core';

const config = useConfig();

const [isPublicOfferShow, isPublicOfferShowToggle] = useToggle(false);
const [isUserAgreementShow, isUserAgreementShowToggle] = useToggle(false);
const [isConfidentialPolicyShow, isConfidentialPolicyShowToggle] = useToggle(false);

const onPublicOfferClick = () => {
  isPublicOfferShowToggle(true);
};
const onPublicOfferClose = () => {
  isPublicOfferShowToggle(false);
};

const onUserAgreementClick = () => {
  isUserAgreementShowToggle(true);
};
const onUserAgreementClose = () => {
  isUserAgreementShowToggle(false);
};

const onConfidentialPolicyClick = () => {
  isConfidentialPolicyShowToggle(true);
};
const onConfidentialPolicyClose = () => {
  isConfidentialPolicyShowToggle(false);
};
</script>
<template>
  <div class="footer">
    <p>© {{ new Date().getFullYear() }} {{ config.site.name }} — Ваша приватность под защитой</p>
    <div class="footer-links">
      <a href="#" id="offer-link" class="text-xsmall" @click.prevent="onPublicOfferClick">
        Публичная оферта
      </a>
      <a href="#" id="agreement-link" class="text-xsmall" @click.prevent="onUserAgreementClick">
        Пользовательское соглашение
      </a>
      <a
        href="#"
        id="confidential-policy-link"
        class="text-xsmall"
        @click.prevent="onConfidentialPolicyClick"
      >
        Политика конфиденциальности
      </a>
    </div>
    <div class="req">
      <p>{{ config.organization.fullName }} · ИНН {{ config.organization.inn }}</p>
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

    <Modal
      key="userAgreement"
      title="Пользовательское соглашение"
      :show="isUserAgreementShow"
      closeOnEsc
      closeOnClickOutside
      @close="onUserAgreementClose"
    >
      <template #title>Пользовательское соглашение</template>
      <template #body> <UserAgreement /> </template>
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
      <template #body> <ConfidentialPolicy /> </template>
    </Modal>
  </div>
</template>

<style scoped lang="scss">
.footer {
  text-align: center;
  padding: 16px 12px;
  border-top: 1px solid var(--border);

  p {
    font-size: var(--xs);
    font-weight: 400;
    color: var(--t3);
    line-height: 1.7;
    margin-bottom: 2px;
  }

  .footer-links {
    margin-bottom: 8px;

    a {
      color: var(--p);
      text-decoration: none;
      font-size: var(--xs);
      font-weight: 400;
      margin: 0 4px;
    }
  }

  .req {
    margin-top: 8px;
    padding-top: 8px;
    border-top: 1px solid var(--border);

    p {
      color: var(--t3);
    }
  }
}

@media (prefers-color-scheme: dark) {
  .footer {
    border-top-color: var(--border);

    p {
      color: var(--t3);
    }

    .req {
      border-top-color: var(--border);
    }
  }
}
</style>
