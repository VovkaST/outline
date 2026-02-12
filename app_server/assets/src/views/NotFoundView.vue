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
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: var(--dark);
  text-align: center;
}

.container {
  width: 100%;
  max-width: 400px;
  margin: 0 auto;
}

.card {
  background: rgba(255, 255, 255, 0.98);
  border-radius: 16px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.15);
  padding: 20px;
}

.main-title {
  font-size: 1.4rem;
  font-weight: 800;
  margin-bottom: 4px;
}

.text-medium {
  font-size: 1rem;
  margin-top: 5px;
}

.text-small {
  font-size: 0.9rem;
  margin-top: 10px;
}
</style>
