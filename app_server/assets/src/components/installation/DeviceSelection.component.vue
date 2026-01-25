<script setup lang="ts">
import { computed } from 'vue';

export type DeviceType = 'android' | 'iphone' | 'windows' | 'mac';

const props = defineProps<{
  selectedDevice: DeviceType | null;
  translations: {
    androidLabel: string;
    androidDesc: string;
    iphoneLabel: string;
    iphoneDesc: string;
    windowsLabel: string;
    windowsDesc: string;
    macLabel: string;
    macDesc: string;
  };
}>();

const emit = defineEmits<{
  (e: 'deviceSelect', device: DeviceType): void;
}>();

const devices: Array<{
  type: DeviceType;
  icon: string;
  label: string;
  desc: string;
}> = computed(() => [
  {
    type: 'android',
    icon: 'fab fa-android',
    label: props.translations.androidLabel,
    desc: props.translations.androidDesc,
  },
  {
    type: 'iphone',
    icon: 'fab fa-apple',
    label: props.translations.iphoneLabel,
    desc: props.translations.iphoneDesc,
  },
  {
    type: 'windows',
    icon: 'fab fa-windows',
    label: props.translations.windowsLabel,
    desc: props.translations.windowsDesc,
  },
  {
    type: 'mac',
    icon: 'fab fa-apple',
    label: props.translations.macLabel,
    desc: props.translations.macDesc,
  },
]);

const isSelected = (deviceType: DeviceType) => {
  return props.selectedDevice === deviceType;
};

const handleClick = (deviceType: DeviceType) => {
  emit('deviceSelect', deviceType);
};
</script>

<template>
  <div class="device-options">
    <button
      v-for="device in devices"
      :key="device.type"
      class="device-option"
      :class="{
        selected: isSelected(device.type),
      }"
      @click="handleClick(device.type)"
    >
      <div class="device-icon">
        <i :class="device.icon"></i>
      </div>
      <div class="device-info">
        <div class="device-name">{{ device.label }}</div>
        <div class="device-desc">{{ device.desc }}</div>
      </div>
    </button>
  </div>
</template>

<style scoped lang="scss">
.device-options {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-bottom: 20px;
}

.device-option {
  background: var(--light);
  border-radius: 12px;
  padding: 18px;
  display: flex;
  align-items: center;
  gap: 14px;
  cursor: pointer;
  border: 2px solid var(--border);
  transition: all 0.2s ease;
  -webkit-tap-highlight-color: rgba(99, 102, 241, 0.1);
  user-select: none;
  -webkit-user-select: none;
  -webkit-touch-callout: none;
  position: relative;
  text-decoration: none;
  color: inherit;
  text-align: left;
  width: 100%;

  .device-name {
    color: #1e293b;
    font-weight: 600;
    font-size: 16px;
    margin-bottom: 3px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }

  .device-desc {
    color: #475569;
    font-size: 12px;
    line-height: 1.3;
    -webkit-user-select: text;
    user-select: text;
  }

  &:active {
    transform: scale(0.98);
  }

  &:hover {
    border-color: var(--primary);
    box-shadow: 0 4px 12px rgba(99, 102, 241, 0.15);
  }

  &.selected {
    border-color: var(--primary);
    background: linear-gradient(135deg, rgba(99, 102, 241, 0.1), rgba(79, 70, 229, 0.1));
    box-shadow: 0 4px 16px rgba(99, 102, 241, 0.2);
  }
}

.device-icon {
  width: 44px;
  height: 44px;
  border-radius: 10px;
  background: linear-gradient(135deg, var(--primary), var(--primary-dark));
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;

  i {
    font-size: 22px;
    color: white;
  }
}

.device-info {
  flex: 1;
  min-width: 0;
}


@media (prefers-color-scheme: dark) {
  .device-option {
    background: rgba(255, 255, 255, 0.15);
    color: var(--dark);

    .device-name {
      color: #f1f5f9;
    }

    .device-desc {
      color: #cbd5e1;
    }
  }
}

@media (max-width: 360px) {
  .device-option {
    padding: 16px;
    gap: 12px;
  }

  .device-icon {
    width: 40px;
    height: 40px;

    i {
      font-size: 20px;
    }
  }
}
</style>
