<script setup lang="ts">
const props = withDefaults(
  defineProps<{
    notificationType: string;
  }>(),
  { notificationType: 'info' },
);
</script>

<template>
  <div :class="['notice', props.notificationType]" role="alert">
    <i class="fas fa-exclamation-circle"></i>
    <slot></slot>
  </div>
</template>

<style scoped lang="scss">
.notice {
  padding: 16px;
  font-size: 16px;

  &.info {
    background: linear-gradient(135deg, rgba(16, 185, 129, 0.15), rgba(16, 185, 129, 0.1));
    color: #1e293b;
  }

  &.warning {
    background: linear-gradient(135deg, rgba(245, 158, 11, 0.25), rgba(245, 158, 11, 0.15));
    color: #92400e;
  }

  &.error {
    background: linear-gradient(135deg, rgba(255, 0, 0, 0.15), rgba(255, 0, 0, 0.1));
    color: white;
  }
  &.critical {
    background: linear-gradient(135deg, rgba(245, 158, 11, 0.25) 0%, rgba(245, 158, 11, 0.15) 100%);
    color: #fef3c7;
    border-color: rgba(245, 158, 11, 0.4);
    background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
    color: #92400e;
    padding: 20px;
    border-radius: 12px;
    font-weight: 900;
    font-size: 18px;
    text-align: center;
    border: 3px solid #f59e0b;
    margin: 25px 0;
    text-transform: uppercase;
    letter-spacing: 0.8px;
    box-shadow: 0 8px 25px rgba(245, 158, 11, 0.4);
    animation: pulse-yellow 2s infinite;
  }

  .fas {
    margin-right: 0.5rem;
  }
}

@media (prefers-color-scheme: dark) {
  .notice {
    background: linear-gradient(135deg, rgba(245, 158, 11, 0.25) 0%, rgba(245, 158, 11, 0.15) 100%);
    color: #fef3c7;
    border-color: rgba(245, 158, 11, 0.4);
  }
}
@media (max-width: 360px) {
  .notice {
    padding: 16px;
    font-size: 16px;
  }
}
@media (max-width: 800px) {
  .notice {
    padding: 22px;
    font-size: 19px;
  }
}
@media (max-width: 900px) {
  .notice {
    padding: 24px;
    font-size: 20px;
  }
}
</style>
