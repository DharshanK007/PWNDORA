export type LogLevel = 'info' | 'warn' | 'error' | 'debug'

export interface LogEntry {
  timestamp: string
  module: string
  action: string
  level: LogLevel
  message: string
  metadata?: Record<string, unknown>
}

class Logger {
  private formatLog(entry: Omit<LogEntry, 'timestamp'>): LogEntry {
    return {
      ...entry,
      timestamp: new Date().toISOString()
    }
  }

  private write(entry: LogEntry) {
    // In development, output to console.
    // In production, this could send to a telemetry/monitoring endpoint.
    const output = `[${entry.timestamp}] [${entry.level.toUpperCase()}] [${entry.module}] [${entry.action}] ${entry.message}`
    
    switch (entry.level) {
      case 'info':
        console.info(output, entry.metadata || '')
        break
      case 'warn':
        console.warn(output, entry.metadata || '')
        break
      case 'error':
        console.error(output, entry.metadata || '')
        break
      case 'debug':
        if (process.env.NODE_ENV === 'development') {
          console.debug(output, entry.metadata || '')
        }
        break
    }
  }

  info(module: string, action: string, message: string, metadata?: Record<string, unknown>) {
    this.write(this.formatLog({ module, action, level: 'info', message, metadata }))
  }

  warn(module: string, action: string, message: string, metadata?: Record<string, unknown>) {
    this.write(this.formatLog({ module, action, level: 'warn', message, metadata }))
  }

  error(module: string, action: string, message: string, metadata?: Record<string, unknown>) {
    this.write(this.formatLog({ module, action, level: 'error', message, metadata }))
  }

  debug(module: string, action: string, message: string, metadata?: Record<string, unknown>) {
    this.write(this.formatLog({ module, action, level: 'debug', message, metadata }))
  }
}

export const logger = new Logger()
