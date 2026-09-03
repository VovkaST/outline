import type {
  SiteConfig,
  SiteConfigInput,
  SiteConfigOrganizationInput,
  SiteConfigPublicOffer,
  SiteConfigSite,
  SiteConfigSubscriptionButton,
  SiteConfigSupportItem,
  SiteTheme,
} from './siteConfig.types';

export const DEFAULT_SITE_CONFIG = {
  site: {
    theme: 'classic',
    copyrightSuffix: '',
    tariffsHeader: 'Выберите тариф',
  },
  publicOffer: {
    representativeBasis: 'Устава',
  },
  supportItems: [],
  subscriptionAddUrl: '',
  subscriptionButton: {
    url: '',
    title: 'Получить пробную подписку',
    hint: 'если это не ваш номер',
  },
  tariffNote:
    '<strong>1 ключ</strong> можно использовать <strong>только на одном устройстве</strong>.',
} as const satisfies Pick<
  Partial<SiteConfig>,
  'supportItems' | 'subscriptionAddUrl' | 'tariffNote'
> & {
  site: Pick<SiteConfigSite, 'theme' | 'copyrightSuffix' | 'tariffsHeader'>;
  publicOffer: Pick<SiteConfigPublicOffer, 'representativeBasis'>;
  supportItems: readonly SiteConfigSupportItem[];
  subscriptionButton: SiteConfigSubscriptionButton;
};

const SITE_THEMES: readonly SiteTheme[] = ['classic', 'babochki'];

function resolveSiteTheme(value: unknown): SiteTheme {
  return SITE_THEMES.includes(value as SiteTheme)
    ? (value as SiteTheme)
    : DEFAULT_SITE_CONFIG.site.theme;
}

const REQUIRED_SITE_FIELDS: (keyof Pick<SiteConfigSite, 'name' | 'url' | 'title'>)[] = [
  'name',
  'url',
  'title',
];

const REQUIRED_ORGANIZATION_FIELDS: (keyof SiteConfigOrganizationInput)[] = [
  'fullName',
  'inn',
  'legalAddress',
  'bank',
  'bankAccount',
  'correspondentAccount',
  'bik',
  'phone',
  'email',
];

function validateRequired(raw: SiteConfigInput): void {
  const missing: string[] = [];

  for (const field of REQUIRED_SITE_FIELDS) {
    if (!raw.site?.[field]) {
      missing.push(`site.${field}`);
    }
  }

  for (const field of REQUIRED_ORGANIZATION_FIELDS) {
    if (!raw.organization?.[field]) {
      missing.push(`organization.${field}`);
    }
  }

  if (!raw.publicOffer?.city) {
    missing.push('publicOffer.city');
  }

  if (!raw.publicOffer?.representativeName) {
    missing.push('publicOffer.representativeName');
  }

  if (!raw.tariffs?.length) {
    missing.push('tariffs');
  }

  if (missing.length > 0) {
    throw new Error(`Missing required site-config fields: ${missing.join(', ')}`);
  }
}

export function mergeSiteConfig(raw: SiteConfigInput): SiteConfig {
  validateRequired(raw);

  const site = {
    ...DEFAULT_SITE_CONFIG.site,
    ...raw.site,
    theme: resolveSiteTheme(raw.site.theme),
    copyrightSuffix: raw.site.copyrightSuffix ?? DEFAULT_SITE_CONFIG.site.copyrightSuffix,
    tariffsHeader: raw.site.tariffsHeader ?? DEFAULT_SITE_CONFIG.site.tariffsHeader,
  };

  const publicOffer = {
    ...DEFAULT_SITE_CONFIG.publicOffer,
    ...raw.publicOffer,
    representativeBasis:
      raw.publicOffer.representativeBasis ?? DEFAULT_SITE_CONFIG.publicOffer.representativeBasis,
  };

  const supportItems = raw.supportItems ?? DEFAULT_SITE_CONFIG.supportItems;

  const subscriptionUrl =
    raw.subscriptionButton?.url ??
    raw.subscriptionAddUrl ??
    DEFAULT_SITE_CONFIG.subscriptionButton.url;
  const subscriptionButton: SiteConfigSubscriptionButton = {
    url: subscriptionUrl,
    title: raw.subscriptionButton?.title ?? DEFAULT_SITE_CONFIG.subscriptionButton.title,
    hint: raw.subscriptionButton?.hint ?? DEFAULT_SITE_CONFIG.subscriptionButton.hint,
  };
  const tariffNote = raw.tariffNote ?? DEFAULT_SITE_CONFIG.tariffNote;

  return {
    site,
    organization: raw.organization,
    publicOffer,
    supportItems,
    subscriptionAddUrl: subscriptionUrl,
    subscriptionButton,
    tariffNote,
    announcement: raw.announcement,
    tariffs: raw.tariffs,
  };
}
