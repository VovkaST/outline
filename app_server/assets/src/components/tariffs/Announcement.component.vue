<script setup lang="ts"></script>

<template>
  <div class="announcement">
    <div class="announcement-title">
      <svg
        viewBox="0 0 24 24"
        fill="none"
        stroke="currentColor"
        stroke-width="2"
        stroke-linecap="round"
        stroke-linejoin="round"
      >
        <path
          d="M10.29 3.86 1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"
        />
        <line x1="12" y1="9" x2="12" y2="13" />
        <line x1="12" y1="17" x2="12.01" y2="17" />
      </svg>
      <slot name="title" />
    </div>
    <slot />
  </div>
</template>

<style lang="scss" scoped>
.announcement {
  background: linear-gradient(135deg, #fdf6e3 0%, #faf3e3 100%);
  border: 1px solid var(--primary);
  border-radius: 12px;
  padding: 16px 18px;
  margin-bottom: 28px;
  text-align: left;
}

.announcement-title {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  font-weight: 700;
  color: #8a6d28;
  margin-bottom: 8px;
  letter-spacing: -0.1px;
}

.announcement-title svg {
  width: 18px;
  height: 18px;
  flex-shrink: 0;
}

:slotted(p) {
  font-size: 13px;
  line-height: 1.55;
  color: #6b5320;
  margin-bottom: 6px;
}

:slotted(p:last-child) {
  margin-bottom: 0;
}

:slotted(.announcement-cta) {
  font-weight: 700;
  color: #5d4818;
}

@media (max-width: 380px) {
  .announcement {
    padding: 14px 16px;
    margin-bottom: 22px;
  }

  .announcement-title {
    font-size: 13px;
  }

  :slotted(p) {
    font-size: 12.5px;
  }
}
</style>
