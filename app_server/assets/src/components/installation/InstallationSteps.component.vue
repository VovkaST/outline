<script setup lang="ts">
import { computed } from 'vue';
import type { StoreLink } from './AppStores.component.vue';
import AppStores from './AppStores.component.vue';
import type { DeviceType } from './DeviceSelection.component.vue';
import DeviceSelection from './DeviceSelection.component.vue';
import Step from './Step.component.vue';
import SubscriptionCard from './SubscriptionCard.component.vue';

import type { Translations } from '@/utils/translations';

const props = defineProps<{
  currentStep: number;
  selectedDevice: DeviceType | null;
  translations: Translations;
  subscriptionUrl: string;
}>();

const emit = defineEmits<{
  (e: 'deviceSelect', device: DeviceType): void;
  (e: 'stepChange', step: number): void;
  (e: 'storeClick', store: StoreLink): void;
}>();

const deviceSelectionTranslations = computed(() => ({
  androidLabel: props.translations.devices.android.label,
  androidDesc: props.translations.devices.android.desc,
  iphoneLabel: props.translations.devices.iphone.label,
  iphoneDesc: props.translations.devices.iphone.desc,
  windowsLabel: props.translations.devices.windows.label,
  windowsDesc: props.translations.devices.windows.desc,
  macLabel: props.translations.devices.mac.label,
  macDesc: props.translations.devices.mac.desc,
}));

const appStoresTranslations = computed(() => ({
  androidText: props.translations.stores.android,
  windowsText: props.translations.stores.windows,
  appStoreUs: props.translations.stores.appStoreUs,
  appStoreRu: props.translations.stores.appStoreRu,
}));

const subscriptionTranslations = computed(() => ({
  title: props.translations.subscription.title,
  desc: props.translations.subscription.desc,
  buttonText: props.translations.subscription.button,
  note: props.translations.subscription.note,
  wait: props.translations.subscription.wait,
  imagePaymentNote: props.translations.subscription.imagePaymentNote,
  imagePaymentDescription: props.translations.subscription.imagePaymentDescription,
}));

const handleDeviceSelect = (device: DeviceType) => {
  emit('deviceSelect', device);
};

const handleStepChange = (step: number) => {
  emit('stepChange', step);
};

const handleStoreClick = (store: StoreLink) => {
  emit('storeClick', store);
};
</script>

<template>
  <div class="steps-container">
    <!-- Шаг 1: Выбор устройства -->
    <Step
      v-show="currentStep === 1"
      :step-number="1"
      :title="translations.steps.step1.title"
      :instruction="translations.steps.step1.instruction"
    >
      <DeviceSelection
        :selected-device="selectedDevice"
        :translations="deviceSelectionTranslations"
        @device-select="handleDeviceSelect"
      />
    </Step>

    <!-- Шаг 2: Установка приложения -->
    <Step
      v-show="currentStep === 2"
      :step-number="2"
      :title="translations.steps.step2.title"
      :instruction="translations.steps.step2.instruction"
    >
      <AppStores
        :device="selectedDevice"
        :translations="appStoresTranslations"
        @store-click="handleStoreClick"
      />

      <div class="buttons-container">
        <button class="btn" @click="handleStepChange(3)">
          <i class="fas fa-check"></i>
          {{ translations.buttons.installed }}
        </button>
        <button class="btn btn-back" @click="handleStepChange(1)">
          <i class="fas fa-arrow-left"></i>
          {{ translations.common.back }}
        </button>
      </div>
    </Step>

    <!-- Шаг 3: Активация подписки -->
    <Step v-show="currentStep === 3" :step-number="3" :title="translations.steps.step3.title">
      <SubscriptionCard
        :subscription-url="subscriptionUrl"
        :translations="subscriptionTranslations"
      />

      <div class="buttons-container">
        <button class="btn btn-back" @click="handleStepChange(2)">
          <i class="fas fa-arrow-left"></i>
          {{ translations.common.back }}
        </button>
      </div>
    </Step>
  </div>
</template>

<style scoped lang="scss">
.steps-container {
  width: 100%;
}

.buttons-container {
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin-top: 20px;
}

.btn {
  display: block;
  width: 100%;
  padding: 16px;
  background: linear-gradient(135deg, var(--primary), var(--primary-dark));
  color: white;
  border: none;
  border-radius: 12px;
  font-size: 15px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  text-align: center;
  text-decoration: none;
  -webkit-tap-highlight-color: rgba(99, 102, 241, 0.2);
  user-select: none;
  position: relative;
  overflow: hidden;

  i {
    margin-right: 8px;
    font-size: 14px;
  }

  &:active {
    transform: scale(0.98);
  }

  &:hover {
    box-shadow: 0 8px 20px rgba(99, 102, 241, 0.35);
  }
}

.btn-back {
  background: var(--light);
  color: var(--gray);
  border: 2px solid var(--border);
}

.btn-back:hover {
  background: var(--border);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.info-note {
  background: linear-gradient(135deg, rgba(99, 102, 241, 0.1), rgba(79, 70, 229, 0.1));
  border-left: 4px solid var(--primary);
  padding: 16px;
  border-radius: 10px;
  margin: 20px 0;
  font-size: 13px;
  color: var(--dark);
  line-height: 1.4;
  -webkit-user-select: text;
  user-select: text;

  i {
    color: var(--primary);
    margin-right: 8px;
    font-size: 14px;
  }
}

@media (max-width: 360px) {
  .btn,
  .store-btn {
    padding: 14px;
    font-size: 14px;
  }
}

@media (min-height: 900px) {
  .buttons-container {
    gap: 12px;
  }

  .btn {
    padding: 18px;
  }
}

@media (prefers-color-scheme: dark) {
  .btn-back {
    background: rgba(255, 255, 255, 0.15);
    border-color: var(--border);
    color: var(--dark);

    &:hover {
      background: rgba(255, 255, 255, 0.2);
    }
  }

  .info-note {
    background: rgba(255, 255, 255, 0.1);
  }
}
</style>
