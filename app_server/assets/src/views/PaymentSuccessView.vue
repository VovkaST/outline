<script setup lang="ts">
import screenshotUrl from '@/assets/payment-success-app-screenshot.jpg';
import {
  Header,
  PaymentSuccessConnectionMode,
  PaymentSuccessStep,
  SuccessHero,
} from '@/components/tariffs';
import { useConfig } from '@/composables/useConfig';
import { onMounted, onUnmounted, watchEffect } from 'vue';

defineProps<{
  /** Идентификатор задачи (из URL) */
  taskId: string;
}>();

const config = useConfig();

watchEffect(() => {
  const baseTitle = config.value?.site?.title;
  document.title = baseTitle ? `${baseTitle} — Подписка активирована` : 'Подписка активирована';
});

onMounted(() => {
  document.body.classList.add('payment-success-scroll');
});

onUnmounted(() => {
  document.body.classList.remove('payment-success-scroll');
});
</script>

<template>
  <div class="page payment-success-view">
    <Header />

    <SuccessHero>
      <template #title>Подписка активирована</template>
      <template #description>
        Оплата прошла успешно. Осталась пара действий, чтобы VPN снова заработал.
      </template>
    </SuccessHero>

    <div class="section-title">Что делать дальше</div>

    <div class="screenshot">
      <img
        :src="screenshotUrl"
        alt="Скриншот приложения: кнопка отключения VPN и кнопка обновления подписки"
      />
      <div class="screenshot-caption">Так это выглядит в приложении</div>
    </div>

    <div class="steps">
      <PaymentSuccessStep :step-number="1">
        <template #title>Отключите VPN</template>
        <template #description>
          Если приложение сейчас подключено — нажмите «Стоп» или выключите соединение.
        </template>
      </PaymentSuccessStep>

      <PaymentSuccessStep :step-number="2">
        <template #title> Нажмите <span class="inline-chip">🔄 Обновить подписку</span> </template>
        <template #description>
          Кнопка находится в приложении. Она подтянет вашу новую оплату и активирует доступ.
        </template>
      </PaymentSuccessStep>

      <PaymentSuccessStep :step-number="3">
        <template #title>Выберите режим из списка внизу</template>
        <template #description>
          После обновления выберите подходящий вариант подключения:
        </template>
        <template #below>
          <div class="modes">
            <PaymentSuccessConnectionMode>
              <template #icon>🛜</template>
              <template #name>Wi-Fi</template>
              <template #description>Основной режим при подключении по Wi-Fi.</template>
            </PaymentSuccessConnectionMode>

            <PaymentSuccessConnectionMode>
              <template #icon>📶</template>
              <template #name>LTE Обход блокировок</template>
              <template #tag>only mobile</template>
              <template #description>
                Для обхода блокировок и при атаках БПЛА — когда мобильный интернет работает с
                ограничениями.
              </template>
            </PaymentSuccessConnectionMode>
          </div>
        </template>
      </PaymentSuccessStep>
    </div>

    <div class="footer-tip">
      <strong>Совет:</strong>
      если после обновления VPN не подключается — попробуйте переключиться между режимами Wi-Fi и
      LTE Обход блокировок. Один из них всегда работает в текущих условиях сети.
    </div>
  </div>
</template>

<style scoped lang="scss">
.page {
  max-width: 440px;
  width: 100%;
  margin: 0 auto;
  text-align: center;
}

.section-title {
  text-align: left;
  font-size: 13px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 1px;
  color: var(--ink-faint);
  margin-bottom: 14px;
  padding-left: 4px;
}

.screenshot {
  margin: 0 auto 24px;
  max-width: 280px;
  background: #fff;
  border: 1px solid var(--border);
  border-radius: 18px;
  padding: 10px 10px 12px;
  box-shadow: 0 6px 20px rgba(15, 17, 21, 0.08);
}

.screenshot img {
  display: block;
  width: 100%;
  height: auto;
  border-radius: 12px;
}

.screenshot-caption {
  margin-top: 10px;
  font-size: 12px;
  font-weight: 600;
  color: var(--ink-dim);
  text-align: center;
  letter-spacing: -0.1px;
}

.steps {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-bottom: 24px;
}

.modes {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.inline-chip {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  background: var(--primary-soft);
  border: 1px solid var(--primary);
  color: #5d4818;
  font-weight: 700;
  font-size: 12.5px;
  padding: 3px 9px;
  border-radius: 6px;
  margin: 0 2px;
  white-space: nowrap;
}

.footer-tip {
  margin-top: 28px;
  padding-top: 22px;
  border-top: 1px solid var(--border);
  font-size: 12px;
  color: var(--ink-faint);
  line-height: 1.55;
  text-align: center;
}

.footer-tip strong {
  color: var(--ink-dim);
  font-weight: 600;
}

@media (prefers-color-scheme: dark) {
  .screenshot {
    background: rgba(30, 41, 59, 0.98);
    border-color: rgba(148, 163, 184, 0.25);
  }

  .inline-chip {
    color: #f5e7c8;
    border-color: var(--primary);
    background: rgba(201, 169, 97, 0.15);
  }
}
</style>
