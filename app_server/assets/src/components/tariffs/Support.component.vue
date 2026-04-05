<script setup lang="ts">
import { computed, inject } from 'vue';
import { useConfig } from '@/composables/useConfig';

const config = useConfig();
const taskId = inject<string>('taskId', '');

const supportItems = computed(() =>
  config.value.supportItems.map((item) => ({
    ...item,
    url: item.url.replace('{task_id}', taskId),
  })),
);

const isWhatsApp = (url: string) => url.includes('wa.me') || url.includes('whatsapp.com');
</script>
<template>
  <div class="sup-box">
    <h3>Остались вопросы?</h3>
    <p>Напишите нам — ответим в течение нескольких минут</p>
    <a
      v-for="support in supportItems"
      :key="support.url"
      :href="support.url"
      class="sup-btn"
      :class="{ 'wa-btn': isWhatsApp(support.url) }"
      target="_blank"
    >
      <i v-if="isWhatsApp(support.url)" class="fab fa-whatsapp"></i>
      {{ support.text }}
    </a>
    <p class="sup-note">Работаем с 10:00 до 22:00 МСК</p>
  </div>
</template>
<style lang="scss" scoped>
.sup-box {
  background: var(--light);
  border: 1px solid var(--border);
  border-radius: 10px;
  padding: 18px 16px;
  text-align: center;
  margin-top: 15px;

  h3 {
    font-size: var(--lg);
    font-weight: 700;
    color: var(--t1);
    margin-bottom: 6px;
  }

  p:not(.sup-note) {
    font-size: var(--sm);
    font-weight: 400;
    color: var(--t2);
    line-height: 1.55;
    margin-bottom: 16px;
  }

  .sup-btn {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
    width: 100%;
    min-height: 48px;
    padding: 12px;
    background: var(--p);
    color: #fff;
    border: none;
    border-radius: 10px;
    font-size: var(--md);
    font-weight: 600;
    cursor: pointer;
    text-decoration: none;
    transition: opacity 0.15s;
    margin-bottom: 8px;

    &:active {
      opacity: 0.82;
    }

    &.wa-btn {
      background: #16a34a;
    }

    i {
      font-size: 17px;
    }
  }

  .sup-note {
    font-size: var(--xs);
    font-weight: 400;
    color: var(--t3);
    margin-top: 10px;
  }
}

@media (prefers-color-scheme: dark) {
  .sup-box {
    background: #2c2c2e;
    border-color: #3a3a3c;

    h3 {
      color: #f5f5f7;
    }

    p,
    .sup-note {
      color: #8e8e93;
    }
  }
}
</style>
