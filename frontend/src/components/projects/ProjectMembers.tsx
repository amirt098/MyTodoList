import { useState } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { projectMemberApi } from '../../services/api'
import { useAuthStore } from '../../store/authStore'
import Card from '../ui/Card'
import Button from '../ui/Button'
import { Users, Plus, Trash2, Shield, User, Crown } from 'lucide-react'

interface ProjectMembersProps {
  projectId: number
}

export default function ProjectMembers({ projectId }: ProjectMembersProps) {
  const { user } = useAuthStore()
  const userId = user?.user_id || 1
  const [showAddModal, setShowAddModal] = useState(false)
  const queryClient = useQueryClient()

  // Note: We need to get project members from the project data
  // For now, we'll create a simple UI that can be enhanced when the API is available
  const addMemberMutation = useMutation({
    mutationFn: (data: any) => projectMemberApi.addMember(projectId, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['project', projectId] })
      setShowAddModal(false)
    },
  })

  const removeMemberMutation = useMutation({
    mutationFn: (data: any) => projectMemberApi.removeMember(projectId, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['project', projectId] })
    },
  })

  const updateRoleMutation = useMutation({
    mutationFn: (data: any) => projectMemberApi.updateMemberRole(projectId, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['project', projectId] })
    },
  })

  const handleAddMember = (email: string, role: string) => {
    addMemberMutation.mutate({
      user_email: email,
      role,
      // user_id comes from auth token
    })
  }

  const handleRemoveMember = (memberUserId: number) => {
    if (!confirm('Are you sure you want to remove this member?')) return
    removeMemberMutation.mutate({
      member_user_id: memberUserId,
      // user_id comes from auth token
    })
  }

  const handleUpdateRole = (memberUserId: number, newRole: string) => {
    updateRoleMutation.mutate({
      member_user_id: memberUserId,
      new_role: newRole,
      // user_id comes from auth token
    })
  }

  return (
    <Card>
      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <Users className="h-5 w-5 text-primary-600" />
            <h3 className="text-lg font-semibold text-gray-900">Project Members</h3>
          </div>
          <Button size="sm" onClick={() => setShowAddModal(true)}>
            <Plus className="h-4 w-4 mr-2" />
            Add Member
          </Button>
        </div>

        <p className="text-sm text-gray-600">
          Member management will be displayed here. The project data should include members list.
        </p>

        {showAddModal && (
          <AddMemberModal
            onClose={() => setShowAddModal(false)}
            onAdd={handleAddMember}
            isPending={addMemberMutation.isPending}
          />
        )}
      </div>
    </Card>
  )
}

interface AddMemberModalProps {
  onClose: () => void
  onAdd: (email: string, role: string) => void
  isPending: boolean
}

function AddMemberModal({ onClose, onAdd, isPending }: AddMemberModalProps) {
  const [email, setEmail] = useState('')
  const [role, setRole] = useState('Member')

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (!email.trim()) return
    onAdd(email.trim(), role)
    setEmail('')
    setRole('Member')
  }

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-lg w-full max-w-md">
        <div className="flex items-center justify-between p-4 border-b border-gray-200">
          <h2 className="text-lg font-semibold text-gray-900">Add Project Member</h2>
          <button onClick={onClose} className="p-1 text-gray-400 hover:text-gray-600">
            <span className="text-xl">×</span>
          </button>
        </div>

        <form onSubmit={handleSubmit} className="p-4 space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Member Email *
            </label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="input"
              placeholder="user@example.com"
              required
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Role *
            </label>
            <select
              value={role}
              onChange={(e) => setRole(e.target.value)}
              className="input"
            >
              <option value="Member">Member</option>
              <option value="Admin">Admin</option>
            </select>
            <p className="text-xs text-gray-500 mt-1">
              Note: Only the project owner can assign Admin role
            </p>
          </div>

          <div className="flex gap-3 pt-4">
            <Button type="button" variant="secondary" className="flex-1" onClick={onClose}>
              Cancel
            </Button>
            <Button type="submit" className="flex-1" disabled={isPending || !email.trim()}>
              {isPending ? 'Adding...' : 'Add Member'}
            </Button>
          </div>
        </form>
      </div>
    </div>
  )
}

