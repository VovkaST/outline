<script setup lang="ts"></script>

<template>
  <section class="dummy-storage-flow-diagram" aria-label="Как работает облачное хранение">
    <div class="flow">
      <div class="flow-item">
        <div class="flow-icon" aria-hidden="true">
          <svg viewBox="0 0 64 64">
            <rect x="11" y="20" width="34" height="22" rx="7" />
            <circle cx="28" cy="31" r="7" />
            <path d="m45 25 9-5v22l-9-5M23 42v7M16 50h20" />
          </svg>
        </div>
        <div class="flow-label">Камера</div>
      </div>

      <div class="arrow" aria-hidden="true">
        <svg viewBox="0 0 48 24">
          <path d="M2 12h38M31 4l9 8-9 8" />
        </svg>
      </div>

      <div class="flow-item flow-item--cloud">
        <div class="flow-icon" aria-hidden="true">
          <svg viewBox="0 0 64 64">
            <path d="M19 47h28a11 11 0 0 0 1-22 17 17 0 0 0-32-5 13.5 13.5 0 0 0 3 27Z" />
            <path d="m24 34 8-8 8 8M32 27v14" />
          </svg>
        </div>
        <div class="flow-label">Облако</div>
      </div>

      <div class="arrow" aria-hidden="true">
        <svg viewBox="0 0 48 24">
          <path d="M2 12h38M31 4l9 8-9 8" />
        </svg>
      </div>

      <div class="flow-item">
        <div class="flow-icon" aria-hidden="true">
          <svg viewBox="0 0 64 64">
            <rect x="13" y="17" width="38" height="34" rx="5" />
            <path d="M13 29h38M24 38h16M24 44h10" />
            <rect x="22" y="10" width="20" height="12" rx="3" />
            <path d="m30 13 6 3-6 3Z" />
          </svg>
        </div>
        <div class="flow-label">
          Архив сохраняется<br />
          автоматически
        </div>
      </div>
    </div>

    <div class="diagram-footer">
      <div class="dots" aria-hidden="true">
        <span />
        <span />
        <span />
      </div>

      <p>Так будет храниться архив записей</p>
    </div>
  </section>
</template>

<style scoped lang="scss">
.dummy-storage-flow-diagram {
  overflow: hidden;
  padding: 25px 22px 17px;
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 22px;
  background:
    radial-gradient(circle at 50% 5%, rgba(86, 101, 218, 0.31), transparent 32%),
    linear-gradient(180deg, #172552, #141f40);
  box-shadow: 0 15px 35px rgba(20, 31, 64, 0.2);
  color: #fff;
}

.flow {
  display: grid;
  grid-template-columns: 1fr auto 1fr auto 1fr;
  align-items: center;
  gap: 10px;
}

.flow-item {
  min-width: 0;
  text-align: center;
}

.flow-icon {
  display: grid;
  width: 100px;
  height: 100px;
  margin: 0 auto 12px;
  place-items: center;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(255, 255, 255, 0.13), rgba(255, 255, 255, 0.025));
  box-shadow: inset 0 0 25px rgba(255, 255, 255, 0.04);
}

.flow-icon svg {
  width: 68px;
  height: 68px;
  fill: rgba(255, 255, 255, 0.11);
  stroke: #f6f7fb;
  stroke-linecap: round;
  stroke-linejoin: round;
  stroke-width: 2.2;
}

.flow-item--cloud .flow-icon svg {
  stroke: #7ca8ff;
}

.flow-label {
  min-height: 42px;
  color: #ff4949;
  font-size: 14px;
  font-weight: 800;
  line-height: 1.22;
  text-transform: uppercase;
}

.arrow {
  color: #ff4949;
}

.arrow svg {
  width: 37px;
  height: 25px;
  fill: none;
  stroke: currentColor;
  stroke-linecap: round;
  stroke-linejoin: round;
  stroke-width: 4;
}

.diagram-footer {
  margin-top: 17px;
  padding-top: 14px;
  border-top: 1px solid rgba(128, 147, 255, 0.32);
  text-align: center;
}

.dots {
  display: flex;
  justify-content: center;
  gap: 8px;
  margin-bottom: 8px;
}

.dots span {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #7180da;
}

.dots span:nth-child(2) {
  background: #5264d2;
}

.diagram-footer p {
  color: rgba(255, 255, 255, 0.78);
  font-size: 15px;
}

@media (max-width: 640px) {
  .dummy-storage-flow-diagram {
    padding: 21px 15px 16px;
    border-radius: 19px;
  }

  .flow {
    grid-template-columns: 1fr;
    gap: 9px;
  }

  .flow-icon {
    width: 88px;
    height: 88px;
    margin-bottom: 8px;
  }

  .flow-icon svg {
    width: 60px;
    height: 60px;
  }

  .flow-label {
    min-height: auto;
    font-size: 13px;
  }

  .arrow {
    display: grid;
    place-items: center;
  }

  .arrow svg {
    width: 30px;
    transform: rotate(90deg);
  }
}
</style>
