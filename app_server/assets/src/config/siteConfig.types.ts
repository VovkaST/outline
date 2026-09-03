export type SiteTheme = 'classic' | 'babochki';

export interface SiteConfigSite {
  name: string;
  theme: SiteTheme;
  copyrightSuffix: string;
  url: string;
  title: string;
  tariffsHeader: string;
}

export interface SiteConfigOrganization {
  fullName: string;
  inn: string;
  ogrn?: string;
  legalAddress: string;
  bank: string;
  bankAccount: string;
  correspondentAccount: string;
  bik: string;
  phone: string;
  email: string;
}

export interface SiteConfigPublicOffer {
  city: string;
  representativeName: string;
  representativeBasis: string;
}

export interface SiteConfigSupportItem {
  url: string;
  text: string;
}

export interface SiteConfigSubscriptionButtonInput {
  url?: string;
  /** Может содержать HTML-теги, выводится без экранирования. */
  title?: string;
  /** Может содержать HTML-теги, выводится без экранирования. */
  hint?: string;
}

export interface SiteConfigSubscriptionButton {
  url: string;
  title: string;
  hint: string;
}

export interface SiteConfigTariff {
  period: string;
  price: number;
  featured?: boolean;
}

export interface SiteConfigAnnouncement {
  title: string;
  paragraphs: readonly string[];
  cta?: string;
  deadline?: string;
}

export interface SiteConfig {
  readonly site: SiteConfigSite;
  readonly organization: SiteConfigOrganization;
  readonly publicOffer: SiteConfigPublicOffer;
  readonly supportItems: readonly SiteConfigSupportItem[];
  /** URL кнопки пробной подписки. Сохранён для обратной совместимости; дублирует subscriptionButton.url. */
  readonly subscriptionAddUrl?: string;
  readonly subscriptionButton: SiteConfigSubscriptionButton;
  /** HTML-строка инфо-карточки на экране выбора тарифа, выводится без экранирования. */
  readonly tariffNote: string;
  readonly announcement?: SiteConfigAnnouncement;
  readonly tariffs: readonly SiteConfigTariff[];
}

export interface SiteConfigSiteInput {
  name: string;
  theme?: SiteTheme;
  url: string;
  title: string;
  copyrightSuffix?: string;
  tariffsHeader?: string;
}

export interface SiteConfigOrganizationInput {
  fullName: string;
  inn: string;
  ogrn?: string;
  legalAddress: string;
  bank: string;
  bankAccount: string;
  correspondentAccount: string;
  bik: string;
  phone: string;
  email: string;
}

export interface SiteConfigPublicOfferInput {
  city: string;
  representativeName: string;
  representativeBasis?: string;
}

export interface SiteConfigAnnouncementInput {
  title: string;
  paragraphs: readonly string[];
  cta?: string;
  deadline?: string;
}

export interface SiteConfigInput {
  site: SiteConfigSiteInput;
  organization: SiteConfigOrganizationInput;
  publicOffer: SiteConfigPublicOfferInput;
  supportItems?: readonly SiteConfigSupportItem[];
  /** Legacy-вход: URL кнопки пробной подписки. Предпочтителен subscriptionButton.url. */
  subscriptionAddUrl?: string;
  subscriptionButton?: SiteConfigSubscriptionButtonInput;
  tariffNote?: string;
  announcement?: SiteConfigAnnouncementInput;
  tariffs: readonly SiteConfigTariff[];
}
