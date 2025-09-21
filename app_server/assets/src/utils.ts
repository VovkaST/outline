import { PlatformOS } from "@/types";

export function str2bool(str: string): boolean {
  return ['true', '1', 'y', 'yes'].includes(str.toLowerCase());
}

export function platformOSDetect(userAgent: string): PlatformOS {
  if (/iPhone|iPad|iPod/i.test(userAgent)) return PlatformOS.IOS;
  if (/Android/i.test(userAgent)) return PlatformOS.ANDROID;
  return PlatformOS.WINDOWS
}

export function validateEmail(email: string): boolean {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
}