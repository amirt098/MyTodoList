import { useQuery } from '@tanstack/react-query'
import { kanbanApi } from '../../services/api'
import Card from '../../components/ui/Card'
import { KanbanColumn, KanbanCard } from '../../types'
import { Plus } from 'lucide-react'
import Button from '../../components/ui/Button'

export default function KanbanPage() {
  const { data: board, isLoading } = useQuery({
    queryKey: ['kanban', 'board'],
    queryFn: () => kanbanApi.getBoard({ user_id: 1 }),
  })

  if (isLoading) {
    return <div className="text-center py-12 text-gray-500">Loading board...</div>
  }

  const columns = board?.columns || []
  const cards = board?.cards || []

  // Group cards by status
  const cardsByStatus = cards.reduce((acc: Record<string, KanbanCard[]>, card: KanbanCard) => {
    if (!acc[card.status]) {
      acc[card.status] = []
    }
    acc[card.status].push(card)
    return acc
  }, {})

  return (
    <div className="space-y-6 pb-20 lg:pb-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl sm:text-3xl font-bold text-gray-900">Kanban Board</h1>
          <p className="text-gray-600 mt-1">Visualize and manage your tasks</p>
        </div>
        <Button>
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
              >
                <div
                  className="rounded-lg p-3 mb-3 text-sm font-semibold text-white"
                  style={{ backgroundColor: column.color }}
                >
                  {column.name} ({columnCards.length})
                </div>
                <div className="space-y-3 min-h-[400px]">
                  {columnCards.map((card: KanbanCard) => (
                    <Card
                      key={card.todo_id}
                      className="cursor-move hover:shadow-md transition-shadow"
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
    </div>
  )
}

