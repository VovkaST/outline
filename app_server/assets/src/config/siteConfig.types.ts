export interface SiteConfigSite {
  name: string;
  copyrightSuffix?: string;
  url: string;
  title: string;
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

export interface SiteConfig {
  readonly site: SiteConfigSite;
  readonly organization: SiteConfigOrganization;
  readonly publicOffer: SiteConfigPublicOffer;
  readonly supportItems: readonly SiteConfigSupportItem[];
}
