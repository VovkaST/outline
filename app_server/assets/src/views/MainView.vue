<script setup lang="ts">
import Subscribe from '@/components/Subscribe.component.vue';
import { Spinner } from '@/components/ui';
import { computed, onBeforeMount, provide, readonly, ref } from 'vue';
import { usePaymentStore } from '@/stores/payment.ts';
import { useRoute } from 'vue-router';
import { Errors } from '@/stores/enums.ts';
import { str2bool } from '@/utils.ts';

const route = useRoute();
const paymentStore = usePaymentStore();

const taskGuid = computed<string>(() => {
  return route.query['guid'];
});
const isRecurrent = computed<boolean>(() => {
  const isRecurrentValue = route.query['isRecurrent'];
  if (isRecurrentValue) return str2bool(isRecurrentValue as string);
  return false;
});
const isSuccess = computed<boolean>(() => {
  const successValue = route.query['success'];
  if (successValue) return str2bool(successValue as string);
  return false;
});
const isPaymentValid = ref<boolean>();
const paymentError = ref<Errors>();
const isReady = ref<boolean>(false);

provide(
  'paymentItem',
  readonly({
    taskGuid,
    isSuccess,
    isRecurrent,
  }),
);

provide('paymentError', { paymentError });

onBeforeMount(() => {
  if (taskGuid.value) {
    paymentStore
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
