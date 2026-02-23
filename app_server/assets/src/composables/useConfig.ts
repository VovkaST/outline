import type { SiteConfig } from '@/config/siteConfig.types';
import { readonly, ref, type Ref } from 'vue';

const CONFIG_URL = '/site-config.json';

function getDefaultConfig(): SiteConfig {
  return {
    site: { name: 'Сайт', copyrightSuffix: '', url: '', title: 'Сайт' },
    organisation: {
      fullName: '',
      inn: '',
      legalAddress: '',
      bank: '',
      bankAccount: '',
      correspondentAccount: '',
      bik: '',
      phone: '',
      email: '',
    },
    publicOffer: {
      city: '',
      representativeName: '',
      representativeBasis: 'Устава',
    },
    supportItems: [],
  };
}

let configRef: Ref<SiteConfig> | null = null;

export function useConfig(): Readonly<Ref<SiteConfig>> {
  if (!configRef) {
    configRef = ref<SiteConfig>(getDefaultConfig());
    fetch(CONFIG_URL, { cache: 'no-store' })
      .then((res) => (res.ok ? res.json() : getDefaultConfig()))
      .catch(() => getDefaultConfig())
      .then((data) => {
        configRef!.value = (data as SiteConfig) ?? getDefaultConfig();
      });
  }
  return readonly(configRef);
}
