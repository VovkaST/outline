<script setup lang="ts">
import { ModalProvider } from '@/components';
import { nextTick, onMounted, onUnmounted, ref, watch } from 'vue';

const props = defineProps<{
  title?: string;
  closeOnEsc?: boolean;
  closeOnClickOutside?: boolean;
}>();

const showModal = defineModel<boolean>('show');
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

// Закрытие по Esc
const handleKeydown = (e: KeyboardEvent) => {
  if (props.closeOnEsc && e.key === 'Escape') {
    onCloseModal();
  }
};

// Закрытие по клику вне контента
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
          <button @click="onCloseModal" class="close-btn">&times;</button>
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
$borderRadius: 10px;

.modal {
  &-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.5);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 1000;
    transition: opacity 0.3s ease;
  }

  &-content {
    display: flex;
    flex-direction: column;
    background-color: #fff;
    border-radius: 8px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
    width: 90%;
    max-width: 90vw;
    max-height: 80vh;
    overflow-y: auto;
    transition: transform 0.3s ease;

    /* Для Firefox */
    scrollbar-width: thin;
    scrollbar-color: rgba(0, 0, 0, 0.3) transparent;
    border-radius: $borderRadius;

    /* Для Chrome/Edge/Opera */
    &::-webkit-scrollbar {
      width: 12px;
      height: 12px;
    }

    &::-webkit-scrollbar-track {
      background: transparent;
      border-radius: $borderRadius;
    }

    &::-webkit-scrollbar-thumb {
      background-color: rgba(0, 0, 0, 0.3);
      border-radius: $borderRadius;
      border: 3px solid transparent;
      background-clip: content-box;
    }

    &::-webkit-scrollbar-corner {
      background: transparent;
      border-radius: $borderRadius;
    }
  }

  &-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1px solid #e0e0e0;
    padding: 15px 20px;
    background: linear-gradient(135deg, var(--primary), #7c3aed);
    color: white;
    text-align: center;

    h3 {
      margin: 0;
      width: 100%;
      font-size: 1.25rem;
    }

    .close-btn {
      background: none;
      border: none;
      font-size: 1.5rem;
      cursor: pointer;
      color: #fff;

      &:hover {
        color: #000;
      }
    }
  }

  &-body {
    flex: 1;
    overflow-y: auto;
    padding: 24px;
    -webkit-overflow-scrolling: touch;
  }

  &-footer {
    padding: 16px 24px;
    text-align: right;
    border-top: 1px solid #e0e0e0;
  }
}
</style>
