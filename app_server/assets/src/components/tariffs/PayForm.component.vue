<script setup lang="ts">
import { MainButton, InputText } from '@/components/tariffs';
import { validateEmail } from '@/utils';
import { computed, reactive } from 'vue';

type Errors = {
  amount?: string[];
  email?: string[];
};

const props = withDefaults(
  defineProps<{
    wait?: boolean;
  }>(),
  {
    wait: false,
  },
);

const errors = reactive<Errors>({});

const emit = defineEmits<{
  (e: 'submit', payload: any): void;
}>();

const amount = defineModel('amount');
const email = defineModel('email');

const allowSubmit = computed<boolean>(() => !!amount.value && !props.wait);

const validate = (): Errors => {
  if (!amount.value) {
    errors['amount'] = ['Сумма обязательна для заполнения'];
  } else errors['amount'] = [];
  if (email.value && !validateEmail(email.value)) {
    errors['email'] = ['Неверный формат почты'];
  } else errors['email'] = [];
  return errors;
};

const isValid = (): boolean => {
  return !Object.values(validate()).filter((i) => i.length).length;
};

const onFormSubmit = () => {
  if (!isValid()) return;
  emit('submit', { amount: amount.value, email: email.value });
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
      <InputText
        class="mb-2"
        disabled
        placeholder="Сумма (₽)"
        v-model="amount"
        :errors="errors['amount']"
      />
      <InputText
        type="email"
        class="mb-2"
        placeholder="Email для чека"
        v-model="email"
        :errors="errors['email']"
      />
      <MainButton
        @click="() => (allowSubmit ? onFormSubmit() : null)"
        :disabled="canSubmit"
        :wait="wait"
      >
        Оплатить сейчас
      </MainButton>
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
