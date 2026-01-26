/// <reference types="vite/client" />

declare module '*.json' {
  const value: any;
  export default value;
}

interface ImportMetaEnv {
  readonly VITE_APP_LINK_ANDROID?: string;
  readonly VITE_APP_LINK_IPHONE_US?: string;
  readonly VITE_APP_LINK_IPHONE_RU?: string;
  readonly VITE_APP_LINK_WINDOWS?: string;
  readonly VITE_APP_LINK_MAC_US?: string;
  readonly VITE_APP_LINK_MAC_RU?: string;
  readonly VITE_SUBSCRIPTION_URL?: string;
}

interface ImportMeta {
  readonly env: ImportMetaEnv;
}
