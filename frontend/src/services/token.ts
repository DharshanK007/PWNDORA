import { STORAGE_KEYS } from '@/constants/app'

// ─── JWT Storage Abstraction ──────────────────────────────────────────────────

export const tokenService = {
  getAccessToken(): string | null {
    return localStorage.getItem(STORAGE_KEYS.AUTH_TOKEN)
  },

  setAccessToken(token: string): void {
    localStorage.setItem(STORAGE_KEYS.AUTH_TOKEN, token)
  },

  removeAccessToken(): void {
    localStorage.removeItem(STORAGE_KEYS.AUTH_TOKEN)
  },
}
