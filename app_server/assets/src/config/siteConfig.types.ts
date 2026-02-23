export interface SiteConfigSite {
  name: string;
  copyrightSuffix?: string;
  url: string;
  title: string;
}

export interface SiteConfigOrganisation {
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
  site: SiteConfigSite;
  organisation: SiteConfigOrganisation;
  publicOffer: SiteConfigPublicOffer;
  supportItems: SiteConfigSupportItem[];
}
