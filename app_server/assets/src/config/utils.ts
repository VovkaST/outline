export const getEnvVar = (key: string, defaultValue: string): string => {
  const value = import.meta.env[key];
  if (!value) {
    console.warn(`Environment variable ${key} is not set, using default value`);
    return defaultValue;
  }
  return value;
};