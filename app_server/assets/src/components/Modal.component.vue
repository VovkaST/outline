<script setup lang="ts">
import { ModalProvider } from '@/components';
import { ref, watch } from 'vue';

const props = defineProps<{
  title?: string;
  closeOnEsc?: boolean;
  closeOnClickOutside?: boolean;
}>();

const showModal = defineModel<boolean>('show', { default: false });
const isFirstClick = ref<boolean>(true);

const emit = defineEmits<{
  (e: 'close'): void;
}>();

const onShowModal = () => {
  document.addEventListener('keydown', handleKeydown);
  document.addEventListener('click', handleClickOutside);
};

const onCloseModal = () => {
  document.removeEventListener('keydown', handleKeydown);
  document.removeEventListener('click', handleClickOutside);
  isFirstClick.value = true;
  emit('close');
};

const handleKeydown = (e: KeyboardEvent) => {
  if (props.closeOnEsc && e.key === 'Escape') {
    onCloseModal();
  }
};

const handleClickOutside = (e: MouseEvent) => {
  if (isFirstClick.value) {
    isFirstClick.value = false;
  } else if (
    props.closeOnClickOutside &&
    e.target instanceof HTMLElement &&
    !e.target.closest('.modal-content')
  ) {
    onCloseModal();
  }
};

watch(
  () => showModal.value,
  (value) => {
    value ? onShowModal() : onCloseModal();
  },
);
</script>

<template>
  <ModalProvider :show-modal="showModal">
    <div class="modal-overlay">
      <div class="modal-content">
        <div v-if="title" class="modal-header">
          <h3>{{ title }}</h3>
          <button class="close-btn" type="button" @click="onCloseModal">
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

        <div class="modal-body">
          <slot name="body" />
        </div>

        <footer v-if="$slots.footer" class="modal-footer">
          <slot name="footer" />
        </footer>
      </div>
    </div>
  </ModalProvider>
</template>

<style scoped lang="scss">
.modal {
  &-overlay {
    position: fixed;
    inset: 0;
    background: rgba(15, 17, 21, 0.5);
    backdrop-filter: blur(4px);
    -webkit-backdrop-filter: blur(4px);
    z-index: 1000;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 20px;
    padding-top: max(20px, env(safe-area-inset-top));
    padding-bottom: max(20px, env(safe-area-inset-bottom));
    overscroll-behavior: contain;
  }

  &-content {
    background: #fff;
    border-radius: 16px;
    max-width: 720px;
    width: 100%;
    max-height: calc(100dvh - 40px);
    display: flex;
    flex-direction: column;
    overflow: hidden;
    box-shadow: 0 12px 40px rgba(15, 17, 21, 0.18);
    animation: slide 0.25s ease;
  }

  &-header {
    padding: 18px 22px;
    border-bottom: 1px solid var(--border);
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-shrink: 0;
    gap: 12px;
    background: #fff;

    h3 {
      margin: 0;
      font-size: 16px;
      font-weight: 700;
      letter-spacing: -0.2px;
      line-height: 1.3;
      color: var(--ink);
      text-align: left;
      flex: 1;
    }

    .close-btn {
      width: 32px;
      height: 32px;
      background: var(--bg-soft);
      border: none;
      border-radius: 8px;
      cursor: pointer;
      display: grid;
      place-items: center;
      color: var(--ink-dim);
      transition: all 0.15s;
      padding: 0;
      flex-shrink: 0;

      svg {
        width: 16px;
        height: 16px;
      }

      &:hover {
        background: #eef0f3;
        color: var(--ink);
      }
    }
  }

  &-body {
    overflow-y: auto;
    -webkit-overflow-scrolling: touch;
    overscroll-behavior: contain;
    padding: 20px 22px 24px;
    padding-bottom: max(24px, env(safe-area-inset-bottom));
    font-size: 13px;
    line-height: 1.6;
    color: var(--ink-dim);
    text-align: left;
    word-wrap: break-word;
    overflow-wrap: break-word;

    scrollbar-width: thin;
    scrollbar-color: rgba(15, 17, 21, 0.25) transparent;

    &::-webkit-scrollbar {
      width: 10px;
      height: 10px;
    }

    &::-webkit-scrollbar-track {
      background: transparent;
    }

    &::-webkit-scrollbar-thumb {
      background-color: rgba(15, 17, 21, 0.22);
      border-radius: 10px;
      border: 2px solid transparent;
      background-clip: content-box;
    }

    :deep(h3) {
      font-size: 13.5px;
      font-weight: 700;
      color: var(--primary);
      margin: 18px 0 8px;
      letter-spacing: 0.3px;
    }

    :deep(h3:first-child) {
      margin-top: 0;
    }

    :deep(h4) {
      font-size: 13px;
      font-weight: 700;
      color: var(--ink);
      margin: 14px 0 8px;
    }

    :deep(p) {
      margin-bottom: 8px;
    }

    :deep(ul) {
      list-style: none;
      padding-left: 14px;
      margin-bottom: 8px;
    }

    :deep(ul li) {
      position: relative;
      padding-left: 14px;
      margin-bottom: 4px;
    }

    :deep(ul li::before) {
      content: '•';
      position: absolute;
      left: 0;
      color: var(--primary);
    }

    :deep(ul ul) {
      margin-top: 4px;
      padding-left: 8px;
    }

    :deep(strong) {
      color: var(--ink);
      font-weight: 600;
    }

    :deep(a) {
      color: var(--primary);
      text-decoration: underline;
    }

    :deep(.req) {
      margin-top: 14px;
      padding-top: 14px;
      border-top: 1px solid var(--border);
      font-size: 12px;
      line-height: 1.7;
    }

    :deep(.req-row) {
      margin-bottom: 2px;
    }
  }

  &-footer {
    padding: 16px 22px;
    text-align: right;
    border-top: 1px solid var(--border);
    background: #fff;
  }
}

@keyframes slide {
  from {
    transform: translateY(16px);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}

@media (max-width: 480px) {
  .modal {
    &-overlay {
      padding: 12px;
      padding-top: max(12px, env(safe-area-inset-top));
      padding-bottom: max(12px, env(safe-area-inset-bottom));
    }

    &-content {
      max-height: calc(100dvh - 24px);
      border-radius: 14px;
    }

    &-header {
      padding: 16px 18px;

      h3 {
        font-size: 15px;
      }
    }

    &-body {
      padding: 16px 18px 22px;
      padding-bottom: max(22px, env(safe-area-inset-bottom));
      font-size: 12.5px;

      :deep(h3) {
        font-size: 13px;
      }

      :deep(h4) {
        font-size: 12.5px;
      }
    }
  }
}
</style>
