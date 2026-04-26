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
</script>

<template>
  <div class="logo">
    <div class="logo-mark">{{ logoLetter }}</div>
    {{ nameParts.primary }}
    <span v-if="nameParts.accent">&nbsp;{{ nameParts.accent }}</span>
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
  background: linear-gradient(135deg, #d4b876, #a8893f);
  border-radius: 10px;
  display: grid;
  place-items: center;
  color: #fff;
  font-weight: 800;
  font-size: 17px;
  box-shadow: 0 4px 14px rgba(201, 169, 97, 0.4);
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
