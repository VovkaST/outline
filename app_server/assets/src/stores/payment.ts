import {
  OpenAPI,
  OrdersService,
  PaymentsV1Service,
  PaymentsV2Service,
  PaymentSystems,
  SubscriptionService,
} from '@/api/generated/public';
import { getEnvVar } from '@/config/utils';
import { defineStore } from 'pinia';

if (import.meta.env.DEV) {
  OpenAPI.BASE = getEnvVar("VITE_BASE_URL", 'http://127.0.0.1:8000');
}

export const usePaymentStore = defineStore('payment', {
  actions: {
    checkOrder({ guid }: { guid: string }) {
      return OrdersService.checkOrder({ taskGuid: guid });
    },

    initPayment({
      guid,
      amount,
      isRecurrent = false,
      useQr = false,
    }: {
      guid: string;
      amount: number;
      isRecurrent?: boolean;
      useQr?: boolean;
    }) {
      return PaymentsV1Service.initPayment({ taskGuid: guid, amount, isRecurrent, useQr });
    },

    initPaymentV2({
      taskId,
      amount,
      customerEmail = '',
      description = '',
      returnUrl = '',
      paymentAgent,
    }: {
      taskId: string;
      amount: number;
      customerEmail?: string;
      description?: string;
      returnUrl?: string;
      paymentAgent?: PaymentSystems;
    }) {
      return PaymentsV2Service.initPaymentV2({
        taskId,
        amount,
        customerEmail,
        description,
        returnUrl,
        paymentAgent
      });
    },

    getPaymentStatus({ paymentId }: { paymentId: number }) {
      return PaymentsV1Service.getPaymentStatus({ paymentId });
    },

    subscriptionReject({ guid }: { guid: string }) {
      return SubscriptionService.subscriptionReject({ requestBody: { task_guid: guid } });
    },
  },
});
