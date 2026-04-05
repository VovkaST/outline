<script setup lang="ts">
import {
  PaymentInfoComponent,
  Support,
  TariffCard,
  TariffFeature,
} from '@/components/tariffs';
import { ref } from 'vue';

const props = withDefaults(
  defineProps<{
    wait?: boolean;
  }>(),
  { wait: false },
);

const selectedPrice = ref<number>(0);

const isTariffSelected = (price: number): boolean => props.wait && selectedPrice.value === price;

const emit = defineEmits<{
  (e: 'actionClick', price: number): void;
}>();

const onActionClick = (price: number) => {
  selectedPrice.value = price;
  emit('actionClick', price);
};
</script>
<template>
  <div class="tariffs-container">
    <div class="tariffs">
      <TariffCard
        :price="19900"
        :old-price="24900"
        :per-month="19900"
        :economy="50"
        :wait="isTariffSelected(19900)"
        discount="-20%"
        @actionClick="onActionClick"
      >
        <template #term> 1 месяц </template>
        <template #features>
          <TariffFeature bold>Полная анонимность</TariffFeature>
          <TariffFeature>Высокая скорость</TariffFeature>
          <TariffFeature>Безлимитный трафик</TariffFeature>
          <TariffFeature>Поддержка 24/7</TariffFeature>
        </template>
        <template #buttonText> 🔥 Выбрать тариф </template>
        <template #guarantee> Попробуй без риска </template>
      </TariffCard>

      <TariffCard
        :price="49900"
        :old-price="74700"
        :per-month="16800"
        :economy="248"
        :wait="isTariffSelected(49900)"
        discount="-30%"
        @actionClick="onActionClick"
      >
        <template #term> 3 месяца </template>
        <template #features>
          <TariffFeature bold>Всё из тарифа 1 месяц</TariffFeature>
          <TariffFeature>Приоритетная поддержка</TariffFeature>
          <TariffFeature>Резервные серверы</TariffFeature>
          <TariffFeature>Авто-подключение</TariffFeature>
        </template>
        <template #buttonText> 🚀 Выбрать тариф </template>
        <template #guarantee> Популярный выбор </template>
      </TariffCard>

      <TariffCard
        :price="89900"
        :old-price="179400"
        :per-month="12800"
        :economy="895"
        :wait="isTariffSelected(89900)"
        discount="-50%"
        isPopular
        @actionClick="onActionClick"
      >
        <template #term> 6 месяцев + 1 в подарок </template>
        <template #features>
          <TariffFeature bold>Всё из тарифа 3 месяца</TariffFeature>
          <TariffFeature>+1 месяц БЕСПЛАТНО</TariffFeature>
          <TariffFeature>Выделенный канал</TariffFeature>
          <TariffFeature>Приоритет скорости</TariffFeature>
        </template>
        <template #buttonText> 💎 Выбрать выгоду </template>
        <template #guarantee> Лучшее предложение </template>
      </TariffCard>

      <TariffCard
        :price="199900"
        :old-price="358800"
        :per-month="13300"
        :economy="1589"
        :wait="isTariffSelected(199900)"
        discount="-45%"
        @actionClick="onActionClick"
      >
        <template #term> 12 месяцев + 3 в подарок </template>
        <template #features>
          <TariffFeature bold>Всё из премиум-тарифа</TariffFeature>
          <TariffFeature>+3 месяца БЕСПЛАТНО</TariffFeature>
          <TariffFeature>Максимальная скорость</TariffFeature>
          <TariffFeature>Премиум поддержка</TariffFeature>
        </template>
        <template #buttonText> 🛡 Максимальная защита </template>
        <template #guarantee> Для профессионалов </template>
      </TariffCard>
    </div>
    <PaymentInfoComponent />
    <Support />
  </div>
</template>

<style lang="scss" scoped>
.tariffs-container {
  padding: 16px 12px;

  .tariffs {
    display: flex;
    flex-direction: column;
    gap: 14px;
    margin-bottom: 16px;
  }
}

@media (min-width: 768px) {
  .tariffs-container {
    .tariffs {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
      gap: 20px;
    }
  }
}
</style>
