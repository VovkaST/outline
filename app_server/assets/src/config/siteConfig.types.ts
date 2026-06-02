export interface SiteConfigSite {
  name: string;
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
  readonly subscriptionAddUrl?: string;
  readonly announcement?: SiteConfigAnnouncement;
  readonly tariffs: readonly SiteConfigTariff[];
}

export interface SiteConfigSiteInput {
  name: string;
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
  subscriptionAddUrl?: string;
  announcement?: SiteConfigAnnouncementInput;
  tariffs: readonly SiteConfigTariff[];
}
