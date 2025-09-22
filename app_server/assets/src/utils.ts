import { PlatformOS } from '@/types';

export function str2bool(str: string): boolean {
  return ['true', '1', 'y', 'yes'].includes(str.toLowerCase());
}

export function platformOSDetect(userAgent: string): PlatformOS {
  if (/iPhone|iPad|iPod/i.test(userAgent)) return PlatformOS.IOS;
  if (/Android/i.test(userAgent)) return PlatformOS.ANDROID;
  return PlatformOS.WINDOWS;
}

export function validateEmail(email: string): boolean {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
}

export function safeParseFloat(value: string | number): number {
  if (typeof value === 'number') return value;
  return parseFloat(String(value).replace(/\s+/g, '').replace(',', '.'));
}

export function decimalNumberFormat({
  value,
  fractionDigits = 2,
  cutFractionDigits = false,
  currency,
}: {
  value: string | number;
  fractionDigits?: number;
  cutFractionDigits?: boolean;
  currency?: string;
}): string {
  const val = value ? value : 0;
  let options = {
    minimumFractionDigits: cutFractionDigits ? 0 : fractionDigits,
    maximumFractionDigits: fractionDigits,
  };
  if (currency) {
    options = {
      style: 'currency',
      currency: currency,
      ...options,
    };
  }
  return parseFloat(safeParseFloat(val).toFixed(fractionDigits)).toLocaleString('ru-RU', options);
}
