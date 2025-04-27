<script setup lang="ts">
import CheckBox from './CheckBox.component.vue';
import ButtonComponent from './Button.component.vue';
import { OverflowLayer } from '@/components/ui';
import { computed, inject, onMounted } from 'vue';
import type { Ref } from 'vue';
import { Errors, Messages } from '@/stores/enums.ts';
import { usePaymentStore } from '@/stores/payment.ts';
import { LayerTypes } from '@/components/ui/types.ts';
import { useToggle } from '@vueuse/core';

const taskGuid = inject<Ref<string>>('taskGuid');
const paymentError = inject<Ref<Errors>>('paymentError');
const isSuccessfullyPayedInj = inject<Ref<boolean>>('isSuccess');
const isSuccessfullyPayed = computed<boolean>(() => isSuccessfullyPayedInj.value);

const payment = usePaymentStore();

const offer = defineModel('offer', { default: false });
const personal = defineModel('personal', { default: false });
const subscription = defineModel('subscription', { default: false });

const isAgreed = computed<boolean>(() => offer.value && personal.value && subscription.value);
const allowToPay = computed<boolean>(() => isAgreed.value && !isSuccessfullyPayed.value);

const [isBusy, isBusyToggle] = useToggle();

const onPayClick = async () => {
  isBusy.value = true;
  payment
    .getPaymentURL({ guid: taskGuid.value })
    .then(
      (response) => {
        window.location.href = response.url;
      },
      () => {
        paymentError.value = Errors.UNHANDLED_ERROR;
      },
    )
    .finally(isBusyToggle);
};

onMounted(() => {
  if (isSuccessfullyPayed.value) {
    offer.value = isSuccessfullyPayed?.value;
    personal.value = isSuccessfullyPayed?.value;
    subscription.value = isSuccessfullyPayed?.value;
  }
});
</script>

<template>
  <div class="agreement position-relative">
    <overflow-layer v-if="paymentError" :type="LayerTypes.ERROR">
      {{ paymentError }}
    </overflow-layer>
    <overflow-layer v-else-if="isSuccessfullyPayed" :type="LayerTypes.SUCCESS">
      {{ Messages.PAYED_SUCCESSFULLY }}
    </overflow-layer>
    <check-box id="offer" v-model="offer">
      Согласен с <a href="/attachments/Offer.pdf" target="_blank" download>условиями оферты</a>
    </check-box>
    <check-box id="personal" v-model="personal">
      Согласен с
      <a href="/attachments/AgreementPersonalData.pdf" target="_blank" download>
        условиями обработки персональных данных
      </a>
    </check-box>
    <check-box id="subscription" v-model="subscription">
      Согласен с
      <a href="/attachments/AgreementSubscription.pdf" target="_blank" download
        >условиями подписки</a
      >
    </check-box>
    <div class="text-center">
      <button-component :disabled="!allowToPay || isBusy" :is-busy="isBusy" @click="onPayClick">
        Оплатить
      </button-component>
    </div>
  </div>
</template>

<style scoped lang="scss">
.outline-button {
  width: calc(40% - 40px);
}
</style>
