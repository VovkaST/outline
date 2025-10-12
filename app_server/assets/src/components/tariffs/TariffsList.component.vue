<script setup lang="ts">
import { TariffCard, TariffFeature, PaymentInfoComponent } from '@/components/tariffs';
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
        :wait="isTariffSelected(19900)"
        @actionClick="onActionClick"
      >
        <template v-slot:term> 1 месяц </template>
        <template v-slot:features>
          <TariffFeature>Полный доступ к сервису</TariffFeature>
          <TariffFeature>Техническая поддержка</TariffFeature>
        </template>
      </TariffCard>

      <TariffCard
        :price="49900"
        :old-price="59700"
        :per-month="16600"
        :wait="isTariffSelected(49900)"
        @actionClick="onActionClick"
      >
        <template v-slot:term> 3 месяца </template>
        <template v-slot:features>
          <TariffFeature>Полный доступ к сервису</TariffFeature>
          <TariffFeature>Техническая поддержка</TariffFeature>
        </template>
      </TariffCard>

      <TariffCard
        :price="89900"
        :old-price="139300"
        :per-month="14900"
        :wait="isTariffSelected(89900)"
        isPopular
        @actionClick="onActionClick"
      >
        <template v-slot:term> 6 месяцев + 1 в подарок </template>
        <template v-slot:features>
          <TariffFeature>Полный доступ к сервису</TariffFeature>
          <TariffFeature>Техническая поддержка</TariffFeature>
          <TariffFeature>+1 месяц бесплатно</TariffFeature>
        </template>
      </TariffCard>

      <TariffCard
        :price="199900"
        :old-price="208500"
        :per-month="13300"
        :wait="isTariffSelected(199900)"
        @actionClick="onActionClick"
      >
        <template v-slot:term> 12 месяцев + 3 в подарок </template>
        <template v-slot:features>
          <TariffFeature>Полный доступ к сервису</TariffFeature>
          <TariffFeature>Техническая поддержка</TariffFeature>
          <TariffFeature>+3 месяца бесплатно</TariffFeature>
        </template>
      </TariffCard>
    </div>
    <PaymentInfoComponent />
  </div>
</template>
<style lang="scss" scoped>
.tariffs-container {
  padding: 25px 15px;
  opacity: 1;
  transform: translateY(0px);
  transition:
    opacity 0.5s,
    transform 0.5s;

  .tariffs {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 20px;
    margin-bottom: 20px;
  }
}

@media (max-width: 768px) {
  .tariffs-container {
    padding: 20px 10px;
  }

  .tariffs {
    grid-template-columns: 1fr;
    gap: 15px;
  }
}

@media (max-width: 480px) {
  .tariff {
    padding: 18px 12px;
  }
}
</style>
