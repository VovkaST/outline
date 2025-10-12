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
    <div class="card">
      <Header />
      <TariffsList ref="tariffsListRef" @actionClick="onActionClick" :wait="formSubmitting" />
      <footer>© 2025 — Все права защищены</footer>
    </div>
  </div>
</template>
<style lang="scss" scoped>
.tariff-form-container {
  max-width: 1200px;
  width: 100%;
  margin: 0 auto;

  .card {
    background: rgba(255, 255, 255, 0.95);
    backdrop-filter: blur(10px);
    border-radius: 20px;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
    overflow: hidden;
  }

  footer {
    text-align: center;
    padding: 20px;
    color: var(--gray);
    font-size: 0.85rem;
    border-top: 1px solid var(--border);
  }
}

@media (max-width: 768px) {
  .footer {
    padding: 15px;
  }
}
</style>
