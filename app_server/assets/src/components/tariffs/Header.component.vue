<script setup lang="ts">
import { useConfig } from '@/composables/useConfig';

const config = useConfig();
</script>

<template>
  <header class="hdr">
    <div class="logo-row">
      <div class="logo-icon"><i class="fas fa-user-shield"></i></div>
      <div class="logo-name">
        {{ config.site.name.split(' ')[0] }} <span>{{ config.site.name.split(' ')[1] }}</span>
      </div>
    </div>
    <div class="hdr-title">🔒 Премиум защита</div>
    <div class="hdr-price">от 128₽ в месяц</div>
    <p class="hdr-sub">
      Полная анонимность и доступ ко всем ресурсам. Работает в России. Подключение за 60 секунд!
    </p>
    <div class="chips">
      <span class="chip">100% анонимность</span>
      <span class="chip">Макс. скорость</span>
      <span class="chip">Работает в РФ</span>
    </div>
  </header>
</template>

<style scoped lang="scss">
.hdr {
  background: linear-gradient(160deg, #6d28d9 0%, #4c1d95 100%);
  color: #fff;
  padding: 24px 16px 20px;
  text-align: center;
  border-radius: 16px 16px 0 0;

  .logo-row {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 9px;
    margin-bottom: 14px;

    .logo-icon {
      width: 36px;
      height: 36px;
      min-width: 36px;
      background: rgba(255, 255, 255, 0.15);
      border-radius: 9px;
      display: flex;
      align-items: center;
      justify-content: center;
      border: 1px solid rgba(255, 255, 255, 0.2);

      i {
        font-size: 16px;
        color: var(--gold);
      }
    }

    .logo-name {
      font-size: 20px;
      font-weight: 700;
      letter-spacing: -0.3px;

      span {
        color: var(--gold);
      }
    }
  }

  .hdr-title {
    font-size: var(--md);
    font-weight: 400;
    color: rgba(255, 255, 255, 0.75);
    margin-bottom: 10px;
  }

  .hdr-price {
    font-size: 30px;
    font-weight: 700;
    color: var(--gold);
    letter-spacing: -0.8px;
    line-height: 1.1;
    margin-bottom: 12px;
  }

  .hdr-sub {
    font-size: var(--sm);
    font-weight: 400;
    color: rgba(255, 255, 255, 0.65);
    line-height: 1.55;
    margin-bottom: 16px;
  }

  .chips {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    gap: 6px;

    .chip {
      background: rgba(255, 255, 255, 0.12);
      border: 1px solid rgba(255, 255, 255, 0.18);
      padding: 5px 12px;
      border-radius: 20px;
      font-size: var(--xs);
      font-weight: 500;
      color: rgba(255, 255, 255, 0.95);
    }
  }
}

@media (max-width: 360px) {
  .hdr-price {
    font-size: 26px;
  }
}
</style>
