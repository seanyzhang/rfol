const isDevelopment = import.meta.env.DEV;

export const logger = {
  log: (...args: any[]) => isDevelopment && console.log(...args),
  warn: (...args: any[]) => console.warn(...args),
  error: (...args: any[]) => console.error(...args),
};