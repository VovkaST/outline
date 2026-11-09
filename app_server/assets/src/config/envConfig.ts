import { str2bool } from '@/utils';
import { getEnvVar } from "./utils";

const PAYMENT_GATEWAYS = ['yookassa', 'wata', 'platega'] as const;
const DEFAULT_PAYMENT_SOURCE_MAP = 'vk:platega,wa:wata,pf:platega,tg:wata';
const DEFAULT_DEPRECATED_URL_SOURCE = 'pf';

export type PaymentGateway = (typeof PAYMENT_GATEWAYS)[number];

const PAYMENT_GATEWAY_SET: ReadonlySet<string> = new Set(PAYMENT_GATEWAYS);

function isPaymentGateway(value: string): value is PaymentGateway {
  return PAYMENT_GATEWAY_SET.has(value);
}

function parsePaymentSourceMap(raw: string): Readonly<Record<string, PaymentGateway>> {
  const map: Record<string, PaymentGateway> = {};
  for (const chunk of raw.split(',')) {
    const pair = chunk.trim();
    if (!pair) continue;
    const separator = pair.indexOf(':');
    // Пустой ключ (нет двоеточия или оно в начале) и неизвестный шлюз пропускаются.
    if (separator <= 0) continue;
    const key = pair.slice(0, separator).trim().toLowerCase();
    const gateway = pair.slice(separator + 1).trim().toLowerCase();
    if (!key || !isPaymentGateway(gateway)) continue;
    map[key] = gateway;
  }
  return map;
}

function readDeprecatedUrlSource(): string {
  const source = getEnvVar('VITE_DEPRECATED_URL_SOURCE', DEFAULT_DEPRECATED_URL_SOURCE)
    .trim()
    .toLowerCase();
  return source || DEFAULT_DEPRECATED_URL_SOURCE;
}

export const paymentSourceMap = parsePaymentSourceMap(
  getEnvVar('VITE_PAYMENT_SOURCE_MAP', DEFAULT_PAYMENT_SOURCE_MAP),
);

export const deprecatedUrlSource = readDeprecatedUrlSource();

export interface AppConfigType {
  android: {
    url: string;
  };
  iphone: {
    appStoreUs: string;
    appStoreRu: string;
  };
  windows: {
    url: string;
  };
  mac: {
    appStoreUs: string;
    appStoreRu: string;
  };
  poolingInterval: number;
  useDummyConfig: boolean;
}



export const AppConfig: AppConfigType = {
  android: {
    url: getEnvVar(
      'VITE_APP_LINK_ANDROID',
      'https://play.google.com/store/apps/details?id=com.happproxy',
    ),
  },
  iphone: {
    appStoreUs: getEnvVar(
      'VITE_APP_LINK_IPHONE_US',
      'https://apps.apple.com/us/app/happ-proxy-utility/id6504287215',
    ),
    appStoreRu: getEnvVar(
      'VITE_APP_LINK_IPHONE_RU',
      'https://apps.apple.com/ru/app/happ-proxy-utility-plus/id6746188973',
    ),
  },
  windows: {
    url: getEnvVar(
      'VITE_APP_LINK_WINDOWS',
      'https://github.com/Happ-proxy/happ-desktop/releases/latest/download/setup-Happ.x64.exe',
    ),
  },
  mac: {
    appStoreUs: getEnvVar(
      'VITE_APP_LINK_MAC_US',
      'https://apps.apple.com/us/app/happ-proxy-utility/id6504287215',
    ),
    appStoreRu: getEnvVar(
      'VITE_APP_LINK_MAC_RU',
      'https://apps.apple.com/ru/app/happ-proxy-utility-plus/id6746188973',
    ),
  },
  poolingInterval: Number(getEnvVar('VITE_APP_POOLING_INTERVAL', '1500')),
  useDummyConfig: str2bool(getEnvVar('VITE_USE_DUMMY_CONFIG', 'false')),
};
