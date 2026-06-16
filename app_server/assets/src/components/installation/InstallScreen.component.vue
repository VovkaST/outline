<script setup lang="ts">
import type { Translations } from '@/utils/translations';

type InstallIcon = 'apple' | 'android' | 'windows';

defineProps<{
  translations: Translations;
  installData: {
    platformText: string;
    ctaText: string;
    url: string;
    icon: InstallIcon;
  } | null;
}>();

const emit = defineEmits<{
  (e: 'continue'): void;
}>();
</script>

<template>
  <div class="screen active">
    <div class="logo-sm">
      <div class="logo-sm-mark">H</div>
      {{ translations.brand.nameFirst }} <span>{{ translations.brand.nameSecond }}</span>
    </div>

    <h1 class="screen-title">{{ translations.install.title }}</h1>
    <p class="screen-sub">{{ translations.install.subtitle }}</p>

    <div v-if="installData" class="install-card">
      <div class="install-icon" aria-hidden="true">
        <svg v-if="installData.icon === 'apple'" viewBox="0 0 24 24" fill="currentColor">
          <path
            d="M18.71 19.5c-.83 1.24-1.71 2.45-3.05 2.47-1.34.03-1.77-.79-3.29-.79-1.53 0-2 .77-3.27.82-1.31.05-2.3-1.32-3.14-2.53C4.25 17 2.94 12.45 4.7 9.39c.87-1.52 2.43-2.48 4.12-2.51 1.28-.02 2.5.87 3.29.87.78 0 2.26-1.07 3.81-.91.65.03 2.47.26 3.64 1.98-.09.06-2.17 1.28-2.15 3.81.03 3.02 2.65 4.03 2.68 4.04-.03.07-.42 1.44-1.38 2.83M13 3.5c.73-.83 1.94-1.46 2.94-1.5.13 1.17-.34 2.35-1.04 3.19-.69.85-1.83 1.51-2.95 1.42-.15-1.15.41-2.35 1.05-3.11z"
          />
        </svg>
        <svg v-else-if="installData.icon === 'android'" viewBox="0 0 24 24" fill="currentColor">
          <path
            d="M3.609 1.814 13.792 12 3.609 22.186a.996.996 0 0 1-.61-.92V2.734a1 1 0 0 1 .61-.92zm10.89 10.893 2.302 2.302-10.937 6.333 8.635-8.635zm3.199-3.198 2.807 1.626a1 1 0 0 1 0 1.73l-2.808 1.626L15.206 12l2.492-2.491zM5.864 2.658 16.802 8.99l-2.302 2.302L5.864 2.658z"
          />
        </svg>
        <svg v-else viewBox="0 0 24 24" fill="currentColor">
          <path
            d="M3 5.5 11 4v8H3V5.5zM3 18.5 11 20v-8H3v6.5zM12 4l9-1.5V12h-9V4zM12 12h9v9.5L12 20v-8z"
          />
        </svg>
      </div>

      <div class="install-title">{{ translations.install.appName }}</div>
      <div class="install-platform">{{ installData.platformText }}</div>

      <a class="cta" :href="installData.url" target="_blank" rel="noopener noreferrer">
        <svg
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          stroke-width="2.2"
          stroke-linecap="round"
          stroke-linejoin="round"
          aria-hidden="true"
        >
          <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" />
          <polyline points="7 10 12 15 17 10" />
          <line x1="12" y1="15" x2="12" y2="3" />
        </svg>
        <span>{{ installData.ctaText }}</span>
      </a>
    </div>

    <button class="secondary" type="button" @click="emit('continue')">
      {{ translations.install.continue }}
      <svg
        viewBox="0 0 24 24"
        fill="none"
        stroke="currentColor"
        stroke-width="2.2"
        stroke-linecap="round"
        stroke-linejoin="round"
        aria-hidden="true"
      >
        <line x1="5" y1="12" x2="19" y2="12" />
        <polyline points="12 5 19 12 12 19" />
      </svg>
    </button>
  </div>
</template>
