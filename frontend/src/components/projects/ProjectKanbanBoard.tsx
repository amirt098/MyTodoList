import { useState } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { kanbanApi } from '../../services/api'
import Card from '../ui/Card'
import { KanbanColumn, KanbanCard } from '../../types'
import { Plus } from 'lucide-react'
import Button from '../ui/Button'
import CreateTodoModal from '../todos/CreateTodoModal'

interface ProjectKanbanBoardProps {
  projectId: number
  userId: number
}

export default function ProjectKanbanBoard({ projectId, userId }: ProjectKanbanBoardProps) {
  const queryClient = useQueryClient()
  const [draggedCard, setDraggedCard] = useState<KanbanCard | null>(null)
  const [draggedOverColumn, setDraggedOverColumn] = useState<string | null>(null)
  const [showCreateModal, setShowCreateModal] = useState(false)

  const { data: board, isLoading } = useQuery({
    queryKey: ['kanban', 'board', projectId],
    queryFn: () => kanbanApi.getBoard({ project_id: projectId }), // user_id comes from auth token
  })

  const moveTodoMutation = useMutation({
    mutationFn: (data: { todo_id: number; new_status: string; user_id: number; new_order?: number }) =>
      kanbanApi.moveTodo(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['kanban', 'board', projectId] })
      queryClient.invalidateQueries({ queryKey: ['todos', 'project', projectId] })
    },
  })

  if (isLoading) {
    return <div className="text-center py-12 text-gray-500">Loading board...</div>
  }

  const columns = (board as any)?.columns || []
  const cards = (board as any)?.cards || []

  // Group cards by status
  const cardsByStatus = cards.reduce((acc: Record<string, KanbanCard[]>, card: KanbanCard) => {
    if (!acc[card.status]) {
      acc[card.status] = []
    }
    acc[card.status].push(card)
    return acc
  }, {})

  const handleDragStart = (e: React.DragEvent, card: KanbanCard) => {
    setDraggedCard(card)
    e.dataTransfer.effectAllowed = 'move'
    e.dataTransfer.setData('text/plain', card.todo_id.toString())
    if (e.currentTarget instanceof HTMLElement) {
      e.currentTarget.style.opacity = '0.5'
    }
  }

  const handleDragOver = (e: React.DragEvent, statusValue: string) => {
    e.preventDefault()
    e.stopPropagation()
    e.dataTransfer.dropEffect = 'move'
    setDraggedOverColumn(statusValue)
  }

  const handleDragLeave = () => {
    setDraggedOverColumn(null)
  }

  const handleDrop = (e: React.DragEvent, targetColumn: KanbanColumn) => {
    e.preventDefault()
    e.stopPropagation()
    setDraggedOverColumn(null)

    if (!draggedCard || draggedCard.status === targetColumn.status_value) {
      setDraggedCard(null)
      return
    }

    moveTodoMutation.mutate({
      todo_id: draggedCard.todo_id,
      new_status: targetColumn.status_value,
      user_id: userId, // user_id comes from auth token
    })

    setDraggedCard(null)
  }

  const handleDragEnd = (e: React.DragEvent) => {
    if (e.currentTarget instanceof HTMLElement) {
      e.currentTarget.style.opacity = '1'
    }
    setDraggedCard(null)
    setDraggedOverColumn(null)
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <p className="text-gray-600">Project Kanban Board</p>
        <Button onClick={() => setShowCreateModal(true)}>
          <Plus className="h-4 w-4 mr-2" />
          New Todo
        </Button>
      </div>

      {/* Kanban Board */}
      <div className="overflow-x-auto">
        <div className="flex gap-4 min-w-max pb-4">
          {columns.map((column: KanbanColumn) => {
            const columnCards = cardsByStatus[column.status_value] || []
            return (
              <div
                key={column.column_id || column.name}
                className="flex-shrink-0 w-72"
                onDragOver={(e) => handleDragOver(e, column.status_value)}
                onDragLeave={handleDragLeave}
                onDrop={(e) => handleDrop(e, column)}
              >
                <div
                  className="rounded-lg p-3 mb-3 text-sm font-semibold text-white"
                  style={{ backgroundColor: column.color }}
                >
                  {column.name} ({columnCards.length})
                </div>
                <div
                  className={`space-y-3 min-h-[400px] transition-colors ${
                    draggedOverColumn === column.status_value
                      ? 'bg-primary-50 rounded-lg p-2'
                      : ''
                  }`}
                >
                  {columnCards.map((card: KanbanCard) => (
                    <Card
                      key={card.todo_id}
                      draggable
                      onDragStart={(e) => handleDragStart(e, card)}
                      onDragEnd={handleDragEnd}
                      className="cursor-move hover:shadow-md transition-shadow active:opacity-50"
                    >
                      <h3 className="font-medium text-gray-900 mb-2">{card.title}</h3>
                      {card.description && (
                        <p className="text-sm text-gray-600 mb-3 line-clamp-2">
                          {card.description}
                        </p>
                      )}
                      <div className="flex items-center gap-2 flex-wrap">
                        <span className={`text-xs px-2 py-1 rounded-full ${
                          card.priority === 'Critical' ? 'bg-red-100 text-red-700' :
                          card.priority === 'High' ? 'bg-orange-100 text-orange-700' :
                          card.priority === 'Medium' ? 'bg-yellow-100 text-yellow-700' :
                          'bg-gray-100 text-gray-700'
                        }`}>
                          {card.priority}
                        </span>
                        {card.progress > 0 && (
                          <span className="text-xs text-gray-500">
                            {card.progress}%
                          </span>
                        )}
                      </div>
                    </Card>
                  ))}
                </div>
              </div>
            )
          })}
        </div>
      </div>

      {/* Create Todo Modal */}
      {showCreateModal && (
        <CreateTodoModal
          onClose={() => setShowCreateModal(false)}
          onSuccess={() => {
            setShowCreateModal(false)
            queryClient.invalidateQueries({ queryKey: ['kanban', 'board', projectId] })
            queryClient.invalidateQueries({ queryKey: ['todos', 'project', projectId] })
          }}
          projectId={projectId}
        />
      )}
    </div>
  )
}

