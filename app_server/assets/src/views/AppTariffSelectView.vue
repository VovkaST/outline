<script setup lang="ts">
import { Header, TariffsList, Footer } from '@/components/tariffs';
import { usePaymentStore } from '@/stores/payment';
import { useToggle } from '@vueuse/core';
import { computed } from 'vue';
import { useRoute } from 'vue-router';

const route = useRoute();
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
      <Footer />
    </div>
  </div>
</template>
<style lang="scss" scoped>
.tariff-form-container {
  max-width: 1200px;
  width: 100%;
  margin: 0 auto;

  .card {
    background: #fff;
    border-radius: 16px;
    box-shadow: 0 12px 40px rgba(0, 0, 0, 0.22);
    overflow: visible;
    margin-bottom: 14px;
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
