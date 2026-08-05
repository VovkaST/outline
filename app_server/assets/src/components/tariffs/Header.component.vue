<script setup lang="ts">
import { useConfig } from '@/composables/useConfig';
import { computed } from 'vue';

const config = useConfig();

const nameParts = computed<{ primary: string; accent: string }>(() => {
  const name = config.value.site.name ?? '';
  const [primary = '', ...rest] = name.split(' ');
  return { primary, accent: rest.join(' ') };
});

const logoLetter = computed<string>(() => (nameParts.value.primary[0] ?? '').toUpperCase());
const isBabochkiTheme = computed<boolean>(() => config.value.site.theme === 'babochki');
</script>

<template>
  <div class="logo">
    <div class="logo-mark" :class="{ 'logo-mark--butterfly': isBabochkiTheme }">
      <svg
        v-if="isBabochkiTheme"
        class="logo-butterfly"
        viewBox="0 0 64 64"
        fill="none"
        aria-hidden="true"
      >
        <path
          d="M30.5 31.5C25.5 18.5 17 9.5 10.5 13.5C3.5 18 8.5 29.5 20.5 34C11 36 8 44 13.5 49C19.5 54.5 27.5 45.5 31 36.5L30.5 31.5Z"
          fill="currentColor"
        />
        <path
          d="M33.5 31.5C38.5 18.5 47 9.5 53.5 13.5C60.5 18 55.5 29.5 43.5 34C53 36 56 44 50.5 49C44.5 54.5 36.5 45.5 33 36.5L33.5 31.5Z"
          fill="currentColor"
        />
        <path
          d="M32 25.5C35.5 30 35.5 39.5 32 46C28.5 39.5 28.5 30 32 25.5Z"
          fill="currentColor"
        />
        <path
          d="M30.5 26C27.5 21.5 25 19.5 22.5 18M33.5 26C36.5 21.5 39 19.5 41.5 18"
          stroke="currentColor"
          stroke-width="2.5"
          stroke-linecap="round"
        />
      </svg>

      <template v-else>{{ logoLetter }}</template>
    </div>

    {{ nameParts.primary }}<span v-if="nameParts.accent">{{ nameParts.accent }}</span>
  </div>
</template>

<style scoped lang="scss">
.logo {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  font-size: 24px;
  font-weight: 700;
  letter-spacing: -0.4px;
  margin-bottom: 24px;
  color: var(--ink);
}

.logo-mark {
  width: 38px;
  height: 38px;
  background: var(--logo-mark-background);
  border-radius: 10px;
  display: grid;
  place-items: center;
  color: var(--logo-mark-color);
  font-weight: 800;
  font-size: 17px;
  box-shadow: var(--logo-mark-shadow);
}

.logo span {
  color: var(--primary);
}

@media (max-width: 380px) {
  .logo {
    font-size: 22px;
    margin-bottom: 28px;
  }

  .logo-mark {
    width: 34px;
    height: 34px;
    font-size: 15px;
  }
}
</style>
