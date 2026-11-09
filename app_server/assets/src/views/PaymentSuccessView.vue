<script setup lang="ts">
import { PaymentSuccessContent, PaymentSuccessDummyContent } from '@/components/tariffs';
import { AppConfig } from '@/config/envConfig';
import { paymentAgentBySource } from '@/utils/checkoutUrl';
import NotFoundView from '@/views/NotFoundView.vue';
import { computed, onMounted, onUnmounted } from 'vue';

const props = defineProps<{
  /** Идентификатор задачи (из URL) */
  taskId: string;
  source?: string;
}>();

const sourceUnknown = computed<boolean>(
  () => Boolean(props.source) && !paymentAgentBySource(props.source),
);

onMounted(() => {
  if (sourceUnknown.value) return;
  document.body.classList.add('payment-success-scroll');
});

onUnmounted(() => {
  document.body.classList.remove('payment-success-scroll');
});
</script>

<template>
  <NotFoundView v-if="sourceUnknown" />
  <PaymentSuccessDummyContent v-else-if="AppConfig.useDummyConfig" :task-id="taskId" />
  <PaymentSuccessContent v-else :task-id="taskId" />
</template>
