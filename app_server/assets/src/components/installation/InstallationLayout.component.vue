<script setup lang="ts">
import type { CreateTaskResponse, GetTaskKeyResponse } from '@/api/generated/public';
import { LanguageSwitcher } from '@/components/installation';
import { AppConfig } from '@/config/envConfig';
import { useTasksStore } from '@/stores/tasks';
import {
  detectLanguage,
  getTranslations,
  type Language,
  type Translations,
} from '@/utils/translations';
import { computed, onMounted, onUnmounted, ref } from 'vue';
import ActivationModal from './ActivationModal.component.vue';
import DeviceScreen, { type DeviceType } from './DeviceScreen.component.vue';
import InstallScreen from './InstallScreen.component.vue';
import WelcomeScreen from './WelcomeScreen.component.vue';

type ScreenId = 'welcome' | 'device' | 'install';

const tasksStore = useTasksStore();

const isLoading = ref<boolean>(true);
const currentLanguage = ref<Language>('ru');
const translations = computed<Translations>(() => getTranslations(currentLanguage.value));

const currentScreen = ref<ScreenId>('welcome');
const screenHistory = ref<ScreenId[]>(['welcome']);

const selectedDevice = ref<DeviceType | null>(null);

const stepDone = ref<number>(0);

const setStepDone = (n: number) => {
  stepDone.value = n;
};

const handleLanguageChange = (lang: Language) => {
  currentLanguage.value = lang;
  localStorage.setItem('preferredLanguage', lang);
};

const goTo = (screen: ScreenId) => {
  if (screen === 'welcome') {
    screenHistory.value = ['welcome'];
  } else if (screenHistory.value[screenHistory.value.length - 1] !== screen) {
    screenHistory.value.push(screen);
  }
  currentScreen.value = screen;
  window.scrollTo(0, 0);
};

const goBack = () => {
  if (screenHistory.value.length <= 1) return;
  screenHistory.value.pop();
  currentScreen.value = screenHistory.value[screenHistory.value.length - 1] || 'welcome';
  window.scrollTo(0, 0);
};

const subscriptionUrl = ref<string>('');
const isKeyFetching = ref<boolean>(false);
const pollingInterval = ref<number | undefined>(undefined);

const pollingStart = (taskId: number) => {
  pollingInterval.value = window.setInterval(() => polling(taskId), AppConfig.poolingInterval);
};

const pollingStop = () => {
  if (pollingInterval.value) {
    clearInterval(pollingInterval.value);
    pollingInterval.value = undefined;
  }
  isKeyFetching.value = false;
};

const polling = async (taskId: number) => {
  await tasksStore.getTaskKey({ taskId }).then((response: GetTaskKeyResponse) => {
    if (response.key) {
      subscriptionUrl.value = response.key;
      pollingStop();
    }
  });
};

const ensureKeyFetching = () => {
  if (isKeyFetching.value) return;
  isKeyFetching.value = true;
  tasksStore.createTask().then((response: CreateTaskResponse) => {
    pollingStart(response.id);
  });
};

const pickDevice = (device: DeviceType) => {
  selectedDevice.value = device;
  ensureKeyFetching();
  goTo('install');
};

const finishInstallToStep2 = () => {
  setStepDone(Math.max(stepDone.value, 1));
  goTo('welcome');
};

const isSubscriptionReady = computed(() => !!subscriptionUrl.value);
const canDoStep2 = computed(() => stepDone.value >= 1 && isSubscriptionReady.value);
const canDoStep3 = computed(() => stepDone.value >= 2);

const getHappDeepLink = (raw: string) => {
  if (raw.startsWith('happ://')) return raw;
  return `happ://add/${encodeURIComponent(raw)}`;
};

const onWelcomeStep1 = () => goTo('device');
const onWelcomeStep2 = () => {
  if (!canDoStep2.value) return;
  setStepDone(Math.max(stepDone.value, 2));
  window.location.href = getHappDeepLink(subscriptionUrl.value);
};

const lockScrollState = ref<{ y: number } | null>(null);
const lockScroll = () => {
  if (lockScrollState.value) return;
  const y = window.scrollY || 0;
  lockScrollState.value = { y };
  document.body.style.top = `-${y}px`;
  document.body.classList.add('modal-open');
};
const unlockScroll = () => {
  const state = lockScrollState.value;
  if (!state) return;
  document.body.classList.remove('modal-open');
  document.body.style.top = '';
  lockScrollState.value = null;
  window.scrollTo(0, state.y);
};

const isActivationModalOpen = ref<boolean>(false);
const openActivationModal = () => {
  if (!canDoStep3.value) return;
  isActivationModalOpen.value = true;
  setStepDone(Math.max(stepDone.value, 3));
  lockScroll();
};
const closeActivationModal = () => {
  isActivationModalOpen.value = false;
  unlockScroll();
};

const handleKeyDown = (e: KeyboardEvent) => {
  if (e.key === 'Escape' && isActivationModalOpen.value) {
    closeActivationModal();
  }
};

const installData = computed(() => {
  const lang = currentLanguage.value;
  const device = selectedDevice.value;
  if (!device) return null;

  if (device === 'android') {
    return {
      platformText: translations.value.install.platform.android,
      ctaText: translations.value.install.cta.android,
      url: AppConfig.android.url,
      icon: 'android' as const,
    };
  }
  if (device === 'windows') {
    return {
      platformText: translations.value.install.platform.windows,
      ctaText: translations.value.install.cta.windows,
      url: AppConfig.windows.url,
      icon: 'windows' as const,
    };
  }
  if (device === 'iphone') {
    return {
      platformText: translations.value.install.platform.iphone,
      ctaText: translations.value.install.cta.ios,
      url: lang === 'ru' ? AppConfig.iphone.appStoreRu : AppConfig.iphone.appStoreUs,
      icon: 'apple' as const,
    };
  }
  return {
    platformText: translations.value.install.platform.mac,
    ctaText: translations.value.install.cta.ios,
    url: lang === 'ru' ? AppConfig.mac.appStoreRu : AppConfig.mac.appStoreUs,
    icon: 'apple' as const,
  };
});

onMounted(() => {
  setTimeout(() => {
    isLoading.value = false;
  }, 150);

  currentLanguage.value = detectLanguage();
  document.addEventListener('keydown', handleKeyDown);
});

onUnmounted(() => {
  if (pollingInterval.value) clearInterval(pollingInterval.value);
  document.removeEventListener('keydown', handleKeyDown);
  unlockScroll();
});
</script>

<template>
  <div class="installation2">
    <div class="lang-float">
      <LanguageSwitcher
        :current-language="currentLanguage"
        @language-change="handleLanguageChange"
      />
    </div>

    <div v-if="isLoading" class="loading">{{ translations.common.loading }}</div>

    <div v-else class="page">
      <div class="topbar">
        <div v-if="currentScreen !== 'welcome'" class="header">
          <button class="back" type="button" @click="goBack">
            <svg
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="2.5"
              stroke-linecap="round"
              stroke-linejoin="round"
              aria-hidden="true"
            >
              <polyline points="15 18 9 12 15 6" />
            </svg>
          </button>
        </div>
      </div>

      <WelcomeScreen
        v-if="currentScreen === 'welcome'"
        :translations="translations"
        :step-done="stepDone"
        :is-subscription-ready="isSubscriptionReady"
        :can-do-step2="canDoStep2"
        :can-do-step3="canDoStep3"
        @step1="onWelcomeStep1"
        @step2="onWelcomeStep2"
        @step3="openActivationModal"
      />

      <DeviceScreen
        v-else-if="currentScreen === 'device'"
        :translations="translations"
        @pickDevice="pickDevice"
      />

      <InstallScreen
        v-else
        :translations="translations"
        :install-data="installData"
        @continue="finishInstallToStep2"
      />

      <ActivationModal
        :open="isActivationModalOpen"
        :translations="translations"
        @close="closeActivationModal"
        @goInstall="goTo('device')"
      />
    </div>
  </div>
</template>
