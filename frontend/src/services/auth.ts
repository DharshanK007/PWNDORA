import apiClient from '@/lib/axios'
import type { LoginRequest, LoginResponse } from '@/types/auth'
import type { UserResponse } from '@/types/user'

// ─── Authentication Service ───────────────────────────────────────────────────

export const authService = {
  /**
   * Submits login credentials to the backend.
   * Expects application/x-www-form-urlencoded.
   */
  async login(credentials: LoginRequest): Promise<LoginResponse> {
    const formData = new URLSearchParams()
    formData.append('username', credentials.username)
    formData.append('password', credentials.password)

    const response = await apiClient.post<LoginResponse>('/auth/login', formData, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
    })
    return response.data
  },

  /**
   * Verifies the current token and returns the current user profile.
   * The backend uses POST /auth/test-token.
   */
  async getCurrentUser(): Promise<UserResponse> {
    const response = await apiClient.post<UserResponse>('/auth/test-token')
    return response.data
  },
}
