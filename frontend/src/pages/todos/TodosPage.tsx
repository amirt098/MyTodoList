import { useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import { todoApi } from '../../services/api'
import Card from '../../components/ui/Card'
import Button from '../../components/ui/Button'
import { Plus, Filter, Search } from 'lucide-react'
import TodoItem from '../../components/todos/TodoItem'
import CreateTodoModal from '../../components/todos/CreateTodoModal'

export default function TodosPage() {
  const [showCreateModal, setShowCreateModal] = useState(false)
  const [searchQuery, setSearchQuery] = useState('')
  const [statusFilter, setStatusFilter] = useState<string>('all')

  const { data: todos, isLoading } = useQuery({
    queryKey: ['todos', 'all', statusFilter, searchQuery],
    queryFn: () => todoApi.getAllMyTodos({ 
      user_id: 1,
      status: statusFilter !== 'all' ? statusFilter : undefined,
      search: searchQuery || undefined
    }),
  })

  const filteredTodos = todos?.todos || []

  return (
    <div className="space-y-6 pb-20 lg:pb-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h1 className="text-2xl sm:text-3xl font-bold text-gray-900">My Todos</h1>
          <p className="text-gray-600 mt-1">Manage all your tasks</p>
        </div>
        <Button onClick={() => setShowCreateModal(true)}>
          <Plus className="h-4 w-4 mr-2" />
          New Todo
        </Button>
      </div>

      {/* Filters */}
      <Card>
        <div className="space-y-4">
          {/* Search */}
          <div className="relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 h-5 w-5" />
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="input pl-10"
              placeholder="Search todos..."
            />
          </div>

          {/* Status Filter */}
          <div className="flex items-center gap-2 flex-wrap">
            <Filter className="h-4 w-4 text-gray-500" />
            <span className="text-sm text-gray-600">Status:</span>
            {['all', 'ToDo', 'In Progress', 'Done'].map((status) => (
              <button
                key={status}
                onClick={() => setStatusFilter(status)}
                className={`px-3 py-1 rounded-full text-sm font-medium transition-colors ${
                  statusFilter === status
                    ? 'bg-primary-600 text-white'
                    : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                }`}
              >
                {status}
              </button>
            ))}
          </div>
        </div>
      </Card>

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
            <TodoItem key={todo.todo_id} todo={todo} />
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

