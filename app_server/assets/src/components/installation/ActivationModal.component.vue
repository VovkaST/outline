<script setup lang="ts">
import type { Translations } from '@/utils/translations';

defineProps<{
  open: boolean;
  translations: Translations;
}>();

const emit = defineEmits<{
  (e: 'close'): void;
  (e: 'goInstall'): void;
}>();
</script>

<template>
  <div class="overlay" :class="{ active: open }" @click.self="emit('close')">
    <div
      class="offer-modal"
      role="dialog"
      aria-modal="true"
      :aria-label="translations.activate.modalTitle"
    >
      <div class="offer-head">
        <h2>{{ translations.activate.modalTitle }}</h2>
        <button class="close" type="button" @click="emit('close')">
          <svg
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2.5"
            stroke-linecap="round"
          >
            <line x1="18" y1="6" x2="6" y2="18" />
            <line x1="6" y1="6" x2="18" y2="18" />
          </svg>
        </button>
      </div>

      <div class="activate-body">
        <p class="activate-intro" v-html="translations.activate.introHtml"></p>

        <div class="ac-card">
          <div class="ac-card-head">
            <div class="ac-card-num">1</div>
            <div class="ac-card-title">{{ translations.activate.step1.title }}</div>
          </div>
          <p class="ac-card-desc" v-html="translations.activate.step1.descHtml"></p>

          <div class="happ-fig__photo" aria-hidden="true">
            <img
              src="/static/subscritpion-activate.jpeg"
              :alt="
                (translations.activate.step1 as any).imageAlt || translations.activate.step1.title
              "
              loading="lazy"
            />
            <span class="happ-fig__pulse" style="top: 78%; left: 93%"></span>
          </div>
        </div>

        <div class="ac-card">
          <div class="ac-card-head">
            <div class="ac-card-num">2</div>
            <div class="ac-card-title">{{ translations.activate.step2.title }}</div>
          </div>
          <p class="ac-card-desc" v-html="translations.activate.step2.descHtml"></p>

          <div class="happ-fig__photo" aria-hidden="true">
            <img
              src="/static/subscritpion-pay.jpeg"
              :alt="
                (translations.activate.step2 as any).imageAlt || translations.activate.step2.title
              "
              loading="lazy"
            />
            <span class="happ-fig__pulse" style="top: 78%; left: 5.7%"></span>
          </div>
        </div>

        <p class="activate-note">
          {{ translations.activate.noAppPrefix }}
          <button
            class="activate-link"
            type="button"
            @click="
              emit('close');
              emit('goInstall');
            "
          >
            {{ translations.activate.noAppLink }}
          </button>
        </p>
      </div>
    </div>
  </div>
</template>
