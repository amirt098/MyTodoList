import { useState } from 'react'
import { useMutation, useQueryClient } from '@tanstack/react-query'
import { subtaskApi } from '../../services/api'
import { Subtask } from '../../types'
import { Check, Plus, X } from 'lucide-react'
import Button from '../ui/Button'

interface SubtaskListProps {
  todoId: number
  subtasks: Subtask[]
}

export default function SubtaskList({ todoId, subtasks }: SubtaskListProps) {
  const [newSubtaskTitle, setNewSubtaskTitle] = useState('')
  const [showAddForm, setShowAddForm] = useState(false)
  const queryClient = useQueryClient()

  const addMutation = useMutation({
    mutationFn: (data: any) => subtaskApi.addSubtask(todoId, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['subtasks', todoId] })
      setNewSubtaskTitle('')
      setShowAddForm(false)
    },
  })

  const toggleMutation = useMutation({
    mutationFn: ({ subtaskId, done }: { subtaskId: number; done: boolean }) =>
      subtaskApi.markSubtaskDone(subtaskId, { todo_id: todoId, done }), // user_id comes from auth token
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['subtasks', todoId] })
    },
  })

  const handleAdd = (e: React.FormEvent) => {
    e.preventDefault()
    if (newSubtaskTitle.trim()) {
      addMutation.mutate({
        title: newSubtaskTitle.trim(),
        // user_id comes from auth token
      })
    }
  }

  return (
    <div className="space-y-3">
      {subtasks.map((subtask) => (
        <div
          key={subtask.subtask_id}
          className="flex items-center gap-3 p-3 rounded-lg border border-gray-200"
        >
          <button
            onClick={() =>
              toggleMutation.mutate({
                subtaskId: subtask.subtask_id,
                done: subtask.status !== 'Done',
              })
            }
            className={`flex-shrink-0 h-5 w-5 rounded border-2 flex items-center justify-center transition-colors ${
              subtask.status === 'Done'
                ? 'bg-green-600 border-green-600'
                : 'border-gray-300 hover:border-green-600'
            }`}
          >
            {subtask.status === 'Done' && <Check className="h-3 w-3 text-white" />}
          </button>
          <span
            className={`flex-1 ${
              subtask.status === 'Done' ? 'line-through text-gray-500' : 'text-gray-900'
            }`}
          >
            {subtask.title}
          </span>
        </div>
      ))}

      {showAddForm ? (
        <form onSubmit={handleAdd} className="flex items-center gap-2">
          <input
            type="text"
            value={newSubtaskTitle}
            onChange={(e) => setNewSubtaskTitle(e.target.value)}
            className="input flex-1"
            placeholder="Add subtask..."
            autoFocus
          />
          <Button type="submit" size="sm" disabled={addMutation.isPending}>
            Add
          </Button>
          <button
            type="button"
            onClick={() => {
              setShowAddForm(false)
              setNewSubtaskTitle('')
            }}
            className="p-2 text-gray-400 hover:text-gray-600"
          >
            <X className="h-4 w-4" />
          </button>
        </form>
      ) : (
        <button
          onClick={() => setShowAddForm(true)}
          className="flex items-center gap-2 text-sm text-primary-600 hover:text-primary-700 font-medium"
        >
          <Plus className="h-4 w-4" />
          Add subtask
        </button>
      )}
    </div>
  )
}

