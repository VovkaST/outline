<script setup lang="ts">
import { useConfig } from '@/composables/useConfig';

const config = useConfig();
</script>
<template>
  <div class="support-section">
    <div class="support-title text-medium">💬 Остались вопросы? Напишите нам!</div>
    <a
      v-for="support in config.supportItems"
      :href="support.url"
      class="email-btn text-medium"
      target="_blank"
    >
      {{ support.text }}
    </a>
    <p class="text-xsmall" style="margin-top: 8px; color: #6b7280">Ответим в течение 24 часов</p>
  </div>
</template>
<style lang="scss" scoped>
.support-section {
  text-align: center;
  padding: 16px 12px;
  background: var(--light);
  border-radius: 10px;
  margin-top: 15px;
  border: 1px solid #e5e7eb;

  .support-title {
    margin-bottom: 10px;
    color: var(--dark);
    font-weight: 600;
    line-height: 1.3;
    padding: 0 5px;
  }

  .email-btn {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 12px 20px;
    background: var(--primary);
    color: white;
    text-decoration: none;
    border-radius: 10px;
    font-weight: 700;
    transition: all 0.3s ease;
    box-shadow: 0 4px 12px rgba(139, 92, 246, 0.3);
    min-height: 44px;
  }

  .email-btn:active {
    transform: scale(0.96);
    box-shadow: 0 2px 8px rgba(139, 92, 246, 0.4);
  }

  .email-btn i {
    font-size: 1.1rem;
  }
}
</style>
