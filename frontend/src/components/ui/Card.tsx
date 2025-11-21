import { ReactNode } from 'react'
import { cn } from '../../utils/cn'

interface CardProps {
  children: ReactNode
  className?: string
  onClick?: () => void
  draggable?: boolean
  onDragStart?: (e: React.DragEvent) => void
  onDragEnd?: (e: React.DragEvent) => void
}

export default function Card({ children, className, onClick, draggable, onDragStart, onDragEnd }: CardProps) {
  return (
    <div
      className={cn('card', onClick && 'cursor-pointer hover:shadow-md transition-shadow', className)}
      onClick={onClick}
      draggable={draggable}
      onDragStart={onDragStart}
      onDragEnd={onDragEnd}
    >
      {children}
    </div>
  )
}

