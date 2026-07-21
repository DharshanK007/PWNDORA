import type { UserResponse, RoleEnum } from './user'

// ─── Permission ───────────────────────────────────────────────────────────────

export type PermissionAction = 'read' | 'write' | 'delete' | 'admin'

export interface Permission {
  id: string
  name: string
  resource: string
  action: PermissionAction
}

// ─── Auth State ───────────────────────────────────────────────────────────────

export interface AuthState {
  user: UserResponse | null
  token: string | null
  isAuthenticated: boolean
  isInitializing: boolean
  roles: RoleEnum[]
  permissions: Permission[]
}

// ─── Login ────────────────────────────────────────────────────────────────────

export interface LoginRequest {
  username: string
  password: string
}

export interface LoginResponse {
  access_token: string
  token_type: string
}
