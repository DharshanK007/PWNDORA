// ─── Typed Environment Variables ──────────────────────────────────────────────
// All env values are read from VITE_ prefixed variables.
// No hardcoded URLs anywhere in the codebase.

const getEnvVar = (key: string): string => {
  const value = import.meta.env[key]
  if (!value) {
    console.warn(`[env] Missing environment variable: ${key}`)
    return ''
  }
  return value as string
}

export const env = {
  API_BASE_URL: getEnvVar('VITE_API_BASE_URL'),
  MODE: import.meta.env.MODE as 'development' | 'production' | 'test',
  IS_DEV: import.meta.env.DEV,
  IS_PROD: import.meta.env.PROD,
} as const

export type Env = typeof env
