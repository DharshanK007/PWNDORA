import { useState } from 'react'
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { AlertTriangle } from 'lucide-react'

import { AuthLayout } from '@/layouts/AuthLayout'
import { LoadingSpinner } from '@/components/common/LoadingSpinner'
import { loginSchema, type LoginFormValues } from '@/utils/validators'
import { authService } from '@/services/auth'
import { useAuth } from '@/hooks/useAuth'

// ─── Login Page ───────────────────────────────────────────────────────────────

export function LoginPage() {
  const { login } = useAuth()
  const [globalError, setGlobalError] = useState<string | null>(null)

  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm<LoginFormValues>({
    resolver: zodResolver(loginSchema),
    defaultValues: {
      username: '',
      password: '',
    },
  })

  const onSubmit = async (data: LoginFormValues) => {
    try {
      setGlobalError(null)
      // 1. Authenticate and get JWT
      const { access_token } = await authService.login(data)

      // 2. We can save the token first, but to avoid double renders, 
      // let's fetch the user immediately if possible, or just let the context do it.
      // The context's `login` function saves the token. The context will then
      // trigger `useCurrentUser` which fetches the user and updates `isAuthenticated`.
      login(access_token)
    } catch (error: unknown) {
      // 3. Handle errors securely
      const apiError = error as Record<string, string>
      const message = apiError?.detail || apiError?.message || 'Invalid credentials or server error'
      setGlobalError(message)
    }
  }

  return (
    <AuthLayout>
      <div className="space-y-6">
        <div className="space-y-1.5 text-center">
          <h2 className="text-2xl font-bold tracking-tight text-foreground">Welcome back</h2>
          <p className="text-sm text-muted-foreground">
            Sign in to your enterprise account
          </p>
        </div>

        {globalError && (
          <div className="flex items-start gap-3 rounded-lg border border-destructive/20 bg-destructive/10 p-3 text-sm text-destructive">
            <AlertTriangle className="mt-0.5 h-4 w-4 flex-shrink-0" />
            <p>{globalError}</p>
          </div>
        )}

        <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
          <div className="space-y-2">
            <label
              htmlFor="username"
              className="text-sm font-medium leading-none text-foreground peer-disabled:cursor-not-allowed peer-disabled:opacity-70"
            >
              Email Address
            </label>
            <input
              id="username"
              type="email"
              autoComplete="email"
              placeholder="admin@neofactory.com"
              className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring disabled:cursor-not-allowed disabled:opacity-50"
              {...register('username')}
            />
            {errors.username && (
              <p className="text-xs font-medium text-destructive">{errors.username.message}</p>
            )}
          </div>

          <div className="space-y-2">
            <label
              htmlFor="password"
              className="text-sm font-medium leading-none text-foreground peer-disabled:cursor-not-allowed peer-disabled:opacity-70"
            >
              Password
            </label>
            <input
              id="password"
              type="password"
              autoComplete="current-password"
              className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring disabled:cursor-not-allowed disabled:opacity-50"
              {...register('password')}
            />
            {errors.password && (
              <p className="text-xs font-medium text-destructive">{errors.password.message}</p>
            )}
          </div>

          <button
            type="submit"
            disabled={isSubmitting}
            className="inline-flex h-10 w-full items-center justify-center rounded-md bg-primary px-4 py-2 text-sm font-medium text-primary-foreground hover:bg-primary/90 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring disabled:pointer-events-none disabled:opacity-50 transition-colors"
          >
            {isSubmitting ? (
              <>
                <LoadingSpinner size="sm" className="mr-2 text-primary-foreground" />
                Signing in...
              </>
            ) : (
              'Sign In'
            )}
          </button>
        </form>
      </div>
    </AuthLayout>
  )
}
