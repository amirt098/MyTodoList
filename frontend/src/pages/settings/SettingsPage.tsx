import Card from '../../components/ui/Card'
import Button from '../../components/ui/Button'
import { useAuthStore } from '../../store/authStore'
import { Bell, User, Shield, Moon } from 'lucide-react'

export default function SettingsPage() {
  const { user, logout } = useAuthStore()

  return (
    <div className="space-y-6 pb-20 lg:pb-6">
      <div>
        <h1 className="text-2xl sm:text-3xl font-bold text-gray-900">Settings</h1>
        <p className="text-gray-600 mt-1">Manage your account and preferences</p>
      </div>

      {/* Profile Settings */}
      <Card>
        <div className="flex items-center gap-3 mb-6">
          <div className="h-12 w-12 rounded-full bg-primary-600 flex items-center justify-center text-white text-lg font-medium">
            {user?.email?.charAt(0).toUpperCase() || 'U'}
          </div>
          <div>
            <h2 className="font-semibold text-gray-900">{user?.email}</h2>
            <p className="text-sm text-gray-600">Member since {user?.created_at ? new Date(user.created_at).getFullYear() : '2024'}</p>
          </div>
        </div>

        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <User className="h-5 w-5 text-gray-400" />
              <div>
                <h3 className="font-medium text-gray-900">Profile</h3>
                <p className="text-sm text-gray-600">Update your profile information</p>
              </div>
            </div>
            <Button variant="ghost" size="sm">Edit</Button>
          </div>

          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <Bell className="h-5 w-5 text-gray-400" />
              <div>
                <h3 className="font-medium text-gray-900">Notifications</h3>
                <p className="text-sm text-gray-600">Manage notification preferences</p>
              </div>
            </div>
            <Button variant="ghost" size="sm">Configure</Button>
          </div>

          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <Shield className="h-5 w-5 text-gray-400" />
              <div>
                <h3 className="font-medium text-gray-900">Security</h3>
                <p className="text-sm text-gray-600">Password and security settings</p>
              </div>
            </div>
            <Button variant="ghost" size="sm">Change</Button>
          </div>
        </div>
      </Card>

      {/* Danger Zone */}
      <Card>
        <h2 className="text-lg font-semibold text-red-600 mb-4">Danger Zone</h2>
        <Button variant="danger" onClick={logout}>
          Logout
        </Button>
      </Card>
    </div>
  )
}

