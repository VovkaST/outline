<script setup lang="ts">
import type { Translations } from '@/utils/translations';
import StepCard from './StepCard.component.vue';

const props = defineProps<{
  translations: Translations;
  stepDone: number;
  isSubscriptionReady: boolean;
  canDoStep2: boolean;
  canDoStep3: boolean;
}>();

const emit = defineEmits<{
  (e: 'step1'): void;
  (e: 'step2'): void;
  (e: 'step3'): void;
}>();

const stepClass = (step: number) => {
  if (step <= props.stepDone) return 'done' as const;
  if (step === props.stepDone + 1) return 'active' as const;
  return 'locked' as const;
};

const step2Desc = () => {
  if (props.stepDone < 1) return props.translations.welcome.steps.step2.descNeedInstall;
  if (!props.isSubscriptionReady) return props.translations.welcome.steps.step2.descWaitingKey;
  return props.translations.welcome.steps.step2.descReady;
};
</script>

<template>
  <div class="screen welcome active">
    <div class="welcome">
      <div class="logo-lg" aria-label="Halal VPN">
        <div class="logo-lg-mark">H</div>
        {{ translations.brand.nameFirst }} <span>{{ translations.brand.nameSecond }}</span>
      </div>

      <p class="screen-sub">{{ translations.welcome.subtitle }}</p>

      <StepCard
        :step-number="1"
        :label="translations.welcome.steps.step1.label"
        :title="translations.welcome.steps.step1.title"
        :desc="translations.welcome.steps.step1.desc"
        :state="stepClass(1)"
        @click="emit('step1')"
      />

      <StepCard
        :step-number="2"
        :label="translations.welcome.steps.step2.label"
        :title="translations.welcome.steps.step2.title"
        :desc="step2Desc()"
        :state="stepClass(2)"
        :disabled="!canDoStep2"
        @click="emit('step2')"
      >
        <template v-if="stepDone >= 1 && !isSubscriptionReady" #descSuffix>
          <span class="step-wait" aria-hidden="true">
            <span class="dot"></span>
            <span class="dot"></span>
            <span class="dot"></span>
          </span>
        </template>
      </StepCard>

      <StepCard
        :step-number="3"
        :label="translations.welcome.steps.step3.label"
        :title="translations.welcome.steps.step3.title"
        :desc="translations.welcome.steps.step3.desc"
        :state="stepClass(3)"
        :disabled="!canDoStep3"
        @click="emit('step3')"
      />
    </div>
  </div>
</template>
