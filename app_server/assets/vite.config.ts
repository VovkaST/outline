import { copyFileSync, existsSync } from 'node:fs';
import { resolve } from 'node:path';
import { fileURLToPath, URL } from 'node:url';

import vue from '@vitejs/plugin-vue';
import vueJsx from '@vitejs/plugin-vue-jsx';
import { defineConfig } from 'vite';
import vueDevTools from 'vite-plugin-vue-devtools';

const root = fileURLToPath(new URL('.', import.meta.url));
const siteConfigPath = resolve(root, 'site-config.json');

function copySiteConfig(): import('vite').Plugin {
  return {
    name: 'copy-site-config',
    closeBundle() {
      const out = resolve(root, 'dist', 'site-config.json');
      if (existsSync(siteConfigPath)) {
        copyFileSync(siteConfigPath, out);
      }
    },
  };
}

// https://vite.dev/config/
export default defineConfig({
  plugins: [copySiteConfig(), vue(), vueJsx(), vueDevTools()],
  server: {
    host: '0.0.0.0',
    port: 8080,
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
    lib: {
      entry: resolve(__dirname, './src/main.ts'),
      name: 'Assets',
      fileName: 'assets',
    },
    rollupOptions: {
      input: {
        main: resolve(__dirname, 'index.html'),
      },
      external: [],
      output: {
        entryFileNames: `[name].[hash].js`,
        chunkFileNames: `[name].[hash].js`,
        assetFileNames: `[name].[hash].[ext]`
      },
    },
  },
  css: {
    preprocessorOptions: {
      scss: {
        api: 'modern-compiler',
      },
    },
  },
});
