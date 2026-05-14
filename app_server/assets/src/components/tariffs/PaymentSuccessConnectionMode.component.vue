<script setup lang="ts"></script>

<template>
  <div class="mode">
    <div class="mode-icon" aria-hidden="true">
      <slot name="icon" />
    </div>
    <div class="mode-body">
      <div class="mode-name">
        <slot name="name" />
        <span v-if="$slots.tag" class="mode-tag"><slot name="tag" /></span>
      </div>
      <div class="mode-desc">
        <slot name="description" />
      </div>
    </div>
  </div>
</template>

<style scoped lang="scss">
.mode {
  display: flex;
  gap: 12px;
  background: #fff;
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 12px 14px;
  align-items: flex-start;
  transition:
    border-color 0.2s,
    box-shadow 0.2s;
}

.mode:hover {
  border-color: var(--primary);
  box-shadow: 0 4px 14px rgba(201, 169, 97, 0.15);
}

.mode-icon {
  flex-shrink: 0;
  width: 36px;
  height: 36px;
  border-radius: 9px;
  background: var(--primary-soft);
  display: grid;
  place-items: center;
  font-size: 18px;
}

.mode-body {
  flex: 1;
  min-width: 0;
}

.mode-name {
  font-size: 14px;
  font-weight: 700;
  color: var(--ink);
  margin-bottom: 2px;
  letter-spacing: -0.1px;
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 6px;
}

.mode-desc {
  font-size: 12.5px;
  line-height: 1.45;
  color: var(--ink-dim);
}

.mode-tag {
  display: inline-block;
  font-size: 10.5px;
  font-weight: 700;
  color: var(--primary-hover);
  background: var(--primary-soft);
  padding: 2px 7px;
  border-radius: 5px;
  letter-spacing: 0.2px;
}

@media (prefers-color-scheme: dark) {
  .mode {
    background: rgba(30, 41, 59, 0.98);
    border-color: rgba(148, 163, 184, 0.25);
  }

  .mode-name {
    color: #fff;
  }

  .mode-desc {
    color: rgba(255, 255, 255, 0.82);
  }
}
</style>
