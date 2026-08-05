<script setup lang="ts">
import { useConfig } from '@/composables/useConfig';
import { computed } from 'vue';

const props = defineProps<{
  url: string;
  taskId: string;
}>();

const config = useConfig();

const href = computed(() => props.url.replace('{task_id}', props.taskId));
const isBabochkiTheme = computed<boolean>(() => config.value.site.theme === 'babochki');
</script>

<template>
  <a v-if="url" class="trial-button" :href="href" target="_blank" rel="noopener">
    <svg
      v-if="isBabochkiTheme"
      class="trial-button__icon"
      viewBox="0 0 24 24"
      fill="currentColor"
      aria-hidden="true"
    >
      <path
        d="M21.7 3.3 18.5 19c-.24 1.11-.88 1.38-1.78.86l-4.87-3.59-2.35 2.26c-.26.26-.48.48-.98.48l.35-4.96 9.02-8.15c.39-.35-.09-.55-.61-.2L6.13 12.73l-4.8-1.5c-1.04-.33-1.06-1.04.22-1.54L20.3 2.47c.87-.32 1.63.2 1.4.83Z"
      />
    </svg>

    <svg
      v-else
      class="trial-button__icon"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      stroke-width="2"
      stroke-linecap="round"
      stroke-linejoin="round"
      aria-hidden="true"
    >
      <circle cx="7.5" cy="15.5" r="5.5" />
      <path d="m21 2-9.6 9.6" />
      <path d="m15.5 7.5 3 3L22 7l-3-3" />
    </svg>
    <span class="trial-button__text">
      <span class="trial-button__title">
        {{ isBabochkiTheme ? 'Получить пробную подписку в Telegram' : 'Получить пробную подписку' }}
      </span>
      <span v-if="!isBabochkiTheme" class="trial-button__hint">
        если это не ваш номер
      </span>
    </span>
  </a>
</template>

<style lang="scss" scoped>
.trial-button {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  width: 100%;
  min-height: 76px;
  margin-top: 12px;
  padding: 16px 22px;
  background: var(--trial-button-background);
  border: 1.5px solid var(--primary);
  border-radius: 12px;
  color: var(--primary);
  font-family: inherit;
  text-decoration: none;
  cursor: pointer;
  transition: all 0.15s ease;
}

.trial-button__icon {
  flex-shrink: 0;
  width: 18px;
  height: 18px;
}

.trial-button__text {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 2px;
  text-align: center;
}

.trial-button__title {
  font-size: 15px;
  font-weight: 600;
  line-height: 1.3;
  color: var(--primary);
  transition: color 0.15s ease;
}

.trial-button__hint {
  font-size: var(--sm);
  font-weight: 400;
  line-height: 1.3;
  color: var(--ink-dim);
  transition: color 0.15s ease;
}

.trial-button:hover {
  background: var(--primary);
  color: var(--trial-button-hover-ink);
  transform: translateY(-1px);
  box-shadow: var(--trial-button-hover-shadow);
}

.trial-button:hover .trial-button__title {
  color: var(--trial-button-hover-ink);
}

.trial-button:hover .trial-button__hint {
  color: var(--trial-button-hover-hint);
}

@media (max-width: 380px) {
  .trial-button {
    padding: 14px 18px;
  }

  .trial-button__title {
    font-size: 14px;
  }

  .trial-button__hint {
    font-size: 12px;
  }
}

@media (hover: none) {
  .trial-button:hover {
    background: var(--trial-button-background);
    color: var(--primary);
    transform: none;
    box-shadow: none;
  }

  .trial-button:hover .trial-button__title {
    color: var(--primary);
  }

  .trial-button:hover .trial-button__hint {
    color: var(--ink-dim);
  }

  .trial-button:active {
    transform: scale(0.98);
    transition: transform 0.1s;
  }
}
</style>
