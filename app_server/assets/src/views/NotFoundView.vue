<script setup lang="ts">
import { useRoute } from 'vue-router';
import { computed } from 'vue';

const route = useRoute();
const fullPath = computed(() => `${window.location.origin}${route.fullPath}`);
</script>

<template>
  <div class="not-found">
    <div class="container">
      <div class="card">
        <p class="main-title">404 - Страница не найдена</p>
        <p class="text-medium">К сожалению, эта страница не существует.</p>
        <p class="text-small">
          Вы пытались получить доступ к: <strong>{{ fullPath }}</strong>
        </p>
      </div>
    </div>
  </div>
</template>

<style scoped>
.not-found {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  background: #3B0764;
  color: var(--t1);
  text-align: center;
}

.container {
  width: 100%;
  max-width: 400px;
  margin: 0 auto;
}

.card {
  background: #fff;
  border-radius: 16px;
  box-shadow: 0 12px 40px rgba(0, 0, 0, 0.22);
  padding: 24px 20px;
}

.main-title {
  font-size: 1.4rem;
  font-weight: 800;
  margin-bottom: 8px;
  color: var(--p);
}

.text-medium {
  font-size: var(--md);
  margin-top: 5px;
  color: var(--t1);
}

.text-small {
  font-size: var(--sm);
  margin-top: 12px;
  color: var(--t2);
}
</style>
