import { type ClassValue, clsx } from 'clsx'
import { twMerge } from 'tailwind-merge'

// ─── shadcn/ui utility ────────────────────────────────────────────────────────
// Merges Tailwind class names intelligently, resolving conflicts.

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}
