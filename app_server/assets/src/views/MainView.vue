<script setup lang="ts">
import Subscribe from '@/components/Subscribe.component.vue';
import { Spinner } from '@/components/ui';
import { computed, onBeforeMount, provide, readonly, ref } from 'vue';
import { usePaymentStore } from '@/stores/payment.ts';
import { useRoute } from 'vue-router';
import { Errors } from '@/stores/enums.ts';

const route = useRoute();
const payment = usePaymentStore();

const paymentGuid = computed<string>(() => {
  return route.query['guid'];
});
const isPaymentValid = ref<boolean>();
const paymentError = ref<Errors>();
const isReady = ref<boolean>(false);

provide('paymentError', readonly(paymentError));

onBeforeMount(() => {
  payment.checkOrder({ guid: paymentGuid.value }).then((response) => {
    isPaymentValid.value = response.is_valid;
    if (!isPaymentValid.value) paymentError.value = Errors.PAYMENT_NOT_FOUND;
    isReady.value = true;
  });
});
</script>

<template>
  <div v-if="!isReady" class="d-flex justify-content-center">
    <spinner />
  </div>
  <subscribe v-else />
</template>

<style scoped lang="scss"></style>
