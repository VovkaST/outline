<script setup lang="ts">
const props = defineProps<{
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
    >
      RU
    </button>
    <button
      class="lang-btn"
      :class="{ active: currentLanguage === 'en' }"
      @click="switchLanguage('en')"
    >
      EN
    </button>
  </div>
</template>

<style scoped lang="scss">
.language-switcher {
  position: fixed;
  top: 15px;
  right: 15px;
  z-index: 100;
  display: flex;
  gap: 8px;
}

.lang-btn {
  background: rgba(255, 255, 255, 0.95);
  border: none;
  border-radius: 20px;
  padding: 8px 16px;
  font-size: 12px;
  font-weight: 600;
  color: var(--primary);
  cursor: pointer;
  transition: all 0.2s ease;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);

  &:hover {
    background: white;
    transform: translateY(-1px);
    box-shadow: 0 6px 16px rgba(0, 0, 0, 0.15);
  }

  &.active {
    background: var(--primary);
    color: white;
  }
}
</style>
