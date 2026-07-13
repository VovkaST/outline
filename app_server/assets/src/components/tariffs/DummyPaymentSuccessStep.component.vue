<script setup lang="ts">
defineProps<{
  stepNumber: number;
}>();
</script>

<template>
  <article class="dummy-payment-success-step">
    <div class="dummy-payment-success-step__number" aria-hidden="true">{{ stepNumber }}</div>

    <div>
      <h3 class="dummy-payment-success-step__title">
        <slot name="title" />
      </h3>
      <p class="dummy-payment-success-step__description">
        <slot name="description" />
      </p>
    </div>
  </article>
</template>

<style scoped lang="scss">
.dummy-payment-success-step {
  display: grid;
  grid-template-columns: 52px 1fr;
  gap: 17px;
  align-items: start;
  padding: 19px 21px;
  border-radius: 19px;
  background: linear-gradient(180deg, #2b3a4e, #1f2b3c);
  box-shadow: 0 10px 24px rgba(22, 34, 53, 0.13);
  color: #fff;
  text-align: left;
}

.dummy-payment-success-step__number {
  display: grid;
  width: 46px;
  height: 46px;
  place-items: center;
  border-radius: 50%;
  background: linear-gradient(145deg, #e1c36c, #bf9238);
  box-shadow: 0 8px 18px rgba(208, 170, 80, 0.27);
  font-size: 21px;
  font-weight: 800;
}

.dummy-payment-success-step__title {
  margin: 1px 0 5px;
  font-size: 19px;
  font-weight: 800;
  line-height: 1.25;
}

.dummy-payment-success-step__description {
  color: rgba(255, 255, 255, 0.9);
  font-size: 16px;
  line-height: 1.5;
}

.dummy-payment-success-step__description :deep(strong) {
  color: #f3cf72;
  white-space: nowrap;
}

@media (max-width: 640px) {
  .dummy-payment-success-step {
    grid-template-columns: 43px 1fr;
    gap: 13px;
    padding: 17px 16px;
    border-radius: 17px;
  }

  .dummy-payment-success-step__number {
    width: 40px;
    height: 40px;
    font-size: 18px;
  }

  .dummy-payment-success-step__title {
    font-size: 17px;
  }

  .dummy-payment-success-step__description {
    font-size: 15px;
  }
}
</style>
