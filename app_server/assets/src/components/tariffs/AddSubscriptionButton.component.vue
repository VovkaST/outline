<script setup lang="ts">
import { computed } from 'vue';

const props = defineProps<{
  url: string;
  taskId: string;
}>();

const href = computed(() => props.url.replace('{task_id}', props.taskId));
</script>

<template>
  <a v-if="url" class="trial-button" :href="href" target="_blank" rel="noopener">
    <svg
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
      <span class="trial-button__title">Получить пробную подписку</span>
      <span class="trial-button__hint">если это не ваш номер</span>
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
  background: #fff;
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
  color: #fff;
  transform: translateY(-1px);
  box-shadow: 0 6px 18px rgba(201, 169, 97, 0.3);
}

.trial-button:hover .trial-button__title {
  color: #fff;
}

.trial-button:hover .trial-button__hint {
  color: rgba(255, 255, 255, 0.75);
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
    background: #fff;
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
