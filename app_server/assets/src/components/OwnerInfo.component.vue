<script setup lang="ts">
const props = withDefaults(
  defineProps<{
    name?: boolean;
    itn?: boolean;
    regNumber?: boolean;
    account?: boolean;
    corrAccount?: boolean;
    bankCode?: boolean;
  }>(),
  {
    name: true,
    itn: true,
    regNumber: true,
    account: true,
    corrAccount: true,
    bankCode: true,
  },
);
</script>

<template>
  <div class="owner-info">
    <p v-if="name" class="info-item">ИП Абдулаев Мухаммад Мурадович</p>
    <p v-if="itn" class="info-item">ИНН: 057204730881</p>
    <p v-if="regNumber" class="info-item">ОГРН: 325050000001862</p>
    <p v-if="account" class="info-item">Расчетный счет: 40802810300007713048</p>
    <p v-if="corrAccount" class="info-item">Корреспондентский счет: 30101810145250000974</p>
    <p v-if="bankCode" class="info-item">БИК: 044525974</p>
  </div>
</template>

<style scoped lang="scss">
.info-item {
  margin-bottom: 0;
}
</style>
