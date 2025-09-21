<script setup lang="ts">
import { MainButton } from '@/components/tariffs';
import { ref } from 'vue';

const props = defineProps<{
  amount?: number;
}>();

const emit = defineEmits<{
  (e: 'submit', payload: any): void;
}>();

const amountValue = ref(props.amount);
const emailValue = ref(null);

const onFormSubmit = () => {
  emit('submit', { amount: amountValue.value, email: emailValue.value });
};
</script>
<template>
  <div class="pay-form-container">
    <h3 class="header">
      <slot name="header"></slot>
    </h3>
    <p class="description lead">
      <slot name="description"></slot>
    </p>
    <div class="form d-flex flex-column">
      <input name="amount" type="text" disabled placeholder="Сумма (₽)" v-model="amountValue" />
      <input name="email" type="email" placeholder="Email для чека" v-model="emailValue" />
      <MainButton @click="onFormSubmit">Оплатить сейчас</MainButton>
    </div>
    <p class="footnote">
      <slot name="footnote"></slot>
    </p>
  </div>
</template>
<style lang="scss" scoped>
.pay-form-container {
  margin-top: 24px;
  padding: 16px;
  border-radius: 10px;
  background: linear-gradient(180deg, rgba(35, 197, 82, 0.06), rgba(15, 107, 53, 0.04));
  border: 1px solid rgba(35, 197, 82, 0.06);

  .header {
    margin: 0 0 8px;
    font-size: 1.2rem;
    font-weight: 700;
  }

  .description {
    margin: 0 0 12px;
    color: var(--muted-color);
    font-size: 1rem;
  }

  .form {
    input {
      width: 100%;
      padding: 10px;
      border-radius: 8px;
      border: 1px solid rgba(255, 255, 255, 0.06);
      background: transparent;
      font-size: 0.8rem;
      color: #fff;
      margin-bottom: 8px;
    }
  }

  .footnote {
    margin-top: 18px;
    color: var(--muted-color);
    font-size: 0.85rem;
  }
}
</style>
