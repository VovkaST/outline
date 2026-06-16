<script setup lang="ts">
defineProps<{
  currentLanguage: 'ru' | 'en';
}>();

const emit = defineEmits<{
  (e: 'languageChange', lang: 'ru' | 'en'): void;
}>();

const switchLanguage = (lang: 'ru' | 'en') => {
  emit('languageChange', lang);
};
</script>

<template>
  <div class="language-switcher">
    <button
      class="lang-btn"
      :class="{ active: currentLanguage === 'ru' }"
      @click="switchLanguage('ru')"
      type="button"
    >
      RU
    </button>
    <button
      class="lang-btn"
      :class="{ active: currentLanguage === 'en' }"
      @click="switchLanguage('en')"
      type="button"
    >
      EN
    </button>
  </div>
</template>

<style scoped lang="scss">
.language-switcher {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 4px;
  border-radius: 12px;
  border: 1px solid var(--border);
  background: var(--bg-soft);
}

.lang-btn {
  appearance: none;
  border: none;
  border-radius: 10px;
  padding: 6px 10px;
  font-size: 12px;
  font-weight: 600;
  color: var(--ink-dim);
  cursor: pointer;
  transition: all 0.15s ease;
  background: transparent;

  &:hover {
    color: var(--ink);
  }

  &.active {
    background: var(--primary);
    color: white;
  }
}
</style>
