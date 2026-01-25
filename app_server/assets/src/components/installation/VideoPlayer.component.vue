<script setup lang="ts">
import { computed, onMounted, onUnmounted, ref } from 'vue';

const props = defineProps<{
  videoSrc?: string;
  translations: {
    title: string;
    description: string;
    loadButtonText: string;
    loadingText: string;
    errorTitle: string;
    errorDescription: string;
    retryButtonText: string;
    fullscreenButtonText: string;
    exitFullscreenText: string;
  };
}>();

const emit = defineEmits<{
  (e: 'videoLoad'): void;
}>();

const videoElement = ref<HTMLVideoElement | null>(null);
const videoWrapper = ref<HTMLDivElement | null>(null);

const isFullscreen = ref(false);
const videoLoaded = ref(false);
const showPlaceholder = ref(true);
const showLoading = ref(false);
const showError = ref(false);

const videoSources = [
  props.videoSrc || 'video/video.MP4',
  'video/video.mp4',
  'video/Видео-инструкция.mp4',
  'video/instruction.mp4',
  'video/video-instruction.mp4',
];

let currentSourceIndex = 0;

const isIOS = computed(() => {
  return /iPad|iPhone|iPod/.test(navigator.userAgent) && !window.MSStream;
});

const loadVideo = () => {
  if (!videoElement.value) return;

  if (videoLoaded.value && videoElement.value.readyState >= 2) {
    showPlaceholder.value = false;
    showLoading.value = false;
    if (isIOS.value) {
      videoElement.value.play().catch(() => {
        showPlaceholder.value = true;
      });
    } else {
      videoElement.value.play().catch(() => {
        console.log('Автовоспроизведение заблокировано');
      });
    }
    return;
  }

  showPlaceholder.value = false;
  showLoading.value = true;
  showError.value = false;

  currentSourceIndex = 0;
  tryNextSource();
  emit('videoLoad');
};

const tryNextSource = () => {
  if (!videoElement.value) return;

  if (currentSourceIndex >= videoSources.length) {
    showLoading.value = false;
    showError.value = true;
    return;
  }

  const videoSrc = videoSources[currentSourceIndex];
  videoElement.value.src = videoSrc;

  videoElement.value.oncanplay = () => {
    videoLoaded.value = true;
    showLoading.value = false;

    if (isIOS.value) {
      videoElement.value?.play().then(() => {
        console.log('Видео успешно воспроизводится на iOS');
      }).catch(() => {
        showPlaceholder.value = true;
      });
    } else {
      videoElement.value?.play().then(() => {
        console.log('Видео успешно воспроизводится');
      }).catch(() => {
        console.log('Автовоспроизведение заблокировано');
      });
    }
  };

  videoElement.value.onerror = () => {
    currentSourceIndex++;
    if (currentSourceIndex >= videoSources.length) {
      showLoading.value = false;
      showError.value = true;
    } else {
      setTimeout(tryNextSource, 500);
    }
  };

  videoElement.value.load();
};

const toggleFullscreen = () => {
  if (!videoWrapper.value) return;

  if (!isFullscreen.value) {
    if (videoWrapper.value.requestFullscreen) {
      videoWrapper.value.requestFullscreen();
    } else if ((videoWrapper.value as any).webkitRequestFullscreen) {
      (videoWrapper.value as any).webkitRequestFullscreen();
    } else if ((videoWrapper.value as any).msRequestFullscreen) {
      (videoWrapper.value as any).msRequestFullscreen();
    }
    videoWrapper.value.classList.add('fullscreen');
    isFullscreen.value = true;
  } else {
    if (document.exitFullscreen) {
      document.exitFullscreen();
    } else if ((document as any).webkitExitFullscreen) {
      (document as any).webkitExitFullscreen();
    } else if ((document as any).msExitFullscreen) {
      (document as any).msExitFullscreen();
    }
    videoWrapper.value.classList.remove('fullscreen');
    isFullscreen.value = false;
  }
};

const handleFullscreenChange = () => {
  const isFullscreenNow = !!(
    document.fullscreenElement ||
    (document as any).webkitFullscreenElement ||
    (document as any).msFullscreenElement
  );

  if (!isFullscreenNow && videoWrapper.value) {
    videoWrapper.value.classList.remove('fullscreen');
    isFullscreen.value = false;
  }
};

onMounted(() => {
  document.addEventListener('fullscreenchange', handleFullscreenChange);
  document.addEventListener('webkitfullscreenchange', handleFullscreenChange);
  document.addEventListener('msfullscreenchange', handleFullscreenChange);
});

onUnmounted(() => {
  document.removeEventListener('fullscreenchange', handleFullscreenChange);
  document.removeEventListener('webkitfullscreenchange', handleFullscreenChange);
  document.removeEventListener('msfullscreenchange', handleFullscreenChange);
});
</script>

<template>
  <div ref="videoWrapper" class="video-wrapper">
    <div class="video-container">
      <video
        ref="videoElement"
        playsinline
        webkit-playsinline
        preload="none"
        aria-label="Видео инструкция по установке"
      >
        <source :src="videoSources[0]" type="video/mp4" />
        Ваш браузер не поддерживает видео.
      </video>

      <div
        v-if="showPlaceholder"
        ref="videoPlaceholder"
        class="video-placeholder"
        @click="loadVideo"
      >
        <i class="fas fa-play-circle"></i>
        <h3>{{ translations.title }}</h3>
        <p>{{ translations.description }}</p>
        <button class="btn" @click.stop="loadVideo">
          <i class="fas fa-play"></i>
          {{ translations.loadButtonText }}
        </button>
      </div>

      <div v-if="showLoading" ref="videoLoading" class="video-loading" aria-live="polite">
        <div class="loader"></div>
        <p>{{ translations.loadingText }}</p>
      </div>

      <div v-if="showError" ref="videoError" class="video-error" aria-live="assertive">
        <i class="fas fa-exclamation-triangle"></i>
        <h3>{{ translations.errorTitle }}</h3>
        <p>{{ translations.errorDescription }}</p>
        <button class="btn" @click="loadVideo">
          <i class="fas fa-redo"></i>
          {{ translations.retryButtonText }}
        </button>
      </div>

      <button class="fullscreen-btn" @click="toggleFullscreen">
        <i :class="isFullscreen ? 'fas fa-compress' : 'fas fa-expand'"></i>
        {{ isFullscreen ? translations.exitFullscreenText : translations.fullscreenButtonText }}
      </button>
    </div>
  </div>
</template>

<style scoped lang="scss">
.video-wrapper {
  width: 100%;
  border-radius: 12px;
  overflow: hidden;
  margin: 20px 0;
  background: #000;
  position: relative;
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.2);

  &.fullscreen {
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    z-index: 9999;
    margin: 0;
    border-radius: 0;
    background: #000;

    .video-container {
      width: 100%;
      height: 100%;
      padding-bottom: 0;
    }

    video {
      width: 100%;
      height: 100%;
      object-fit: contain;
    }

    .fullscreen-btn {
      bottom: 20px;
      right: 20px;
      padding: 10px 16px;
      font-size: 14px;
      background: rgba(0, 0, 0, 0.8);
    }
  }
}

.video-container {
  width: 100%;
  padding-bottom: 177.78%;
  position: relative;
  background: #000;

  video {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    object-fit: contain;
    background: #000;
  }
}

.fullscreen-btn {
  position: absolute;
  bottom: 12px;
  right: 12px;
  background: rgba(0, 0, 0, 0.7);
  color: white;
  border: none;
  border-radius: 6px;
  padding: 8px 12px;
  cursor: pointer;
  z-index: 30;
  display: flex;
  align-items: center;
  gap: 5px;
  font-size: 12px;
  font-weight: 600;
  transition: all 0.2s ease;
  -webkit-tap-highlight-color: rgba(255, 255, 255, 0.1);

  &:active {
    transform: scale(0.95);
  }

  &:hover {
    background: rgba(0, 0, 0, 0.9);
  }
}

.video-placeholder,
.video-loading,
.video-error {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background: rgba(0, 0, 0, 0.95);
  z-index: 20;
  border-radius: 12px;
  color: white;
  text-align: center;
  padding: 20px;
}

.video-placeholder {
  cursor: pointer;
  -webkit-tap-highlight-color: rgba(99, 102, 241, 0.1);

  &:active {
    background: rgba(0, 0, 0, 0.97);
  }

  i {
    font-size: 48px;
    color: var(--primary);
    margin-bottom: 16px;
    opacity: 0.9;
  }

  h3 {
    font-size: 18px;
    margin-bottom: 8px;
    color: white;
    font-weight: 600;
    line-height: 1.3;
  }

  p {
    font-size: 13px;
    color: rgba(255, 255, 255, 0.9);
    margin-bottom: 20px;
    line-height: 1.4;
    max-width: 90%;
    -webkit-user-select: none;
    user-select: none;
  }

  .btn {
    max-width: 200px;
    margin-top: 8px;
    padding: 14px;
    font-size: 14px;
  }
}

.video-loading {
  z-index: 25;
}

.loader {
  width: 40px;
  height: 40px;
  border: 2px solid rgba(255, 255, 255, 0.2);
  border-top: 2px solid var(--primary);
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 16px;
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

.video-error {
  z-index: 30;

  i {
    font-size: 40px;
    color: #ef4444;
    margin-bottom: 16px;
    opacity: 0.9;
  }

  h3 {
    font-size: 18px;
    margin-bottom: 10px;
    color: white;
    font-weight: 600;
    line-height: 1.3;
  }

  p {
    font-size: 13px;
    color: rgba(255, 255, 255, 0.9);
    margin-bottom: 8px;
    line-height: 1.4;
  }

  .btn {
    margin-top: 20px;
    max-width: 200px;
  }
}

.btn {
  display: block;
  width: 100%;
  padding: 16px;
  background: linear-gradient(135deg, var(--primary), var(--primary-dark));
  color: white;
  border: none;
  border-radius: 12px;
  font-size: 15px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  text-align: center;
  text-decoration: none;
  -webkit-tap-highlight-color: rgba(99, 102, 241, 0.2);
  user-select: none;
  position: relative;
  overflow: hidden;

  i {
    margin-right: 8px;
    font-size: 14px;
  }

  &:active {
    transform: scale(0.98);
  }

  &:hover {
    box-shadow: 0 8px 20px rgba(99, 102, 241, 0.35);
  }
}

@media (prefers-color-scheme: dark) {
  .video-placeholder,
  .video-loading,
  .video-error {
    background: rgba(0, 0, 0, 0.9);
  }

  .fullscreen-btn {
    background: rgba(255, 255, 255, 0.3);
    color: white;
  }
}
</style>
