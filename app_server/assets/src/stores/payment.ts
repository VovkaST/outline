import { defineStore } from 'pinia';
import { OpenAPI, ServerService } from '@/api/generated/public';

if (import.meta.env.DEV) {
  OpenAPI.BASE = 'http://127.0.0.1:8000';
}

export const usePaymentStore = defineStore('payment', {
  actions: {
    checkOrder({ guid }: { guid: string }) {
      return ServerService.checkOrder({ taskGuid: guid });
    },

    getPaymentURL({ guid }: { guid: string }) {
      return ServerService.getPaymentUrl({ taskGuid: guid });
    },

    subscriptionReject({ guid }: { guid: string }) {
      return ServerService.subscriptionReject({ requestBody: { task_guid: guid } });
    },
  },
});
