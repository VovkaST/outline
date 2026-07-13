<script setup lang="ts">
import { PaymentSuccessContent, PaymentSuccessDummyContent } from '@/components/tariffs';
import { AppConfig } from '@/config/envConfig';
import { onMounted, onUnmounted } from 'vue';

defineProps<{
  /** Идентификатор задачи (из URL) */
  taskId: string;
}>();

onMounted(() => {
  document.body.classList.add('payment-success-scroll');
});

onUnmounted(() => {
  document.body.classList.remove('payment-success-scroll');
});
</script>

<template>
  <PaymentSuccessDummyContent v-if="AppConfig.useSuccessDummyPage" :task-id="taskId" />
  <PaymentSuccessContent v-else :task-id="taskId" />
</template>
