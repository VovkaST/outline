<script setup lang="ts">
import {
  DummyPaymentSuccessStep,
  DummyPriceBadge,
  DummyStorageFlowDiagram,
  DummySuccessHero,
  Header,
} from '@/components/tariffs';
import { useConfig } from '@/composables/useConfig';
import { decimalNumberFormat } from '@/utils';
import { computed, watchEffect } from 'vue';

defineProps<{
  /** Идентификатор задачи (из URL) */
  taskId: string;
}>();

const config = useConfig();

const tariffPrice = computed<number>(() => config.value.tariffs[0]?.price ?? 0);

const formattedPrice = computed<string>(() =>
  decimalNumberFormat({ value: tariffPrice.value, fractionDigits: 0 }),
);

watchEffect(() => {
  const baseTitle = config.value?.site?.title;
  document.title = baseTitle ? `${baseTitle} — Оплата прошла успешно` : 'Оплата прошла успешно';
});
</script>

<template>
  <div class="page payment-success-dummy">
    <Header />

    <DummySuccessHero>
      <template #title>Оплата прошла успешно</template>
      <template #description>
        Облачное хранилище для записей с камер видеонаблюдения активировано. Теперь архив будет
        храниться в облаке вместо флэшки.
      </template>
      <template #badge>
        <DummyPriceBadge :price="tariffPrice" />
      </template>
    </DummySuccessHero>

    <h2 class="section-title">Что делать дальше</h2>

    <DummyStorageFlowDiagram />

    <section class="steps" aria-label="Дальнейшие действия">
      <DummyPaymentSuccessStep :step-number="1">
        <template #title>Подключите нужную камеру</template>
        <template #description>
          Выберите камеру, для которой необходимо хранение записей в облаке.
        </template>
      </DummyPaymentSuccessStep>

      <DummyPaymentSuccessStep :step-number="2">
        <template #title>Архив сохраняется в облако</template>
        <template #description>
          После оплаты записи с камеры будут храниться в облачном хранилище вместо флэшки.
        </template>
      </DummyPaymentSuccessStep>

      <DummyPaymentSuccessStep :step-number="3">
        <template #title>Пользуйтесь архивом</template>
        <template #description>
          Смотрите и выгружайте записи при необходимости. Стоимость хранения —
          <strong>{{ formattedPrice }} ₽</strong> в месяц за одну камеру.
        </template>
      </DummyPaymentSuccessStep>
    </section>

    <footer class="footer-tip">
      <strong>Совет:</strong> облачное хранение помогает сохранить записи в безопасности и получить
      доступ к архиву без использования флэшки.
    </footer>
  </div>
</template>

<style scoped lang="scss">
.page {
  width: min(100%, 700px);
  margin: 0 auto;
  text-align: center;
}

.section-title {
  margin: 31px 4px 15px;
  color: #8c98a7;
  font-size: 16px;
  font-weight: 800;
  letter-spacing: 1.4px;
  text-transform: uppercase;
  text-align: left;
}

.steps {
  display: grid;
  gap: 14px;
  margin-top: 19px;
}

.footer-tip {
  margin-top: 25px;
  padding: 20px 12px 0;
  border-top: 1px solid #d5dbe2;
  color: #8794a5;
  font-size: 15px;
  font-weight: 500;
  line-height: 1.6;
  text-align: center;
}

.footer-tip strong {
  color: #758294;
}

@media (max-width: 640px) {
  .section-title {
    margin-top: 26px;
    font-size: 14px;
  }

  .footer-tip {
    padding-inline: 4px;
    font-size: 14px;
  }
}
</style>
