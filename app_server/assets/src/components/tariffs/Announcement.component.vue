<script setup lang="ts">
import { useConfig } from '@/composables/useConfig';
import { computed, onUnmounted, ref, watch } from 'vue';

const config = useConfig();
const announcement = computed(() => config.value.announcement);

const deadlineMs = computed<number | null>(() => {
  const rawDeadline = announcement.value?.deadline;
  if (!rawDeadline) {
    return null;
  }
  const parsed = Date.parse(rawDeadline);
  return Number.isNaN(parsed) ? null : parsed;
});

const remainingMs = ref<number>(0);
let timerId: ReturnType<typeof window.setInterval> | null = null;

const updateRemaining = (): void => {
  const deadline = deadlineMs.value;
  if (!deadline) {
    remainingMs.value = 0;
    return;
  }
  const diff = deadline - Date.now();
  remainingMs.value = diff > 0 ? diff : 0;
  if (diff <= 0 && timerId) {
    window.clearInterval(timerId);
    timerId = null;
  }
};

const startTimer = (): void => {
  if (timerId) {
    window.clearInterval(timerId);
    timerId = null;
  }
  updateRemaining();
  const deadline = deadlineMs.value;
  if (deadline && deadline > Date.now()) {
    timerId = window.setInterval(updateRemaining, 1000);
  }
};

watch(deadlineMs, startTimer, { immediate: true });

onUnmounted(() => {
  if (timerId) {
    window.clearInterval(timerId);
    timerId = null;
  }
});

const showCountdown = computed<boolean>(() => deadlineMs.value !== null && remainingMs.value > 0);
const showAnnouncement = computed<boolean>(
  () => !!announcement.value && (!deadlineMs.value || remainingMs.value > 0),
);

const pad = (value: number): string => (value < 10 ? `0${value}` : `${value}`);
const totalSeconds = computed<number>(() => Math.floor(remainingMs.value / 1000));
const days = computed<number>(() => Math.floor(totalSeconds.value / 86400));
const hours = computed<number>(() => Math.floor((totalSeconds.value % 86400) / 3600));
const mins = computed<number>(() => Math.floor((totalSeconds.value % 3600) / 60));
const secs = computed<number>(() => totalSeconds.value % 60);

const daysText = computed<string>(() => pad(days.value));
const hoursText = computed<string>(() => pad(hours.value));
const minsText = computed<string>(() => pad(mins.value));
const secsText = computed<string>(() => pad(secs.value));
</script>

<template>
  <div v-if="showAnnouncement" class="announcement">
    <div class="announcement-title">
      <svg
        viewBox="0 0 24 24"
        fill="none"
        stroke="currentColor"
        stroke-width="2"
        stroke-linecap="round"
        stroke-linejoin="round"
      >
        <path
          d="M10.29 3.86 1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"
        />
        <line x1="12" y1="9" x2="12" y2="13" />
        <line x1="12" y1="17" x2="12.01" y2="17" />
      </svg>
      <slot name="title" />
    </div>
    <slot />
    <div v-if="showCountdown" class="countdown" aria-live="polite">
      <div class="countdown-cell">
        <div class="countdown-num">{{ daysText }}</div>
        <span class="countdown-label">дней</span>
      </div>
      <div class="countdown-cell">
        <div class="countdown-num">{{ hoursText }}</div>
        <span class="countdown-label">часов</span>
      </div>
      <div class="countdown-cell">
        <div class="countdown-num">{{ minsText }}</div>
        <span class="countdown-label">минут</span>
      </div>
      <div class="countdown-cell">
        <div class="countdown-num">{{ secsText }}</div>
        <span class="countdown-label">секунд</span>
      </div>
    </div>
  </div>
</template>

<style lang="scss" scoped>
.announcement {
  background: linear-gradient(135deg, #fdf6e3 0%, #faf3e3 100%);
  border: 1px solid var(--primary);
  border-radius: 12px;
  padding: 16px 18px;
  margin-bottom: 28px;
  text-align: left;
}

.announcement-title {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  font-weight: 700;
  color: #8a6d28;
  margin-bottom: 8px;
  letter-spacing: -0.1px;
}

.announcement-title svg {
  width: 18px;
  height: 18px;
  flex-shrink: 0;
}

:slotted(p) {
  font-size: 13px;
  line-height: 1.55;
  color: #6b5320;
  margin-bottom: 6px;
}

:slotted(p:last-child) {
  margin-bottom: 0;
}

:slotted(.announcement-cta) {
  font-weight: 700;
  color: #5d4818;
}

.countdown {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 8px;
  margin-top: 12px;

  &-cell {
    background: #fff;
    border: 1px solid var(--primary);
    border-radius: 10px;
    padding: 8px 4px 6px;
    text-align: center;
    box-shadow: 0 2px 6px rgba(201, 169, 97, 0.18);
  }

  &-num {
    font-size: 22px;
    font-weight: 800;
    color: #5d4818;
    letter-spacing: -0.5px;
    line-height: 1;
    font-variant-numeric: tabular-nums;
  }

  &-label {
    display: block;
    margin-top: 4px;
    font-size: 10px;
    font-weight: 600;
    color: #8a6d28;
    text-transform: uppercase;
    letter-spacing: 0.4px;
  }
}

@media (max-width: 380px) {
  .announcement {
    padding: 14px 16px;
    margin-bottom: 22px;
  }

  .announcement-title {
    font-size: 13px;
  }

  :slotted(p) {
    font-size: 12.5px;
  }
}
</style>
