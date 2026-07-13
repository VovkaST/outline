<script setup lang="ts"></script>

<template>
  <section class="dummy-success-hero" aria-labelledby="dummy-success-title">
    <div class="check-icon" aria-hidden="true">
      <svg viewBox="0 0 24 24" role="img">
        <path d="M20 6 9 17l-5-5" />
      </svg>
    </div>

    <h1 id="dummy-success-title" class="dummy-success-hero__title">
      <slot name="title" />
    </h1>

    <p class="dummy-success-hero__text">
      <slot name="description" />
    </p>

    <div v-if="$slots.badge" class="dummy-success-hero__badge">
      <slot name="badge" />
    </div>
  </section>
</template>

<style scoped lang="scss">
.dummy-success-hero {
  --dummy-card-radius: 22px;
  --dummy-shadow: 0 18px 45px rgba(31, 43, 60, 0.13);
  --dummy-gold: #d0aa50;

  position: relative;
  overflow: hidden;
  padding: 28px 28px 22px;
  border: 1px solid rgba(22, 201, 156, 0.52);
  border-radius: var(--dummy-card-radius);
  background:
    linear-gradient(
      180deg,
      rgba(218, 240, 236, 0.98) 0%,
      rgba(104, 127, 139, 0.92) 42%,
      rgba(24, 39, 57, 0.99) 100%
    );
  box-shadow: var(--dummy-shadow);
  color: #fff;
  text-align: center;
  margin-bottom: 0;
}

.dummy-success-hero::before {
  position: absolute;
  inset: 0;
  background:
    linear-gradient(120deg, rgba(255, 255, 255, 0.2), transparent 45%),
    radial-gradient(circle at 50% 0, rgba(255, 255, 255, 0.2), transparent 44%);
  content: '';
  pointer-events: none;
}

.dummy-success-hero > * {
  position: relative;
  z-index: 1;
}

.check-icon {
  display: grid;
  width: 68px;
  height: 68px;
  margin: 0 auto 17px;
  place-items: center;
  border-radius: 50%;
  background: linear-gradient(180deg, #1bd4a6, #11bc8f);
  box-shadow: 0 13px 28px rgba(17, 188, 143, 0.33);
}

.check-icon svg {
  width: 35px;
  height: 35px;
  fill: none;
  stroke: #fff;
  stroke-linecap: round;
  stroke-linejoin: round;
  stroke-width: 3.2;
}

.dummy-success-hero__title {
  margin-bottom: 10px;
  font-size: clamp(26px, 5vw, 36px);
  font-weight: 800;
  letter-spacing: -0.8px;
  line-height: 1.15;
}

.dummy-success-hero__text {
  width: min(100%, 550px);
  margin: 0 auto;
  color: rgba(255, 255, 255, 0.96);
  font-size: clamp(16px, 3.1vw, 20px);
  line-height: 1.5;
}

.dummy-success-hero__badge {
  margin-top: 20px;
}

@media (max-width: 640px) {
  .dummy-success-hero {
    padding: 23px 18px 19px;
    border-radius: 19px;
  }

  .check-icon {
    width: 58px;
    height: 58px;
    margin-bottom: 14px;
  }

  .check-icon svg {
    width: 30px;
    height: 30px;
  }
}
</style>
