import { useQuery } from '@tanstack/react-query'
import { todoApi } from '../../services/api'
import Card from '../../components/ui/Card'
import Button from '../../components/ui/Button'
import { Plus, CheckCircle2, Clock, AlertCircle, TrendingUp } from 'lucide-react'
import { formatRelativeTime } from '../../utils/formatDate'
import { Link } from 'react-router-dom'

export default function DashboardPage() {
  const { data: todos, isLoading } = useQuery({
    queryKey: ['todos', 'all'],
    queryFn: () => todoApi.getAllMyTodos({ user_id: 1 }),
  })

  const stats = {
    total: todos?.total || 0,
    completed: todos?.todos?.filter((t: any) => t.status === 'Done').length || 0,
    inProgress: todos?.todos?.filter((t: any) => t.status === 'In Progress').length || 0,
    overdue: todos?.todos?.filter((t: any) => {
      if (!t.deadline_timestamp_ms) return false
      return new Date(t.deadline_timestamp_ms) < new Date() && t.status !== 'Done'
    }).length || 0,
  }

  const recentTodos = todos?.todos?.slice(0, 5) || []

  return (
    <div className="space-y-6 pb-20 lg:pb-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h1 className="text-2xl sm:text-3xl font-bold text-gray-900">Dashboard</h1>
          <p className="text-gray-600 mt-1">Overview of your tasks and progress</p>
        </div>
        <Link to="/todos">
          <Button>
            <Plus className="h-4 w-4 mr-2" />
            New Todo
          </Button>
        </Link>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        <Card>
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600">Total Todos</p>
              <p className="text-2xl font-bold text-gray-900">{stats.total}</p>
            </div>
            <div className="h-12 w-12 rounded-full bg-primary-100 flex items-center justify-center">
              <TrendingUp className="h-6 w-6 text-primary-600" />
            </div>
          </div>
        </Card>

        <Card>
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600">Completed</p>
              <p className="text-2xl font-bold text-green-600">{stats.completed}</p>
            </div>
            <div className="h-12 w-12 rounded-full bg-green-100 flex items-center justify-center">
              <CheckCircle2 className="h-6 w-6 text-green-600" />
            </div>
          </div>
        </Card>

        <Card>
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600">In Progress</p>
              <p className="text-2xl font-bold text-blue-600">{stats.inProgress}</p>
            </div>
            <div className="h-12 w-12 rounded-full bg-blue-100 flex items-center justify-center">
              <Clock className="h-6 w-6 text-blue-600" />
            </div>
          </div>
        </Card>

        <Card>
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600">Overdue</p>
              <p className="text-2xl font-bold text-red-600">{stats.overdue}</p>
            </div>
            <div className="h-12 w-12 rounded-full bg-red-100 flex items-center justify-center">
              <AlertCircle className="h-6 w-6 text-red-600" />
            </div>
          </div>
        </Card>
      </div>

      {/* Recent Todos */}
      <Card>
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-lg font-semibold text-gray-900">Recent Todos</h2>
          <Link to="/todos" className="text-sm text-primary-600 hover:text-primary-700">
            View all
          </Link>
        </div>

        {isLoading ? (
          <div className="text-center py-8 text-gray-500">Loading...</div>
        ) : recentTodos.length === 0 ? (
          <div className="text-center py-8 text-gray-500">
            <p>No todos yet</p>
            <Link to="/todos">
              <Button variant="primary" size="sm" className="mt-4">
                Create your first todo
              </Button>
            </Link>
          </div>
        ) : (
          <div className="space-y-3">
            {recentTodos.map((todo: any) => (
              <Link
                key={todo.todo_id}
                to={`/todos/${todo.todo_id}`}
                className="block p-3 rounded-lg hover:bg-gray-50 transition-colors border border-gray-100"
              >
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <h3 className="font-medium text-gray-900">{todo.title}</h3>
                    {todo.description && (
                      <p className="text-sm text-gray-600 mt-1 line-clamp-1">{todo.description}</p>
                    )}
                    <div className="flex items-center gap-2 mt-2">
                      <span className={`text-xs px-2 py-1 rounded-full ${
                        todo.priority === 'Critical' ? 'bg-red-100 text-red-700' :
                        todo.priority === 'High' ? 'bg-orange-100 text-orange-700' :
                        todo.priority === 'Medium' ? 'bg-yellow-100 text-yellow-700' :
                        'bg-gray-100 text-gray-700'
                      }`}>
                        {todo.priority}
                      </span>
                      <span className={`text-xs px-2 py-1 rounded-full ${
                        todo.status === 'Done' ? 'bg-green-100 text-green-700' :
                        todo.status === 'In Progress' ? 'bg-blue-100 text-blue-700' :
                        'bg-gray-100 text-gray-700'
                      }`}>
                        {todo.status}
                      </span>
                    </div>
                  </div>
                  {todo.deadline_timestamp_ms && (
                    <span className="text-xs text-gray-500 ml-4">
                      {formatRelativeTime(todo.deadline_timestamp_ms)}
                    </span>
                  )}
                </div>
              </Link>
            ))}
          </div>
        )}
      </Card>
    </div>
  )
}

