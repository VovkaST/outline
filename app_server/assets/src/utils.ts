export function str2bool(str: string): boolean {
  return ['true', '1', 'y', 'yes'].includes(str.toLowerCase());
}
