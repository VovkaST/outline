<script setup lang="ts">
import { computed } from 'vue';
import { Notice } from '@/components/ui';

const props = defineProps<{
  subscriptionUrl: string;
  translations: {
    title: string;
    desc: string;
    buttonText: string;
    note: string;
    wait: string;
    imagePaymentNote: string;
    imagePaymentDescription: string;
  };
}>();

const isWaiting = computed<boolean>(() => !props.subscriptionUrl);
</script>

<template>
  <div class="subscription-card">
    <div class="subscription-icon">
      <i class="fas fa-key"></i>
    </div>
    <div class="subscription-title">{{ translations.title }}</div>
    <div class="subscription-desc">{{ translations.desc }}</div>

    <div v-if="isWaiting" class="btn">
      {{ translations.wait }}
    </div>
    <a v-else :href="subscriptionUrl" class="btn" target="_blank" rel="noopener noreferrer">
      <i class="fas fa-external-link-alt"></i>
      {{ translations.buttonText }}
    </a>
  </div>

  <Notice notification-type="critical">{{ translations.note }}</Notice>

  <img
    src="/static/happ-subscription-payment.jpg"
    :alt="translations.imagePaymentNote"
    class="payment-image"
    id="paymentImage"
  />
  <div class="image-caption" id="imageCaption">{{ translations.imagePaymentDescription }}</div>
</template>

<style scoped lang="scss">
.subscription-card {
  background: linear-gradient(135deg, rgba(16, 185, 129, 0.15), rgba(16, 185, 129, 0.1));
  border: 2px solid rgba(16, 185, 129, 0.3);
  border-radius: 12px;
  padding: 20px;
  margin: 20px 0;
  text-align: center;
}

.subscription-icon {
  width: 52px;
  height: 52px;
  background: linear-gradient(135deg, var(--secondary), #0da271);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 14px;

  i {
    font-size: 22px;
    color: white;
  }
}

.subscription-title {
  font-size: 17px;
  font-weight: 700;
  color: var(--dark);
  margin-bottom: 6px;
}

.subscription-desc {
  font-size: 13px;
  color: var(--gray);
  margin-bottom: 16px;
  line-height: 1.4;
  -webkit-user-select: text;
  user-select: text;
}

.btn {
  display: block;
  width: 100%;
  padding: 16px;
  background: linear-gradient(135deg, var(--primary), var(--primary-dark));
  color: white;
  border: none;
  border-radius: 12px;
  font-size: 15px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  text-align: center;
  text-decoration: none;
  -webkit-tap-highlight-color: rgba(99, 102, 241, 0.2);
  user-select: none;
  position: relative;
  overflow: hidden;

  i {
    margin-right: 8px;
    font-size: 14px;
  }

  &:active {
    transform: scale(0.98);
  }

  &:hover {
    box-shadow: 0 8px 20px rgba(99, 102, 241, 0.35);
  }
}

.info-note {
  background: linear-gradient(135deg, rgba(99, 102, 241, 0.1), rgba(79, 70, 229, 0.1));
  border-left: 4px solid var(--primary);
  padding: 16px;
  border-radius: 10px;
  margin: 20px 0;
  font-size: 13px;
  color: var(--dark);
  line-height: 1.4;
  -webkit-user-select: text;
  user-select: text;

  i {
    color: var(--primary);
    margin-right: 8px;
    font-size: 14px;
  }
}

.payment-image {
  width: 100%;
  max-width: 100%;
  margin: 20px 0;
  display: block;
  border-radius: 12px;
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.2);
  border: 4px solid var(--light);
  height: auto;

  &:hover {
    transform: translateY(-3px);
    box-shadow: 0 12px 30px rgba(0, 0, 0, 0.3);
    transition: var(--transition);
  }
}

.image-caption {
  text-align: center;
  font-size: 12px;
  color: var(--gray);
  margin-top: 8px;
  margin-bottom: 20px;
  font-style: italic;
}

@media (prefers-color-scheme: dark) {
  .subscription-card {
    background: rgba(255, 255, 255, 0.1);
    border-color: rgba(16, 185, 129, 0.4);
  }

  .subscription-title {
    color: var(--dark);
  }

  .subscription-desc {
    color: rgba(255, 255, 255, 0.9);
  }

  .info-note {
    background: rgba(255, 255, 255, 0.1);
  }
}

@supports (-webkit-touch-callout: none) {
  .payment-image {
    max-height: 400px;
    object-fit: contain;
  }
}
</style>
