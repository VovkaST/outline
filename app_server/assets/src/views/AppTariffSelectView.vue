<script setup lang="ts">
import {
  AddSubscriptionButton,
  Announcement,
  Footer,
  Header,
  SubscriptionRef,
  TariffsList,
} from '@/components/tariffs';
import { useConfig } from '@/composables/useConfig';
import { usePaymentStore } from '@/stores/payment';
import { useToggle } from '@vueuse/core';
import { computed } from 'vue';
import { useRoute } from 'vue-router';

const route = useRoute();
const config = useConfig();
const paymentStore = usePaymentStore();

const props = defineProps<{
  taskId: string;
}>();

const returnUrl = computed<string>(() => (route.query['returnUrl'] as string) || '');

const [formSubmitting, formSubmittingToggle] = useToggle(false);

const onActionClick = (price: number) => {
  formSubmitting.value = true;
  paymentStore
    .initYooKassaPayment({
      taskId: props.taskId,
      amount: price * 100,
      returnUrl: returnUrl.value,
    })
    .then(
      (response) => {
        window.location.href = response.confirmation_url;
      },
      (reason) => console.error('Init payment error: ', reason),
    )
    .finally(formSubmittingToggle);
};
</script>

<template>
  <div class="page">
    <Announcement v-if="config.announcement">
      <template #title>{{ config.announcement.title }}</template>
      <p v-for="paragraph in config.announcement.paragraphs" :key="paragraph">
        {{ paragraph }}
      </p>
      <p v-if="config.announcement.cta" class="announcement-cta">
        {{ config.announcement.cta }}
      </p>
    </Announcement>

    <Header />

    <SubscriptionRef :subscription-number="taskId" />

    <TariffsList :tariffs="config.tariffs" :wait="formSubmitting" @actionClick="onActionClick" />

    <div class="note">Перед оплатой у вас должна быть <strong>добавлена подписка</strong>.</div>

    <AddSubscriptionButton :url="config.subscriptionAddUrl ?? ''" :task-id="taskId" />

    <Footer />
  </div>
</template>

<style lang="scss" scoped>
.page {
  max-width: 420px;
  width: 100%;
  text-align: center;
  margin: 0 auto;
}

.note {
  font-size: 13px;
  color: var(--ink-dim);
  line-height: 1.5;
  padding: 12px 16px;
  background: var(--bg-soft);
  border-radius: 8px;
  text-align: center;
}

.note :deep(strong) {
  color: var(--ink);
  font-weight: 600;
}
</style>
