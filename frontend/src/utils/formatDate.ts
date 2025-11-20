import { format, formatDistanceToNow } from 'date-fns'

export function formatTimestamp(timestamp: number): string {
  return format(new Date(timestamp), 'MMM dd, yyyy')
}

export function formatDateTime(timestamp: number): string {
  return format(new Date(timestamp), 'MMM dd, yyyy HH:mm')
}

export function formatRelativeTime(timestamp: number): string {
  return formatDistanceToNow(new Date(timestamp), { addSuffix: true })
}

export function formatTime(timestamp: number): string {
  return format(new Date(timestamp), 'HH:mm')
}

