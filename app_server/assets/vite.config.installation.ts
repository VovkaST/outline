import { fileURLToPath, URL } from 'node:url';

import vue from '@vitejs/plugin-vue';
import vueJsx from '@vitejs/plugin-vue-jsx';
import { resolve } from 'path';
import { defineConfig, type Plugin } from 'vite';
import vueDevTools from 'vite-plugin-vue-devtools';

// Плагин для использования installation.html вместо index.html в dev режиме
const installationHtmlPlugin = (): Plugin => {
  return {
    name: 'installation-html',
    configureServer(server) {
      server.middlewares.use((req, res, next) => {
        if (req.url === '/' || req.url === '/index.html') {
          req.url = '/installation.html';
        }
        next();
      });
    },
  };
};

// Конфигурация для сборки приложения установки
export default defineConfig({
  plugins: [vue(), vueJsx(), vueDevTools(), installationHtmlPlugin()],
  server: {
    host: '0.0.0.0',
    port: 8081, // Другой порт для dev режима
  },
  define: {
    'process.env': {},
  },
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url)),
      '~bootstrap': resolve(__dirname, 'node_modules/bootstrap'),
    },
  },
  build: {
    outDir: 'dist-installation',
    emptyOutDir: true,
    rollupOptions: {
      input: resolve(__dirname, 'installation.html'),
      output: {
        entryFileNames: `[name].[hash].js`,
        chunkFileNames: `[name].[hash].js`,
        assetFileNames: `[name].[hash].[ext]`,
      },
    },
  },
  css: {
    preprocessorOptions: {
      scss: {},
    },
  },
});
