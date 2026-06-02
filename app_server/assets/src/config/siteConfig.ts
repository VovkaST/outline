import siteConfigJson from '../../site-config.json';
import { mergeSiteConfig } from '@/config/siteConfig.defaults';
import type { SiteConfigInput } from '@/config/siteConfig.types';

export const siteConfig = mergeSiteConfig(siteConfigJson as SiteConfigInput);
