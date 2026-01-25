import { getEnvVar } from "./utils";

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
};
