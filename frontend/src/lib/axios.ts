import axios, { AxiosError, type InternalAxiosRequestConfig, type AxiosResponse } from 'axios'
import { env } from '@/config/env'
import { tokenService } from '@/services/token'
import type { ApiError } from '@/types/api'

// ─── Custom Events ────────────────────────────────────────────────────────────
// Allows independent components (like AuthContext) to listen for 401s
// without creating a circular dependency with Axios.

export const AUTH_UNAUTHORIZED_EVENT = 'auth:unauthorized'

// ─── Axios Instance ───────────────────────────────────────────────────────────

const apiClient = axios.create({
  baseURL: env.API_BASE_URL,
  timeout: 30_000,
  headers: {
    'Content-Type': 'application/json',
    Accept: 'application/json',
  },
})

// ─── Request Interceptor ─────────────────────────────────────────────────────
// Attaches the Bearer token dynamically on every request.

apiClient.interceptors.request.use(
  (config: InternalAxiosRequestConfig) => {
    const token = tokenService.getAccessToken()
    if (token && config.headers) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error: AxiosError) => Promise.reject(error)
)

// ─── Response Interceptor ─────────────────────────────────────────────────────
// Normalizes responses and handles 401s cleanly.

apiClient.interceptors.response.use(
  (response: AxiosResponse) => response,
  (error: AxiosError<ApiError>) => {
    if (error.response?.status === 401) {
      // Dispatch a global event so the AuthContext can log the user out cleanly
      window.dispatchEvent(new Event(AUTH_UNAUTHORIZED_EVENT))
    }

    const apiError: ApiError = {
      status: error.response?.status ?? 0,
      detail: error.response?.data?.detail ?? error.message ?? 'An unexpected error occurred',
      code: error.response?.data?.code,
      errors: error.response?.data?.errors,
    }

    return Promise.reject(apiError)
  }
)

export default apiClient
