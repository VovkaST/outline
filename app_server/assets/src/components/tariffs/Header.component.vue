<script setup lang="ts"></script>

<template>
  <header>
    <div class="logo-container">
      <div class="logo-icon">
        <i class="fas fa-user-shield"></i>
      </div>
      <div class="logo">Halal <span>VPN</span></div>
    </div>
    <div class="title-container">
      <div class="main-title">🔒 Премиум защита</div>
      <div class="price-title">от 128₽/мес!</div>
    </div>

    <p class="text-medium">
      Полная анонимность и доступ ко всем ресурсам. Подключение за 60 секунд!
    </p>

    <div class="benefits">
      <div class="benefit text-small"><i class="fas fa-shield-alt"></i> 100% анонимность</div>
      <div class="benefit text-small"><i class="fas fa-bolt"></i> Макс. скорость</div>
      <div class="benefit text-small"><i class="fas fa-headset"></i> Поддержка 24/7</div>
    </div>
  </header>
</template>

<style scoped lang="scss">
header {
  padding: 20px 15px 15px;
  text-align: center;
  background: linear-gradient(135deg, var(--primary), #7c3aed);
  color: white;

  .logo-container {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 10px;
    margin-bottom: 10px;

    .logo-icon {
      width: 40px;
      height: 40px;
      background: rgba(255, 255, 255, 0.2);
      border-radius: 10px;
      display: flex;
      align-items: center;
      justify-content: center;
      border: 2px solid rgba(255, 255, 255, 0.3);

      i {
        font-size: 1.3rem;
        color: #f59e0b;
      }
    }

    .logo {
      font-size: 1.7rem;
      font-weight: 800;
      color: white;
    }

    .logo span {
      color: #f59e0b;
    }
  }

  .title-container {
    margin-bottom: 8px;

    .main-title {
      font-size: 1.4rem;
      font-weight: 800;
      line-height: 1.2;
      margin-bottom: 4px;
    }

    .price-title {
      font-size: 1.6rem;
      font-weight: 800;
      line-height: 1.1;
      color: #f59e0b;
    }
  }

  .benefits {
    display: flex;
    justify-content: center;
    gap: 8px;
    margin-top: 12px;
    flex-wrap: wrap;

    .benefit {
      display: flex;
      align-items: center;
      gap: 4px;
      background: rgba(255, 255, 255, 0.15);
      padding: 4px 8px;
      border-radius: 12px;
      white-space: nowrap;

      i {
        color: #f59e0b;
      }
    }
  }
}

@media (max-width: 768px) {
  header {
    padding: 25px 15px 12px;
  }

  .logo {
    font-size: 1.6rem;
    margin-bottom: 10px;
  }

  h1 {
    font-size: 1.5rem;
    margin-bottom: 6px;
  }

  .subtitle {
    font-size: 0.9rem;
  }
}

@media (max-width: 480px) {
  .header {
    padding: 20px 10px 10px;
  }

  .logo {
    font-size: 1.4rem;
  }

  h1 {
    font-size: 1.3rem;
  }
}
</style>
