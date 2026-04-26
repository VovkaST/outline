<script setup lang="ts">
import { computed } from 'vue';

const props = defineProps<{
  url: string;
  taskId: string;
}>();

const href = computed(() => props.url.replace('{task_id}', props.taskId));
</script>

<template>
  <a v-if="url" class="key-btn" :href="href" target="_blank" rel="noopener">
    <svg
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      stroke-width="2"
      stroke-linecap="round"
      stroke-linejoin="round"
    >
      <circle cx="7.5" cy="15.5" r="5.5" />
      <path d="m21 2-9.6 9.6" />
      <path d="m15.5 7.5 3 3L22 7l-3-3" />
    </svg>
    Добавить подписку
  </a>
</template>

<style lang="scss" scoped>
.key-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  width: 100%;
  margin-top: 12px;
  padding: 16px 22px;
  background: #fff;
  border: 1.5px solid var(--primary);
  border-radius: 12px;
  color: var(--primary);
  font-family: inherit;
  font-size: 15px;
  font-weight: 600;
  text-decoration: none;
  cursor: pointer;
  transition: all 0.15s ease;
}

.key-btn:hover {
  background: var(--primary);
  color: #fff;
  transform: translateY(-1px);
  box-shadow: 0 6px 18px rgba(201, 169, 97, 0.3);
}

.key-btn svg {
  width: 18px;
  height: 18px;
}

@media (max-width: 380px) {
  .key-btn {
    padding: 14px 18px;
    font-size: 14px;
  }
}

@media (hover: none) {
  .key-btn:hover {
    background: #fff;
    color: var(--primary);
    transform: none;
    box-shadow: none;
  }

  .key-btn:active {
    transform: scale(0.98);
    transition: transform 0.1s;
  }
}
</style>
