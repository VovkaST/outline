import { defineStore } from 'pinia';
import {
  OpenAPI,
  OrdersService,
  PaymentsV1Service,
  PaymentsV2Service,
  SubscriptionService,
} from '@/api/generated/public';

if (import.meta.env.DEV) {
  OpenAPI.BASE = 'http://127.0.0.1:8000';
}

export const usePaymentStore = defineStore('payment', {
  actions: {
    checkOrder({ guid }: { guid: string }) {
      return OrdersService.checkOrder({ taskGuid: guid });
    },

    initPayment({
      guid,
      isRecurrent = false,
      useQr = false,
    }: {
      guid: string;
      isRecurrent?: boolean;
      useQr?: boolean;
    }) {
      return PaymentsV1Service.initPayment({ taskGuid: guid, isRecurrent, useQr });
    },

    initYooKassaPayment({
      taskId,
      amount,
      customerEmail = '',
      description = '',
      returnUrl = '',
    }: {
      taskId: string;
      amount: number;
      customerEmail?: string;
      description?: string;
      returnUrl?: string;
    }) {
      return PaymentsV2Service.initYookassaPayment({
        taskId,
        amount,
        customerEmail,
        description,
        returnUrl,
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
