import { z } from 'zod'

// ─── Common Zod Schemas ───────────────────────────────────────────────────────

export const emailSchema = z
  .string()
  .min(1, 'Email is required')
  .email('Please enter a valid email address')

export const passwordSchema = z
  .string()
  .min(8, 'Password must be at least 8 characters')
  .max(128, 'Password is too long')

export const uuidSchema = z
  .string()
  .uuid('Invalid UUID format')

export const requiredStringSchema = (field: string) =>
  z.string().min(1, `${field} is required`)

export const optionalStringSchema = z.string().optional()

export const pageSizeSchema = z
  .number()
  .int()
  .min(1)
  .max(100)
  .default(25)

// ─── Login Schema ─────────────────────────────────────────────────────────────

export const loginSchema = z.object({
  username: emailSchema,
  password: passwordSchema,
})

export type LoginFormValues = z.infer<typeof loginSchema>
