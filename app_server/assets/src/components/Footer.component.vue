<script setup lang="ts">
import Contacts from './Contacts.component.vue';
import { inject } from 'vue';
import { usePaymentStore } from '@/stores/payment.ts';

const { taskGuid }: { taskGuid: string } = inject('paymentItem');

const payment = usePaymentStore();

const onRejectClick = async () => {
  await payment.subscriptionReject({ guid: taskGuid }).then(() => {
    alert('Подписка отменена успешно');
  });
};
</script>

<template>
  <footer class="d-flex flex-column align-items-center">
    <div id="cancel-subscription">
      Для отмены подписки нажмите <a href="#" @click.prevent="onRejectClick">сюда</a> или свяжитесь
      с&nbsp;нами по&nbsp;данным из&nbsp;раздела Контакты
    </div>
    <contacts class="mt-3" />
  </footer>
</template>

<style scoped lang="scss">
footer {
  margin: 0 auto;
  padding: 10px 10px 30px;
  background-color: #151721e8;
  backdrop-filter: blur(12px);
  gap: 20px;
  border-top-left-radius: 12px;
  border-top-right-radius: 12px;
}
</style>
