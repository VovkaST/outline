<script setup lang="ts">
import Subscribe from '@/components/Subscribe.component.vue';
import { Spinner } from '@/components/ui';
import { computed, onBeforeMount, provide, readonly, ref } from 'vue';
import { usePaymentStore } from '@/stores/payment.ts';
import { useRoute } from 'vue-router';
import { Errors } from '@/stores/enums.ts';

const route = useRoute();
const payment = usePaymentStore();

const taskGuid = computed<string>(() => {
  return route.query['guid'];
});
const isSuccess = computed<boolean>(() => {
  return route.query['success'];
});
const isPaymentValid = ref<boolean>();
const paymentError = ref<Errors>();
const isReady = ref<boolean>(false);

provide<string>('taskGuid', readonly(taskGuid));
provide<Errors>('paymentError', readonly(paymentError));
provide<boolean>('isSuccess', readonly(isSuccess));

onBeforeMount(() => {
  if (taskGuid.value) {
    payment
      .checkOrder({ guid: taskGuid.value })
      .then(
        (response) => {
          isPaymentValid.value = response.is_valid;
          if (!isPaymentValid.value) paymentError.value = Errors.PAYMENT_NOT_FOUND;
        },
        () => {
          paymentError.value = Errors.UNHANDLED_ERROR;
        },
      )
      .finally(() => (isReady.value = true));
  } else {
    paymentError.value = Errors.PAYMENT_GUID_REQUIRED;
    isReady.value = true;
  }
});
</script>

<template>
  <div v-if="!isReady" class="d-flex justify-content-center">
    <spinner />
  </div>
  <subscribe v-else />
</template>

<style scoped lang="scss"></style>
