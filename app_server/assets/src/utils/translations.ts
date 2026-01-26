import ruTranslations from '@/locales/ru.json';
import enTranslations from '@/locales/en.json';

export type Language = 'ru' | 'en';

export type Translations = typeof ruTranslations;

const translations: Record<Language, Translations> = {
  ru: ruTranslations,
  en: enTranslations,
};

export const getTranslations = (lang: Language): Translations => {
  return translations[lang] || translations.ru;
};

export const detectLanguage = (): Language => {
  const savedLang = localStorage.getItem('preferredLanguage');
  if (savedLang === 'ru' || savedLang === 'en') {
    return savedLang;
  }
  const userLang = navigator.language || (navigator as any).userLanguage;
  return userLang.startsWith('ru') ? 'ru' : 'en';
};
