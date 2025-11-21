import { useState } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { reminderApi } from '../../services/api'
import { useAuthStore } from '../../store/authStore'
import Card from '../ui/Card'
import Button from '../ui/Button'
import { Bell, Plus, Edit, Trash2, Clock } from 'lucide-react'
import { Reminder } from '../../types'

interface ReminderManagerProps {
  todoId?: number
}

export default function ReminderManager({ todoId }: ReminderManagerProps) {
  const { user } = useAuthStore()
  const userId = user?.user_id || 1
  const [showCreateModal, setShowCreateModal] = useState(false)
  const queryClient = useQueryClient()

  const { data: remindersResponse, isLoading } = useQuery({
    queryKey: ['reminders', userId, todoId],
    queryFn: () => reminderApi.getReminders({
      user_id: userId,
      todo_id: todoId,
    }),
  })
  const reminders = remindersResponse?.reminders || []

  const deleteMutation = useMutation({
    mutationFn: (reminderId: number) => reminderApi.deleteReminder(reminderId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['reminders', userId, todoId] })
    },
  })

  return (
    <Card>
      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <Bell className="h-5 w-5 text-primary-600" />
            <h3 className="text-lg font-semibold text-gray-900">Reminders</h3>
          </div>
          <Button size="sm" onClick={() => setShowCreateModal(true)}>
            <Plus className="h-4 w-4 mr-2" />
            Add Reminder
          </Button>
        </div>

        {isLoading ? (
          <div className="text-center py-4 text-gray-500">Loading reminders...</div>
        ) : reminders.length === 0 ? (
          <div className="text-center py-4 text-gray-500">
            <p>No reminders set</p>
            <Button size="sm" variant="secondary" className="mt-2" onClick={() => setShowCreateModal(true)}>
              Create your first reminder
            </Button>
          </div>
        ) : (
          <div className="space-y-2">
            {reminders.map((reminder: Reminder) => (
              <div
                key={reminder.reminder_id}
                className="flex items-center justify-between p-3 bg-gray-50 rounded-lg"
              >
                <div className="flex-1">
                  <div className="flex items-center gap-2">
                    <Clock className="h-4 w-4 text-gray-400" />
                    <span className="text-sm font-medium text-gray-900">
                      {new Date(reminder.reminder_time).toLocaleString()}
                    </span>
                    <span className={`text-xs px-2 py-1 rounded-full ${
                      reminder.status === 'Sent' ? 'bg-green-100 text-green-700' :
                      reminder.status === 'Pending' ? 'bg-yellow-100 text-yellow-700' :
                      reminder.status === 'Failed' ? 'bg-red-100 text-red-700' :
                      'bg-gray-100 text-gray-700'
                    }`}>
                      {reminder.status}
                    </span>
                  </div>
                  {reminder.message && (
                    <p className="text-sm text-gray-600 mt-1">{reminder.message}</p>
                  )}
                  <div className="flex items-center gap-2 mt-2">
                    {reminder.notification_channels.map((channel, i) => (
                      <span key={i} className="text-xs px-2 py-1 bg-blue-100 text-blue-700 rounded">
                        {channel}
                      </span>
                    ))}
                  </div>
                </div>
                <div className="flex items-center gap-2">
                  <button
                    onClick={() => deleteMutation.mutate(reminder.reminder_id)}
                    className="p-1 text-red-600 hover:text-red-700"
                  >
                    <Trash2 className="h-4 w-4" />
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}

        {showCreateModal && (
          <CreateReminderModal
            todoId={todoId}
            onClose={() => setShowCreateModal(false)}
            onSuccess={() => {
              setShowCreateModal(false)
              queryClient.invalidateQueries({ queryKey: ['reminders', userId, todoId] })
            }}
          />
        )}
      </div>
    </Card>
  )
}

interface CreateReminderModalProps {
  todoId?: number
  onClose: () => void
  onSuccess: () => void
}

function CreateReminderModal({ todoId, onClose, onSuccess }: CreateReminderModalProps) {
  const { user } = useAuthStore()
  const userId = user?.user_id || 1
  const [reminderTime, setReminderTime] = useState('')
  const [message, setMessage] = useState('')
  const [channels, setChannels] = useState<string[]>(['Email'])

  const createMutation = useMutation({
    mutationFn: (data: any) => reminderApi.createReminder(data),
    onSuccess: () => {
      onSuccess()
    },
  })

  const toggleChannel = (channel: string) => {
    if (channels.includes(channel)) {
      setChannels(channels.filter(c => c !== channel))
    } else {
      setChannels([...channels, channel])
    }
  }

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (!reminderTime) return

    const reminderTimeMs = new Date(reminderTime).getTime()

    createMutation.mutate({
      user_id: userId,
      todo_id: todoId || null,
      reminder_time: reminderTimeMs,
      message: message || null,
      notification_channels: channels,
      reminder_type: 'Manual',
    })
  }

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-lg w-full max-w-md">
        <div className="flex items-center justify-between p-4 border-b border-gray-200">
          <h2 className="text-lg font-semibold text-gray-900">Create Reminder</h2>
          <button onClick={onClose} className="p-1 text-gray-400 hover:text-gray-600">
            <span className="text-xl">×</span>
          </button>
        </div>

        <form onSubmit={handleSubmit} className="p-4 space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Reminder Time *
            </label>
            <input
              type="datetime-local"
              value={reminderTime}
              onChange={(e) => setReminderTime(e.target.value)}
              className="input"
              required
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Message
            </label>
            <textarea
              value={message}
              onChange={(e) => setMessage(e.target.value)}
              className="input min-h-[80px] resize-none"
              placeholder="Optional reminder message"
              rows={3}
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Notification Channels *
            </label>
            <div className="space-y-2">
              {['Email', 'SMS', 'Telegram', 'Bale', 'Eitaa'].map((channel) => (
                <label key={channel} className="flex items-center gap-2">
                  <input
                    type="checkbox"
                    checked={channels.includes(channel)}
                    onChange={() => toggleChannel(channel)}
                    className="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded"
                  />
                  <span className="text-sm text-gray-700">{channel}</span>
                </label>
              ))}
            </div>
          </div>

          <div className="flex gap-3 pt-4">
            <Button type="button" variant="secondary" className="flex-1" onClick={onClose}>
              Cancel
            </Button>
            <Button type="submit" className="flex-1" disabled={createMutation.isPending || channels.length === 0}>
              {createMutation.isPending ? 'Creating...' : 'Create Reminder'}
            </Button>
          </div>
        </form>
      </div>
    </div>
  )
}

