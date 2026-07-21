<script setup lang="ts">
import { useConfig } from '@/composables/useConfig';

const TITLE = 'Дисковое пространство для хранения записей с камер видеонаблюдения';
const SUBTITLE = 'Доступ активируется автоматически после успешной оплаты.';

const config = useConfig();
</script>

<template>
  <section class="storage-info" aria-label="Описание услуги">
    <div class="storage-info__top">
      <div class="storage-info__icon" aria-hidden="true">
        <svg viewBox="0 0 64 64" fill="none">
          <path
            d="M18.2 28.5C11.5 28.5 7 24.6 7 19.2C7 13.8 11.5 9.8 17 9.8C20.2 5.2 25.2 3 30.5 3C38.3 3 44.8 7.8 47.1 14.4C52.8 14.7 57 18.6 57 23.6C57 28.8 52.4 32.5 46.6 32.5H43"
            stroke="currentColor"
            stroke-width="3"
            stroke-linecap="round"
            stroke-linejoin="round"
          />
          <ellipse cx="31" cy="34" rx="14" ry="6" stroke="currentColor" stroke-width="3" />
          <path
            d="M17 34V43C17 46.3 23.3 49 31 49C38.7 49 45 46.3 45 43V34"
            stroke="currentColor"
            stroke-width="3"
          />
          <path
            d="M17 43V52C17 55.3 23.3 58 31 58C38.7 58 45 55.3 45 52V43"
            stroke="currentColor"
            stroke-width="3"
          />
        </svg>
      </div>

      <div>
        <h2 class="storage-info__title text-large">{{ TITLE }}</h2>
        <p class="storage-info__text text-small">{{ SUBTITLE }}</p>
      </div>
    </div>

    <div class="storage-info__provider text-xsmall">
      <svg viewBox="0 0 24 24" fill="none" aria-hidden="true">
        <path
          d="M12 2.5L19 5.4V10.6C19 15.1 16.2 19 12 21.3C7.8 19 5 15.1 5 10.6V5.4L12 2.5Z"
          stroke="currentColor"
          stroke-width="2"
          stroke-linejoin="round"
        />
        <path
          d="M9 11.8L11.1 13.9L15.4 9.5"
          stroke="currentColor"
          stroke-width="2"
          stroke-linecap="round"
          stroke-linejoin="round"
        />
      </svg>
      <span>Услугу оказывает организация {{ config.site.name }}</span>
    </div>
  </section>
</template>

<style lang="scss" scoped>
.storage-info {
  margin-top: 14px;
  padding: 16px 18px;
  background: var(--bg);
  border: 1px solid var(--border);
  border-radius: 12px;
  text-align: left;
}

.storage-info__top {
  display: grid;
  grid-template-columns: 64px minmax(0, 1fr);
  align-items: center;
  gap: 16px;
}

.storage-info__icon {
  width: 64px;
  height: 64px;
  display: grid;
  place-items: center;
  color: var(--primary-hover);
  background: radial-gradient(circle at 38% 30%, var(--primary-soft) 0%, #f7edd6 70%, #f4e8cc 100%);
  border-radius: 50%;
}

.storage-info__icon svg {
  width: 36px;
  height: 36px;
  display: block;
}

.storage-info__title {
  margin: 0 0 8px;
  font-weight: 600;
  line-height: 1.4;
  letter-spacing: -0.2px;
  color: var(--ink);
}

.storage-info__text {
  margin: 0;
  color: var(--ink-dim);
  line-height: 1.5;
}

.storage-info__provider {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  margin-top: 16px;
  padding-top: 16px;
  color: var(--ink-faint);
  border-top: 1px solid var(--border);
  line-height: 1.5;
  text-align: center;
}

.storage-info__provider svg {
  width: 18px;
  height: 18px;
  flex: 0 0 auto;
  color: var(--primary);
}

@media (max-width: 380px) {
  .storage-info {
    padding: 14px 16px;
  }

  .storage-info__top {
    grid-template-columns: 1fr;
    text-align: center;
  }

  .storage-info__icon {
    margin: 0 auto;
  }
}
</style>
