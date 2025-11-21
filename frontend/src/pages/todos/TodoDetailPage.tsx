import { useState } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { todoApi, subtaskApi, dependencyApi } from '../../services/api'
import Card from '../../components/ui/Card'
import Button from '../../components/ui/Button'
import { ArrowLeft, Edit, Trash2, Link2 } from 'lucide-react'
import SubtaskList from '../../components/todos/SubtaskList'
import EditTodoModal from '../../components/todos/EditTodoModal'
import ReminderManager from '../../components/todos/ReminderManager'

export default function TodoDetailPage() {
  const { id } = useParams<{ id: string }>()
  const navigate = useNavigate()
  const todoId = parseInt(id || '0')
  const [showEditModal, setShowEditModal] = useState(false)
  const queryClient = useQueryClient()

  const { data: todo, isLoading } = useQuery({
    queryKey: ['todo', todoId],
    queryFn: () => todoApi.getTodo(todoId, {}), // user_id comes from auth token
    enabled: !!todoId,
  })

  const { data: subtasks } = useQuery({
    queryKey: ['subtasks', todoId],
    queryFn: () => subtaskApi.getSubtasks(todoId, {}), // user_id comes from auth token
    enabled: !!todoId,
  })

  const { data: dependencyChain } = useQuery({
    queryKey: ['dependency-chain', todoId],
    queryFn: () => dependencyApi.getDependencyChain(todoId, {}),
    enabled: !!todoId,
  })

  const deleteMutation = useMutation({
    mutationFn: () => todoApi.deleteTodo(todoId),
    onSuccess: () => {
      navigate('/todos')
    },
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
          <Button variant="ghost" size="sm" onClick={() => setShowEditModal(true)}>
            <Edit className="h-4 w-4" />
          </Button>
          <Button
            variant="ghost"
            size="sm"
            onClick={() => {
              if (confirm('Are you sure you want to delete this todo?')) {
                deleteMutation.mutate()
              }
            }}
            disabled={deleteMutation.isPending}
          >
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

      {/* Dependencies */}
      {dependencyChain && (dependencyChain.previous_todos?.length > 0 || dependencyChain.next_todos?.length > 0) && (
        <Card>
          <div className="flex items-center gap-2 mb-4">
            <Link2 className="h-5 w-5 text-primary-600" />
            <h2 className="text-lg font-semibold text-gray-900">Dependencies</h2>
          </div>
          <div className="space-y-3">
            {dependencyChain.previous_todos && dependencyChain.previous_todos.length > 0 && (
              <div>
                <h3 className="text-sm font-medium text-gray-700 mb-2">Depends On:</h3>
                <div className="space-y-2">
                  {dependencyChain.previous_todos.map((prevTodo: any) => (
                    <div
                      key={prevTodo.todo_id}
                      className="p-2 bg-gray-50 rounded border border-gray-200"
                    >
                      <a
                        href={`/todos/${prevTodo.todo_id}`}
                        className="text-sm text-primary-600 hover:text-primary-700 font-medium"
                      >
                        {prevTodo.title}
                      </a>
                      <span className={`ml-2 text-xs px-2 py-1 rounded-full ${
                        prevTodo.status === 'Done' ? 'bg-green-100 text-green-700' : 'bg-yellow-100 text-yellow-700'
                      }`}>
                        {prevTodo.status}
                      </span>
                    </div>
                  ))}
                </div>
              </div>
            )}
            {dependencyChain.next_todos && dependencyChain.next_todos.length > 0 && (
              <div>
                <h3 className="text-sm font-medium text-gray-700 mb-2">Blocks:</h3>
                <div className="space-y-2">
                  {dependencyChain.next_todos.map((nextTodo: any) => (
                    <div
                      key={nextTodo.todo_id}
                      className="p-2 bg-gray-50 rounded border border-gray-200"
                    >
                      <a
                        href={`/todos/${nextTodo.todo_id}`}
                        className="text-sm text-primary-600 hover:text-primary-700 font-medium"
                      >
                        {nextTodo.title}
                      </a>
                      <span className={`ml-2 text-xs px-2 py-1 rounded-full ${
                        nextTodo.status === 'Done' ? 'bg-green-100 text-green-700' : 'bg-yellow-100 text-yellow-700'
                      }`}>
                        {nextTodo.status}
                      </span>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        </Card>
      )}

      {/* Subtasks */}
      {subtasks && (
        <Card>
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Subtasks</h2>
          <SubtaskList todoId={todoId} subtasks={subtasks.subtasks || []} />
        </Card>
      )}

      {/* Reminders */}
      <ReminderManager todoId={todoId} />

      {/* Edit Modal */}
      {showEditModal && todo && (
        <EditTodoModal
          todo={todo}
          onClose={() => setShowEditModal(false)}
          onSuccess={() => {
            setShowEditModal(false)
            queryClient.invalidateQueries({ queryKey: ['todo', todoId] })
          }}
        />
      )}
    </div>
  )
}

