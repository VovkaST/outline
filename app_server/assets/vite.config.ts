import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { fileURLToPath, URL } from 'node:url';

import vue from '@vitejs/plugin-vue';
import vueJsx from '@vitejs/plugin-vue-jsx';
import { defineConfig, type Plugin } from 'vite';
import vueDevTools from 'vite-plugin-vue-devtools';

import { mergeSiteConfig } from './src/config/siteConfig.defaults';
import type { SiteConfigInput } from './src/config/siteConfig.types';

const ZERO_WIDTH_PATTERN = /[\u200B-\u200D\uFEFF]/g;
const FAVICONS_BLOCK_PATTERN = /<!-- favicons -->[\s\S]*?<!-- \/favicons -->/;
const BABOCHKI_FAVICON = '<link rel="icon" type="image/svg+xml" href="/static/favicon-babochki.svg" />';

// Строки из site-config.json заполняются вручную и могут содержать невидимые символы.
function toHtmlText(value: string): string {
  return value
    .replace(ZERO_WIDTH_PATTERN, '')
    .replace(/\s+/g, ' ')
    .trim()
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}

// Подставляет в index.html заголовок и favicon из site-config.json на этапе сборки,
// чтобы они были верными ещё до загрузки JS (вкладка, превью ссылок).
const siteConfigHtmlPlugin = (): Plugin => ({
  name: 'site-config-html',
  transformIndexHtml(html) {
    const raw = JSON.parse(readFileSync(resolve(__dirname, 'site-config.json'), 'utf-8')) as SiteConfigInput;
    const { site } = mergeSiteConfig(raw);

    let result = html
      .replace(/%SITE_TITLE%/g, toHtmlText(site.title))
      .replace(/%SITE_NAME%/g, toHtmlText(site.name));

    if (site.theme === 'babochki') {
      result = result.replace(FAVICONS_BLOCK_PATTERN, BABOCHKI_FAVICON);
    }

    return result;
  },
});

// https://vite.dev/config/
export default defineConfig({
  plugins: [vue(), vueJsx(), vueDevTools(), siteConfigHtmlPlugin()],
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
      scss: {},
    },
  },
});
