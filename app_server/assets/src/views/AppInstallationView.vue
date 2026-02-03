<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue';
import { InstallationSteps, ProgressBar, LanguageSwitcher } from '@/components/installation';
import type { DeviceType } from '@/components/installation/DeviceSelection.component.vue';
import type { StoreLink } from '@/components/installation/AppStores.component.vue';
import {
  getTranslations,
  detectLanguage,
  type Language,
  type Translations,
} from '@/utils/translations';
import { AppConfig } from '@/config/envConfig';
import { useTasksStore } from '@/stores/tasks';
import { useToggle } from '@vueuse/core';

const currentStep = ref<number>(1);
const selectedDevice = ref<DeviceType | null>(null);
const currentLanguage = ref<Language>('ru');
const isLoading = ref<boolean>(true);

const tasksStore = useTasksStore();
const [isKeyFetching, isKeyFetchingToggle] = useToggle();

const translations = computed<Translations>(() => getTranslations(currentLanguage.value));

const subscriptionUrl = ref<string>('');

const setVH = () => {
  const vh = window.innerHeight * 0.01;
  document.documentElement.style.setProperty('--vh', `${vh}px`);

  if (/iPad|iPhone|iPod/.test(navigator.userAgent) && !(window as any).MSStream) {
    const body = document.body;
    const html = document.documentElement;
    body.style.minHeight = 'auto';
    body.style.height = 'auto';
    body.style.overflowY = 'auto';
    html.style.overflowY = 'auto';
  }
};

const showNotification = (message: string, duration = 2000) => {
  const notification = document.createElement('div');
  notification.className = 'notification';
  notification.textContent = message;
  document.body.appendChild(notification);

  setTimeout(() => {
    notification.remove();
  }, duration);
};

const handleDeviceSelect = (device: DeviceType) => {
  selectedDevice.value = device;
  setTimeout(() => {
    currentStep.value = 2;
  }, 300);
  if (!isKeyFetching.value) {
    isKeyFetchingToggle(true);
    tasksStore.createTask().then((response) => {
      pollingStart(response.id);
    });
  }
};

const pollingInterval = ref();
const pollingStart = (taskId: number) => {
  pollingInterval.value = setInterval(() => polling(taskId), AppConfig.poolingInterval);
};
const pollingStop = () => {
  clearInterval(pollingInterval.value);
  isKeyFetchingToggle(false);
};
const polling = async (taskId: number) => {
  await tasksStore.getTaskKey({ taskId }).then((response) => {
    if (response.key) {
      subscriptionUrl.value = response.key;
      pollingStop();
    }
  });
};

const handleStepChange = (step: number) => {
  currentStep.value = step;
  if (step === 1) {
    selectedDevice.value = null;
  }
  window.scrollTo({ top: 0, behavior: 'smooth' });

  const isIOS = /iPad|iPhone|iPod/.test(navigator.userAgent) && !window.MSStream;
  if (isIOS) {
    document.body.scrollTop = 0;
    document.documentElement.scrollTop = 0;
  }
};

const handleStoreClick = (_store: StoreLink) => {
  let message = '';
  if (selectedDevice.value === 'iphone' || selectedDevice.value === 'mac') {
    message = translations.value.notifications.appStore;
  } else if (selectedDevice.value === 'android') {
    message = translations.value.notifications.playStore;
  } else if (selectedDevice.value === 'windows') {
    message = translations.value.notifications.windows;
  } else {
    message = translations.value.notifications.general;
  }
  setTimeout(() => showNotification(message), 300);
};

const handleLanguageChange = (lang: Language) => {
  currentLanguage.value = lang;
  localStorage.setItem('preferredLanguage', lang);
};

onMounted(() => {
  setTimeout(() => {
    isLoading.value = false;
  }, 300);

  const initialLanguage = detectLanguage();
  currentLanguage.value = initialLanguage;

  setVH();
  window.addEventListener('resize', setVH);
  window.addEventListener('orientationchange', setVH);
});

onUnmounted(() => {
  window.removeEventListener('resize', setVH);
  window.removeEventListener('orientationchange', setVH);
  if (pollingInterval.value) {
    clearInterval(pollingInterval.value);
  }
});
</script>

<template>
  <div class="installation-view">
    <div v-if="isLoading" class="loading-placeholder">
      <div>{{ translations.common.loading }}</div>
    </div>

    <div v-else class="installation-container">
      <LanguageSwitcher
        :current-language="currentLanguage"
        @language-change="handleLanguageChange"
      />

      <div class="installation-header">
        <div class="installation-logo">
          <img
            src="/static/logo.jpg"
            :alt="translations.header.logoAlt"
            class="logo-img"
            id="logoImage"
          />
        </div>
        <h1 class="installation-title">{{ translations.header.title }}</h1>
        <p class="installation-subtitle">{{ translations.header.subtitle }}</p>
      </div>

      <ProgressBar :current-step="currentStep" :total-steps="3" />

      <InstallationSteps
        :current-step="currentStep"
        :selected-device="selectedDevice"
        :translations="translations"
        :subscription-url="subscriptionUrl"
        @device-select="handleDeviceSelect"
        @step-change="handleStepChange"
        @store-click="handleStoreClick"
      />
    </div>
  </div>
</template>

<style lang="scss" scoped>
@import '@/assets/installation.scss';

.installation-view {
  min-height: 100vh;
  min-height: calc(var(--vh, 1vh) * 100);
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  background-attachment: fixed;
  color: var(--dark);
  line-height: 1.5;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  overflow-x: hidden;
  position: relative;
  -webkit-user-select: none;
  user-select: none;

  .logo-img {
    width: 100%;
    height: 100%;
    object-fit: contain;
    border-radius: 12px;
  }
}

@media (prefers-color-scheme: dark) {
  .installation-view {
    background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);
  }
}

@supports (-webkit-touch-callout: none) {
  .logo-img {
    object-fit: cover;
  }
}
</style>
