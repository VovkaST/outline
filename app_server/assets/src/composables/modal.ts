import { ref, computed } from 'vue'

export function useModal() {
  const isOpen = ref(false)

  // Открывает модальное окно
  const open = () => {
    isOpen.value = true
  }

  // Закрывает модальное окно
  const close = () => {
    isOpen.value = false
  }

  // Переключает состояние
  const toggle = () => {
    isOpen.value = !isOpen.value
  }

  // Вычисляемое свойство для классов анимации
  const modalClasses = computed(() => ({
    'modal-open': isOpen.value,
    'modal-closed': !isOpen.value
  }))

  return {
    isOpen,
    open,
    close,
    toggle,
    modalClasses
  }
}
