import { useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import { todoApi, exportApi } from '../../services/api'
import Card from '../../components/ui/Card'
import Button from '../../components/ui/Button'
import { Plus, Search, Download, Sparkles } from 'lucide-react'
import TodoItem from '../../components/todos/TodoItem'
import CreateTodoModal from '../../components/todos/CreateTodoModal'
import AdvancedFilters from '../../components/todos/AdvancedFilters'
import AITodoCreator from '../../components/todos/AITodoCreator'
import BulkOperations from '../../components/todos/BulkOperations'

export default function TodosPage() {
  const [showCreateModal, setShowCreateModal] = useState(false)
  const [showAICreator, setShowAICreator] = useState(false)
  const [searchQuery, setSearchQuery] = useState('')
  const [filters, setFilters] = useState<any>({})
  const [orderBy, setOrderBy] = useState('-created_at')
  const [selectedTodoIds, setSelectedTodoIds] = useState<number[]>([])

  const { data: todos, isLoading } = useQuery({
    queryKey: ['todos', 'all', filters, searchQuery, orderBy],
    queryFn: () => todoApi.getAllMyTodos({ 
      // user_id comes from auth token
      ...filters,
      search: searchQuery || undefined,
      order_by: orderBy
    }),
  })

  const filteredTodos = todos?.todos || []

  const handleExport = async (format: 'json' | 'csv') => {
    try {
      const params = new URLSearchParams({
        format,
        ...Object.fromEntries(
          Object.entries(filters).map(([k, v]) => [k, String(v)])
        ),
      })
      const response = await fetch(`/api/todos/export/?${params.toString()}`, {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('auth_token')}`,
        },
      })
      const blob = await response.blob()
      const url = window.URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = `todos.${format}`
      document.body.appendChild(a)
      a.click()
      window.URL.revokeObjectURL(url)
      document.body.removeChild(a)
    } catch (error) {
      console.error('Export failed:', error)
    }
  }

  return (
    <div className="space-y-6 pb-20 lg:pb-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h1 className="text-2xl sm:text-3xl font-bold text-gray-900">My Todos</h1>
          <p className="text-gray-600 mt-1">Manage all your tasks</p>
        </div>
        <div className="flex gap-2">
          <Button variant="secondary" onClick={() => setShowAICreator(!showAICreator)}>
            <Sparkles className="h-4 w-4 mr-2" />
            AI Creator
          </Button>
          <Button onClick={() => setShowCreateModal(true)}>
            <Plus className="h-4 w-4 mr-2" />
            New Todo
          </Button>
        </div>
      </div>

      {/* AI Todo Creator */}
      {showAICreator && (
        <AITodoCreator
          onSuccess={() => {
            setShowAICreator(false)
          }}
        />
      )}

      {/* Search and Sort */}
      <Card>
        <div className="space-y-4">
          <div className="flex flex-col sm:flex-row gap-4">
            <div className="relative flex-1">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 h-5 w-5" />
              <input
                type="text"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="input pl-10"
                placeholder="Search todos..."
              />
            </div>
            <div className="flex gap-2">
              <select
                value={orderBy}
                onChange={(e) => setOrderBy(e.target.value)}
                className="input"
              >
                <option value="-created_at">Newest First</option>
                <option value="created_at">Oldest First</option>
                <option value="deadline_after">Deadline (Ascending)</option>
                <option value="-deadline_after">Deadline (Descending)</option>
                <option value="priority">Priority (Low to High)</option>
                <option value="-priority">Priority (High to Low)</option>
              </select>
              <Button
                variant="secondary"
                size="sm"
                onClick={() => handleExport('json')}
              >
                <Download className="h-4 w-4 mr-2" />
                Export JSON
              </Button>
              <Button
                variant="secondary"
                size="sm"
                onClick={() => handleExport('csv')}
              >
                <Download className="h-4 w-4 mr-2" />
                Export CSV
              </Button>
            </div>
          </div>
        </div>
      </Card>

      {/* Advanced Filters */}
      <AdvancedFilters filters={filters} onFiltersChange={setFilters} />

      {/* Bulk Operations */}
      {filteredTodos.length > 0 && (
        <BulkOperations
          todos={filteredTodos}
          onSelectionChange={setSelectedTodoIds}
        />
      )}

      {/* Todos List */}
      {isLoading ? (
        <div className="text-center py-12 text-gray-500">Loading todos...</div>
      ) : filteredTodos.length === 0 ? (
        <Card>
          <div className="text-center py-12">
            <p className="text-gray-500 mb-4">No todos found</p>
            <Button onClick={() => setShowCreateModal(true)}>
              <Plus className="h-4 w-4 mr-2" />
              Create your first todo
            </Button>
          </div>
        </Card>
      ) : (
        <div className="space-y-3">
          {filteredTodos.map((todo: any) => (
            <TodoItem
              key={todo.todo_id}
              todo={todo}
              isSelected={selectedTodoIds.includes(todo.todo_id)}
              onSelect={(todoId) => {
                if (selectedTodoIds.includes(todoId)) {
                  setSelectedTodoIds(selectedTodoIds.filter(id => id !== todoId))
                } else {
                  setSelectedTodoIds([...selectedTodoIds, todoId])
                }
              }}
              showCheckbox={true}
            />
          ))}
        </div>
      )}

      {/* Create Todo Modal */}
      {showCreateModal && (
        <CreateTodoModal
          onClose={() => setShowCreateModal(false)}
          onSuccess={() => {
            setShowCreateModal(false)
            // Query will refetch automatically
          }}
        />
      )}
    </div>
  )
}

