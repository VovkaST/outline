<script setup lang="ts"></script>

<template>
  <button class="btn btn-primary" :data-amount="{ price }" @click="onActionClick">
    <slot></slot>
  </button>
</template>

<style lang="scss" scoped>
button {
  background: linear-gradient(90deg, var(--green-color), var(--dark-green-color));
  padding: 12px 16px;
  border-radius: 10px;
  color: #041004;
  font-size: 0.85rem;
  font-weight: 700;
  line-height: normal;
  border: none;
  cursor: pointer;
}
</style>
