<script setup lang="ts">
import { TariffCard } from '@/components/tariffs';
import type { SiteConfigTariff } from '@/config/siteConfig.types';

withDefaults(
  defineProps<{
    tariffs: ReadonlyArray<SiteConfigTariff>;
    wait?: boolean;
  }>(),
  { wait: false },
);

const emit = defineEmits<{
  (e: 'actionClick', price: number): void;
}>();

const onActionClick = (price: number) => {
  emit('actionClick', price);
};
</script>

<template>
  <div class="buttons">
    <TariffCard
      v-for="tariff in tariffs"
      :key="`${tariff.period}-${tariff.price}`"
      :period="tariff.period"
      :price="tariff.price"
      :featured="tariff.featured"
      :disabled="wait"
      @actionClick="onActionClick"
    />
  </div>
</template>

<style lang="scss" scoped>
.buttons {
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin-bottom: 24px;
}
</style>
