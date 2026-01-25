<script setup lang="ts">
import { computed } from 'vue';
import type { DeviceType } from './DeviceSelection.component.vue';
import { AppConfig } from '@/config/envConfig';

export interface StoreLink {
  url: string;
  text: string;
  icon: string;
  type: 'android' | 'apple' | 'windows';
}

const props = defineProps<{
  device: DeviceType | null;
  translations: {
    androidText: string;
    windowsText: string;
    appStoreUs: string;
    appStoreRu: string;
  };
}>();

const deviceLinks: Record<DeviceType, StoreLink[] | StoreLink> = {
  android: {
    url: AppConfig.android.url,
    text: 'Google Play',
    icon: 'fab fa-google-play',
    type: 'android',
  },
  iphone: [
    {
      url: AppConfig.iphone.appStoreUs,
      text: 'App Store (US)',
      icon: 'fab fa-apple',
      type: 'apple',
    },
    {
      url: AppConfig.iphone.appStoreRu,
      text: 'App Store (RU)',
      icon: 'fab fa-apple',
      type: 'apple',
    },
  ],
  windows: {
    url: AppConfig.windows.url,
    text: 'Скачать Happ для Windows',
    icon: 'fab fa-windows',
    type: 'windows',
  },
  mac: [
    {
      url: AppConfig.mac.appStoreUs,
      text: 'App Store (US)',
      icon: 'fab fa-apple',
      type: 'apple',
    },
    {
      url: AppConfig.mac.appStoreRu,
      text: 'App Store (RU)',
      icon: 'fab fa-apple',
      type: 'apple',
    },
  ],
};

const stores = computed(() => {
  if (!props.device) return [];
  const links = deviceLinks[props.device];
  return Array.isArray(links) ? links : [links];
});

const emit = defineEmits<{
  (e: 'storeClick', store: StoreLink): void;
}>();

const handleClick = (store: StoreLink) => {
  emit('storeClick', store);
};
</script>

<template>
  <div class="app-stores">
    <a
      v-for="(store, index) in stores"
      :key="index"
      :href="store.url"
      :class="['store-btn', store.type]"
      target="_blank"
      rel="noopener noreferrer"
      :download="store.type === 'windows' ? 'setup-Happ.x64.exe' : undefined"
      @click="handleClick(store)"
    >
      <i :class="store.icon"></i>
      {{ store.text }}
    </a>
  </div>
</template>

<style scoped lang="scss">
.app-stores {
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin: 20px 0;
}

.store-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  padding: 16px;
  background: var(--light);
  border-radius: 12px;
  text-decoration: none;
  color: var(--dark);
  font-weight: 600;
  font-size: 15px;
  transition: all 0.2s ease;
  border: 2px solid var(--border);
  -webkit-tap-highlight-color: rgba(0, 0, 0, 0.1);
  user-select: none;

  &:active {
    transform: scale(0.98);
  }

  &:hover {
    border-color: var(--primary);
    box-shadow: 0 4px 12px rgba(99, 102, 241, 0.15);
  }

  &.windows {
    background: #0078d4;
    color: white;
    border-color: #0078d4;

    &:hover {
      background: #106ebe;
      border-color: #106ebe;
    }
  }

  &.apple {
    background: #000;
    color: white;
    border-color: #000;

    &:hover {
      background: #333;
      border-color: #333;
    }
  }

  &.android {
    background: #3ddc84;
    color: #000;
    border-color: #3ddc84;

    &:hover {
      background: #2bc973;
      border-color: #2bc973;
    }
  }
}

@media (max-width: 360px) {
  .store-btn {
    padding: 14px;
    font-size: 14px;
  }
}

@media (prefers-color-scheme: dark) {
  .store-btn {
    background: rgba(255, 255, 255, 0.15);
    color: var(--dark);
  }
}
</style>
