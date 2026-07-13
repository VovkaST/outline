/// <reference types="vite/client" />

declare module '*.json' {
  // eslint-disable-next-line @typescript-eslint/no-explicit-any -- ambient stub for JSON imports
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
  readonly VITE_USE_SUCCESS_DUMMY_PAGE?: string;
}

interface ImportMeta {
  readonly env: ImportMetaEnv;
}
