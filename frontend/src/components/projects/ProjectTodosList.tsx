import { useState } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { todoApi } from '../../services/api'
import Card from '../ui/Card'
import Button from '../ui/Button'
import { Plus } from 'lucide-react'
import CreateTodoModal from '../todos/CreateTodoModal'
import TodoItem from '../todos/TodoItem'

interface ProjectTodosListProps {
  projectId: number
  userId: number
}

export default function ProjectTodosList({ projectId, userId }: ProjectTodosListProps) {
  const queryClient = useQueryClient()
  const [showCreateModal, setShowCreateModal] = useState(false)

  const { data: response, isLoading } = useQuery({
    queryKey: ['todos', 'project', projectId],
    queryFn: () => todoApi.getTodos({ project_id: projectId }), // user_id comes from auth token
  })

  const todos = response?.todos || []

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <p className="text-gray-600">Project Todos</p>
        <Button onClick={() => setShowCreateModal(true)}>
          <Plus className="h-4 w-4 mr-2" />
          New Todo
        </Button>
      </div>

      {isLoading ? (
        <div className="text-center py-12 text-gray-500">Loading todos...</div>
      ) : todos.length === 0 ? (
        <Card>
          <div className="text-center py-12">
            <p className="text-gray-500 mb-4">No todos in this project yet</p>
            <Button onClick={() => setShowCreateModal(true)}>
              <Plus className="h-4 w-4 mr-2" />
              Create your first todo
            </Button>
          </div>
        </Card>
      ) : (
        <div className="space-y-3">
          {todos.map((todo: any) => (
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
            queryClient.invalidateQueries({ queryKey: ['todos', 'project', projectId] })
            queryClient.invalidateQueries({ queryKey: ['kanban', 'board', projectId] })
          }}
          projectId={projectId}
        />
      )}
    </div>
  )
}

