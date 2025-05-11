import { defineStore } from 'pinia';
import {
  OpenAPI,
  OrdersService,
  PaymentsService,
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
      return PaymentsService.initPayment({ taskGuid: guid, isRecurrent, useQr });
    },

    getPaymentStatus({ paymentId }: { paymentId: number }) {
      return PaymentsService.getPaymentStatus({ paymentId });
    },

    subscriptionReject({ guid }: { guid: string }) {
      return SubscriptionService.subscriptionReject({ requestBody: { task_guid: guid } });
    },
  },
});
