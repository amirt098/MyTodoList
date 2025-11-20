import { useParams, useNavigate } from 'react-router-dom'
import { useQuery } from '@tanstack/react-query'
import { todoApi, subtaskApi } from '../../services/api'
import Card from '../../components/ui/Card'
import Button from '../../components/ui/Button'
import { ArrowLeft, Edit, Trash2 } from 'lucide-react'
import SubtaskList from '../../components/todos/SubtaskList'

export default function TodoDetailPage() {
  const { id } = useParams<{ id: string }>()
  const navigate = useNavigate()
  const todoId = parseInt(id || '0')

  const { data: todo, isLoading } = useQuery({
    queryKey: ['todo', todoId],
    queryFn: () => todoApi.getTodo(todoId, { user_id: 1 }),
    enabled: !!todoId,
  })

  const { data: subtasks } = useQuery({
    queryKey: ['subtasks', todoId],
    queryFn: () => subtaskApi.getSubtasks(todoId, { user_id: 1 }),
    enabled: !!todoId,
  })

  if (isLoading) {
    return (
      <div className="text-center py-12 text-gray-500">Loading...</div>
    )
  }

  if (!todo) {
    return (
      <div className="text-center py-12">
        <p className="text-gray-500 mb-4">Todo not found</p>
        <Button onClick={() => navigate('/todos')}>Back to Todos</Button>
      </div>
    )
  }

  return (
    <div className="space-y-6 pb-20 lg:pb-6">
      {/* Header */}
      <div className="flex items-center gap-4">
        <Button variant="ghost" size="sm" onClick={() => navigate('/todos')}>
          <ArrowLeft className="h-4 w-4 mr-2" />
          Back
        </Button>
        <div className="flex-1">
          <h1 className="text-2xl sm:text-3xl font-bold text-gray-900">{todo.title}</h1>
        </div>
        <div className="flex gap-2">
          <Button variant="ghost" size="sm">
            <Edit className="h-4 w-4" />
          </Button>
          <Button variant="ghost" size="sm">
            <Trash2 className="h-4 w-4 text-red-600" />
          </Button>
        </div>
      </div>

      {/* Todo Details */}
      <Card>
        <div className="space-y-4">
          {todo.description && (
            <div>
              <h3 className="text-sm font-medium text-gray-700 mb-2">Description</h3>
              <p className="text-gray-900">{todo.description}</p>
            </div>
          )}

          <div className="grid grid-cols-2 gap-4">
            <div>
              <h3 className="text-sm font-medium text-gray-700 mb-2">Priority</h3>
              <span className={`inline-block px-3 py-1 rounded-full text-sm font-medium ${
                todo.priority === 'Critical' ? 'bg-red-100 text-red-700' :
                todo.priority === 'High' ? 'bg-orange-100 text-orange-700' :
                todo.priority === 'Medium' ? 'bg-yellow-100 text-yellow-700' :
                'bg-gray-100 text-gray-700'
              }`}>
                {todo.priority}
              </span>
            </div>

            <div>
              <h3 className="text-sm font-medium text-gray-700 mb-2">Status</h3>
              <span className={`inline-block px-3 py-1 rounded-full text-sm font-medium ${
                todo.status === 'Done' ? 'bg-green-100 text-green-700' :
                todo.status === 'In Progress' ? 'bg-blue-100 text-blue-700' :
                'bg-gray-100 text-gray-700'
              }`}>
                {todo.status}
              </span>
            </div>

            {todo.category && (
              <div>
                <h3 className="text-sm font-medium text-gray-700 mb-2">Category</h3>
                <p className="text-gray-900">{todo.category}</p>
              </div>
            )}

            {todo.deadline_timestamp_ms && (
              <div>
                <h3 className="text-sm font-medium text-gray-700 mb-2">Deadline</h3>
                <p className="text-gray-900">
                  {new Date(todo.deadline_timestamp_ms).toLocaleDateString()}
                </p>
              </div>
            )}
          </div>

          {todo.labels && todo.labels.length > 0 && (
            <div>
              <h3 className="text-sm font-medium text-gray-700 mb-2">Labels</h3>
              <div className="flex flex-wrap gap-2">
                {todo.labels.map((label: string, index: number) => (
                  <span
                    key={index}
                    className="px-2 py-1 bg-gray-100 text-gray-700 rounded text-sm"
                  >
                    {label}
                  </span>
                ))}
              </div>
            </div>
          )}

          {todo.progress > 0 && (
            <div>
              <h3 className="text-sm font-medium text-gray-700 mb-2">Progress</h3>
              <div className="w-full bg-gray-200 rounded-full h-2">
                <div
                  className="bg-primary-600 h-2 rounded-full transition-all"
                  style={{ width: `${todo.progress}%` }}
                ></div>
              </div>
              <p className="text-sm text-gray-600 mt-1">{todo.progress}% complete</p>
            </div>
          )}
        </div>
      </Card>

      {/* Subtasks */}
      {subtasks && (
        <Card>
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Subtasks</h2>
          <SubtaskList todoId={todoId} subtasks={subtasks.subtasks || []} />
        </Card>
      )}
    </div>
  )
}

