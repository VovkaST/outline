<script setup lang="ts">
import { computed } from 'vue';
import { useRoute } from 'vue-router';

const route = useRoute();
const fullPath = computed(() => `${window.location.origin}${route.fullPath}`);
</script>

<template>
  <div class="page">
    <div class="code">404</div>
    <p class="title">Страница не найдена</p>
    <p class="text">К сожалению, эта страница не существует.</p>
    <p class="path">
      Вы пытались получить доступ к: <strong>{{ fullPath }}</strong>
    </p>
  </div>
</template>

<style scoped lang="scss">
.page {
  max-width: 420px;
  width: 100%;
  text-align: center;
  margin: 0 auto;
  color: var(--ink);
}

.code {
  font-size: 72px;
  font-weight: 800;
  letter-spacing: -2px;
  line-height: 1;
  color: var(--primary);
  margin-bottom: 12px;
}

.title {
  font-size: 18px;
  font-weight: 700;
  margin-bottom: 8px;
  letter-spacing: -0.2px;
  color: var(--ink);
}

.text {
  font-size: 14px;
  color: var(--ink-dim);
  line-height: 1.55;
  margin-bottom: 20px;
}

.path {
  font-size: 12px;
  color: var(--ink-dim);
  background: var(--bg-soft);
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 12px 14px;
  word-break: break-all;
  text-align: left;
  line-height: 1.5;
}

.path strong {
  color: var(--ink);
  font-weight: 600;
}

@media (max-width: 380px) {
  .code {
    font-size: 60px;
  }

  .title {
    font-size: 16px;
  }
}
</style>
