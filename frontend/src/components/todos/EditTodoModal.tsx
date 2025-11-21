import { useState, useEffect } from 'react'
import { useMutation, useQueryClient, useQuery } from '@tanstack/react-query'
import { todoApi, projectApi } from '../../services/api'
import { useAuthStore } from '../../store/authStore'
import Button from '../ui/Button'
import { X } from 'lucide-react'
import { Todo } from '../../types'

interface EditTodoModalProps {
  todo: Todo
  onClose: () => void
  onSuccess: () => void
}

export default function EditTodoModal({ todo, onClose, onSuccess }: EditTodoModalProps) {
  const { user } = useAuthStore()
  const userId = user?.user_id || 1
  const [title, setTitle] = useState(todo.title)
  const [description, setDescription] = useState(todo.description || '')
  const [priority, setPriority] = useState(todo.priority)
  const [status, setStatus] = useState(todo.status)
  const [category, setCategory] = useState(todo.category || '')
  const [labels, setLabels] = useState(todo.labels?.join(', ') || '')
  const [deadline, setDeadline] = useState(
    todo.deadline_timestamp_ms
      ? new Date(todo.deadline_timestamp_ms).toISOString().slice(0, 16)
      : ''
  )
  const [selectedProjectId, setSelectedProjectId] = useState<number | null>(todo.project_id || null)
  const queryClient = useQueryClient()

  const { data: projectsResponse } = useQuery({
    queryKey: ['projects'],
    queryFn: () => projectApi.getProjects({}),
  })
  const projects = Array.isArray(projectsResponse) ? projectsResponse : projectsResponse?.projects || []

  const mutation = useMutation({
    mutationFn: (data: any) => todoApi.updateTodo(todo.todo_id, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['todo', todo.todo_id] })
      queryClient.invalidateQueries({ queryKey: ['todos'] })
      queryClient.invalidateQueries({ queryKey: ['kanban', 'board'] })
      onSuccess()
    },
  })

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    
    const labelsArray = labels.split(',').map(l => l.trim()).filter(l => l.length > 0)
    
    // Convert deadline to timestamp_ms if provided
    // UpdateTodoRequest expects deadline_timestamp_ms (number), not deadline (string)
    let deadlineTimestamp: number | null = null
    if (deadline) {
      deadlineTimestamp = new Date(deadline).getTime()
    }

    mutation.mutate({
      title,
      description,
      priority,
      status,
      category: category || null,
      labels: labelsArray.length > 0 ? labelsArray : null,
      deadline_timestamp_ms: deadlineTimestamp,
      project_id: selectedProjectId || null,
    })
  }

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-lg w-full max-w-2xl max-h-[90vh] overflow-y-auto">
        <div className="flex items-center justify-between p-4 border-b border-gray-200">
          <h2 className="text-lg font-semibold text-gray-900">Edit Todo</h2>
          <button
            onClick={onClose}
            className="p-1 text-gray-400 hover:text-gray-600"
          >
            <X className="h-5 w-5" />
          </button>
        </div>

        <form onSubmit={handleSubmit} className="p-4 space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Title *
            </label>
            <input
              type="text"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              className="input"
              placeholder="Enter todo title"
              required
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Description
            </label>
            <textarea
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              className="input min-h-[100px] resize-none"
              placeholder="Enter description (optional)"
              rows={4}
            />
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Priority
              </label>
              <select
                value={priority}
                onChange={(e) => setPriority(e.target.value)}
                className="input"
              >
                <option value="Low">Low</option>
                <option value="Medium">Medium</option>
                <option value="High">High</option>
                <option value="Critical">Critical</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Status
              </label>
              <select
                value={status}
                onChange={(e) => setStatus(e.target.value)}
                className="input"
              >
                <option value="ToDo">ToDo</option>
                <option value="In Progress">In Progress</option>
                <option value="Waiting">Waiting</option>
                <option value="Blocked">Blocked</option>
                <option value="Done">Done</option>
                <option value="Cancelled">Cancelled</option>
              </select>
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Category
            </label>
            <input
              type="text"
              value={category}
              onChange={(e) => setCategory(e.target.value)}
              className="input"
              placeholder="e.g., Work, Home, Personal"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Labels (comma-separated)
            </label>
            <input
              type="text"
              value={labels}
              onChange={(e) => setLabels(e.target.value)}
              className="input"
              placeholder="e.g., urgent, important, meeting"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Deadline
            </label>
            <input
              type="datetime-local"
              value={deadline}
              onChange={(e) => setDeadline(e.target.value)}
              className="input"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Project (optional)
            </label>
            <select
              value={selectedProjectId || ''}
              onChange={(e) => setSelectedProjectId(e.target.value ? parseInt(e.target.value) : null)}
              className="input"
            >
              <option value="">No project</option>
              {projects.map((project: any) => (
                <option key={project.project_id} value={project.project_id}>
                  {project.name}
                </option>
              ))}
            </select>
          </div>

          <div className="flex gap-3 pt-4">
            <Button
              type="button"
              variant="secondary"
              className="flex-1"
              onClick={onClose}
            >
              Cancel
            </Button>
            <Button
              type="submit"
              className="flex-1"
              disabled={mutation.isPending}
            >
              {mutation.isPending ? 'Saving...' : 'Save Changes'}
            </Button>
          </div>
        </form>
      </div>
    </div>
  )
}

