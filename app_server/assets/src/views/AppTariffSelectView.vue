<script setup lang="ts">
import { Delimiter, Header, PayForm, TariffsList } from '@/components/tariffs';
import { usePaymentStore } from '@/stores/payment';
import { useToggle } from '@vueuse/core';
import { computed, ref } from 'vue';
import { useRoute } from 'vue-router';

const route = useRoute();
const paymentStore = usePaymentStore();

const tariffsListRef = ref<typeof TariffsList | null>(null);
const paymentFormRef = ref<typeof TariffsList | null>(null);
const selectedPrice = ref<number | null>(null);
const userEmail = ref<string | null>(null);

const taskId = computed<string>(() => (route.query['task'] as string) || 'empty');

const [formSubmitting, formSubmittingToggle] = useToggle(false);

const onHeaderClick = () => {
  if (!tariffsListRef.value?.$el) return;
  tariffsListRef.value?.$el.scrollIntoView({ behavior: 'smooth' });
};

const onActionClick = (price: number) => {
  if (!paymentFormRef.value?.$el) return;
  selectedPrice.value = price / 100;
  paymentFormRef.value?.$el.scrollIntoView({ behavior: 'smooth' });
};

const onFormSubmit = (payload: { amount: number; email: string }) => {
  formSubmitting.value = true;
  paymentStore
    .initYooKassaPayment({
      taskId: taskId.value,
      amount: payload.amount * 100,
      customerEmail: payload.email,
    })
    .finally(formSubmittingToggle);
};
</script>
<template>
  <div class="tariff-form-container">
    <Header @headerButtonClick="onHeaderClick" />
    <TariffsList ref="tariffsListRef" @actionClick="onActionClick" />
    <Delimiter />
    <PayForm
      ref="paymentFormRef"
      v-model:amount="selectedPrice"
      v-model:email="userEmail"
      :wait="formSubmitting"
      @submit="onFormSubmit"
    >
      <template v-slot:header>Оформление заказа</template>
      <template v-slot:description>
        Нажмите на выбранный тариф выше — сумма автоматически подставится в форму.
      </template>
      <template v-slot:footnote>
        Безопасные платежи. Никаких подписок, оплата разовая. Цены указаны с учётом акции.
      </template>
    </PayForm>
    <footer>© 2025 — Все права защищены</footer>
  </div>
</template>
<style lang="scss" scoped>
.tariff-form-container {
  max-width: 600px;
  margin: 0 auto;
  padding: 16px;

  #plans {
    gap: 16px;
    margin-top: 16px;
  }

  footer {
    margin-top: 40px;
    color: var(--muted-color);
    font-size: 13px;
    text-align: center;
  }
}
</style>
