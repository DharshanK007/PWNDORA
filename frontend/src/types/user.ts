

// ─── Backend User Schema ──────────────────────────────────────────────────────

export type RoleEnum = 'Employee' | 'Engineer' | 'Manager' | 'Administrator'

export interface UserResponse {
  id: string
  email: string
  role: RoleEnum
  created_at: string
  updated_at: string
}
