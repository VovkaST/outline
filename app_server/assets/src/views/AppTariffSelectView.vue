<script setup lang="ts">
import type {
  InitPaymentResponseV2,
  PaymentSystems,
  SubscriptionTaskResponse,
} from '@/api/generated/public';
import {
  AddSubscriptionButton,
  Announcement,
  DummyStorageInfo,
  Footer,
  Header,
  InfoCard,
  InfoCardList,
  SubscriptionRef,
  TariffsList,
} from '@/components/tariffs';
import { useConfig } from '@/composables/useConfig';
import { AppConfig } from '@/config/envConfig';
import { usePaymentStore } from '@/stores/payment';
import { useTasksStore } from '@/stores/tasks';
import NotFoundView from '@/views/NotFoundView.vue';
import { useToggle } from '@vueuse/core';
import { computed, onMounted, ref } from 'vue';
import { useRoute } from 'vue-router';

const route = useRoute();
const config = useConfig();
const paymentStore = usePaymentStore();
const tasksStore = useTasksStore();

const props = defineProps<{
  taskId: string;
}>();

const returnUrl = computed<string>(() => (route.query['returnUrl'] as string) || '');
const paymentAgent = computed<PaymentSystems>(
  () => (route.query['paymentAgent'] as PaymentSystems) || null,
);

const addSubscriptionUrlFromTask = ref<string>('');
const clientPhone = ref<string>('');
const taskInfoLoading = ref<boolean>(true);
const taskNotFound = ref<boolean>(false);
const addSubscriptionUrl = computed<string>(
  () => addSubscriptionUrlFromTask.value || config.value.subscriptionAddUrl || '',
);
const isWhatsappSubscriptionUrl = computed(() => {
  const url = addSubscriptionUrlFromTask.value.toLowerCase();
  return url.includes('whatsapp') || url.includes('wa.me');
});

const [formSubmitting, formSubmittingToggle] = useToggle(false);

const onActionClick = (price: number) => {
  formSubmitting.value = true;
  paymentStore
    .initPaymentV2({
      taskId: props.taskId,
      amount: price * 100,
      returnUrl: returnUrl.value,
      paymentAgent: paymentAgent.value,
    })
    .then(
      (response: InitPaymentResponseV2) => {
        window.location.href = response.confirmation_url;
      },
      (reason: unknown) => console.error('Init payment error: ', reason),
    )
    .finally(formSubmittingToggle);
};

onMounted(() => {
  tasksStore
    .getTaskInfo({ taskGuid: props.taskId })
    .then((response: SubscriptionTaskResponse) => {
      addSubscriptionUrlFromTask.value = response.subscription_add_url;
      clientPhone.value = response.client_phone;
      taskInfoLoading.value = false;
    })
    .catch(() => {
      taskNotFound.value = true;
    });
});
</script>

<template>
  <NotFoundView v-if="taskNotFound" />

  <div v-else class="page">
    <Announcement v-if="config.announcement">
      <template #title>{{ config.announcement.title }}</template>
      <p v-for="paragraph in config.announcement.paragraphs" :key="paragraph">
        {{ paragraph }}
      </p>
      <p v-if="config.announcement.cta" class="announcement-cta">
        {{ config.announcement.cta }}
      </p>
    </Announcement>

    <Header />
    <InfoCardList v-if="!taskInfoLoading && !AppConfig.useDummyConfig">
      <InfoCard v-if="isWhatsappSubscriptionUrl" gold>
        <template #icon>
          <svg
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
            stroke-linecap="round"
            stroke-linejoin="round"
          >
            <circle cx="12" cy="12" r="10" />
            <line x1="12" y1="8" x2="12" y2="12" />
            <line x1="12" y1="16" x2="12.01" y2="16" />
          </svg>
        </template>
        <strong>Внимание:</strong> оплата поступит для подписки клиента
        <span class="phone">{{ clientPhone }}</span>
      </InfoCard>
    </InfoCardList>

    <div v-if="config.site.tariffsHeader" class="tariff-heading">
      <h2 class="tariff-heading__title">{{ config.site.tariffsHeader }}</h2>
    </div>

    <SubscriptionRef
      v-if="!AppConfig.useDummyConfig && !isWhatsappSubscriptionUrl"
      :subscription-number="props.taskId"
    />

    <TariffsList
      :tariffs="config.tariffs"
      :wait="formSubmitting || taskInfoLoading"
      @actionClick="onActionClick"
    />

    <DummyStorageInfo v-if="AppConfig.useDummyConfig" />

    <Transition v-if="!AppConfig.useDummyConfig" name="content-fade">
      <InfoCardList v-if="!taskInfoLoading">
        <InfoCard>
          <template #icon>
            <svg
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
              stroke-linecap="round"
              stroke-linejoin="round"
            >
              <rect x="5" y="2" width="14" height="20" rx="2" ry="2" />
              <line x1="12" y1="18" x2="12.01" y2="18" />
            </svg>
          </template>
          <strong>1 ключ</strong> можно использовать <strong>только на одном устройстве</strong>.
        </InfoCard>
      </InfoCardList>
    </Transition>

    <Transition v-if="!AppConfig.useDummyConfig" name="content-fade">
      <AddSubscriptionButton
        v-if="!taskInfoLoading && isWhatsappSubscriptionUrl"
        :url="addSubscriptionUrl"
        :task-id="taskId"
      />
    </Transition>

    <Footer />
  </div>
</template>

<style lang="scss" scoped>
.page {
  max-width: 420px;
  width: 100%;
  text-align: center;
  margin: 0 auto;
}

.tariff-heading {
  background: var(--primary-soft);
  border: 1px solid rgba(201, 169, 97, 0.35);
  border-radius: 12px;
  padding: 16px 18px;
  margin-bottom: 14px;
}

.tariff-heading__title {
  margin: 0;
  font-size: 20px;
  letter-spacing: -0.4px;
  color: var(--primary);
}

@media (max-width: 380px) {
  .tariff-heading {
    padding: 14px 16px;
  }

  .tariff-heading__title {
    font-size: 18px;
  }
}

.content-fade-enter-active {
  transition:
    opacity 0.3s ease,
    transform 0.3s ease;
}

.content-fade-enter-from {
  opacity: 0;
  transform: translateY(8px);
}
</style>
