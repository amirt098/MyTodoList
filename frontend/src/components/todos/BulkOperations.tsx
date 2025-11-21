import { useState } from 'react'
import { useMutation, useQueryClient } from '@tanstack/react-query'
import { bulkApi } from '../../services/api'
import { useAuthStore } from '../../store/authStore'
import Button from '../ui/Button'
import { Trash2, Edit, CheckSquare, Square } from 'lucide-react'

interface BulkOperationsProps {
  todos: any[]
  onSelectionChange?: (selectedIds: number[]) => void
}

export default function BulkOperations({ todos, onSelectionChange }: BulkOperationsProps) {
  const { user } = useAuthStore()
  const userId = user?.user_id || 1
  const [selectedIds, setSelectedIds] = useState<Set<number>>(new Set())
  const queryClient = useQueryClient()

  const bulkUpdateMutation = useMutation({
    mutationFn: (data: any) => bulkApi.bulkUpdate(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['todos'] })
      queryClient.invalidateQueries({ queryKey: ['kanban', 'board'] })
      setSelectedIds(new Set())
      onSelectionChange?.([])
    },
  })

  const bulkDeleteMutation = useMutation({
    mutationFn: (data: any) => bulkApi.bulkDelete(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['todos'] })
      queryClient.invalidateQueries({ queryKey: ['kanban', 'board'] })
      setSelectedIds(new Set())
      onSelectionChange?.([])
    },
  })

  const toggleSelect = (todoId: number) => {
    const newSet = new Set(selectedIds)
    if (newSet.has(todoId)) {
      newSet.delete(todoId)
    } else {
      newSet.add(todoId)
    }
    setSelectedIds(newSet)
    onSelectionChange?.(Array.from(newSet))
  }

  const toggleSelectAll = () => {
    if (selectedIds.size === todos.length) {
      setSelectedIds(new Set())
      onSelectionChange?.([])
    } else {
      const allIds = new Set(todos.map(t => t.todo_id))
      setSelectedIds(allIds)
      onSelectionChange?.(Array.from(allIds))
    }
  }

  const handleBulkUpdate = (updates: any) => {
    bulkUpdateMutation.mutate({
      todo_ids: Array.from(selectedIds),
      updates,
      user_id: userId,
    })
  }

  const handleBulkDelete = () => {
    if (!confirm(`Are you sure you want to delete ${selectedIds.size} todo(s)?`)) return
    bulkDeleteMutation.mutate({
      todo_ids: Array.from(selectedIds),
      user_id: userId,
    })
  }

  if (selectedIds.size === 0) {
    return (
      <div className="flex items-center gap-2">
        <button
          onClick={toggleSelectAll}
          className="p-2 text-gray-500 hover:text-gray-700"
          title="Select all"
        >
          <Square className="h-5 w-5" />
        </button>
        <span className="text-sm text-gray-600">Select todos for bulk operations</span>
      </div>
    )
  }

  return (
    <div className="flex items-center gap-4 p-3 bg-primary-50 rounded-lg border border-primary-200">
      <div className="flex items-center gap-2">
        <button
          onClick={toggleSelectAll}
          className="p-1 text-primary-600 hover:text-primary-700"
        >
          <CheckSquare className="h-5 w-5" />
        </button>
        <span className="text-sm font-medium text-primary-900">
          {selectedIds.size} todo(s) selected
        </span>
      </div>

      <div className="flex items-center gap-2 flex-1">
        <select
          className="input text-sm"
          onChange={(e) => {
            if (e.target.value) {
              handleBulkUpdate({ status: e.target.value })
              e.target.value = ''
            }
          }}
          defaultValue=""
        >
          <option value="">Change Status...</option>
          <option value="ToDo">ToDo</option>
          <option value="In Progress">In Progress</option>
          <option value="Waiting">Waiting</option>
          <option value="Blocked">Blocked</option>
          <option value="Done">Done</option>
          <option value="Cancelled">Cancelled</option>
        </select>

        <select
          className="input text-sm"
          onChange={(e) => {
            if (e.target.value) {
              handleBulkUpdate({ priority: e.target.value })
              e.target.value = ''
            }
          }}
          defaultValue=""
        >
          <option value="">Change Priority...</option>
          <option value="Low">Low</option>
          <option value="Medium">Medium</option>
          <option value="High">High</option>
          <option value="Critical">Critical</option>
        </select>
      </div>

      <Button
        variant="secondary"
        size="sm"
        onClick={handleBulkDelete}
        disabled={bulkDeleteMutation.isPending}
      >
        <Trash2 className="h-4 w-4 mr-2" />
        Delete ({selectedIds.size})
      </Button>

      <Button
        variant="ghost"
        size="sm"
        onClick={() => {
          setSelectedIds(new Set())
          onSelectionChange?.([])
        }}
      >
        Clear Selection
      </Button>
    </div>
  )
}

