<script setup lang="ts">
import { Header, TariffsList } from '@/components/tariffs';
import { usePaymentStore } from '@/stores/payment';
import { useToggle } from '@vueuse/core';
import { computed, ref } from 'vue';
import { useRoute } from 'vue-router';

const route = useRoute();
const paymentStore = usePaymentStore();

const tariffsListRef = ref<typeof TariffsList | null>(null);

const taskId = computed<string>(() => (route.query['task'] as string) || 'empty');
const returnUrl = computed<string>(() => route.query['returnUrl'] as string);

const [formSubmitting, formSubmittingToggle] = useToggle(false);

const onHeaderClick = () => {
  if (!tariffsListRef.value?.$el) return;
  tariffsListRef.value?.$el.scrollIntoView({ behavior: 'smooth' });
};

const onActionClick = (price: number) => {
  formSubmitting.value = true;
  paymentStore
    .initYooKassaPayment({
      taskId: taskId.value,
      amount: price,
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
  <div class="tariff-form-container">
    <Header @headerButtonClick="onHeaderClick" />
    <TariffsList ref="tariffsListRef" @actionClick="onActionClick" :wait="formSubmitting" />
    <footer>© 2025 — Все права защищены</footer>
  </div>
</template>
<style lang="scss" scoped>
.tariff-form-container {
  max-width: 600px;
  margin: 0 auto;
  padding: 1rem;

  footer {
    margin-top: 40px;
    color: var(--muted-color);
    font-size: 0.8rem;
    text-align: center;
  }
}
</style>
