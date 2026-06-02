import { siteConfig } from '@/config/siteConfig';
import type { SiteConfig } from '@/config/siteConfig.types';
import { readonly, ref, type Ref } from 'vue';

const configRef: Ref<SiteConfig> = ref(siteConfig);

export function useConfig(): Readonly<Ref<SiteConfig>> {
  return readonly(configRef);
}
