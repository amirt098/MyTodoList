import { useAuthStore } from '../../store/authStore'
import { Bell, Search } from 'lucide-react'
import { useState } from 'react'

export default function Header() {
  const { user } = useAuthStore()
  const [showSearch, setShowSearch] = useState(false)

  return (
    <header className="sticky top-0 z-40 bg-white border-b border-gray-200">
      <div className="container-mobile">
        <div className="flex h-16 items-center justify-between">
          {/* Logo */}
          <div className="flex items-center">
            <h1 className="text-xl font-bold text-primary-600">MyTodo</h1>
          </div>
          
          {/* Search - Desktop */}
          <div className="hidden md:flex flex-1 max-w-md mx-8">
            <div className="relative w-full">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 h-5 w-5" />
              <input
                type="text"
                placeholder="Search todos, projects..."
                className="input pl-10 w-full"
              />
            </div>
          </div>
          
          {/* Actions */}
          <div className="flex items-center gap-2">
            {/* Search - Mobile */}
            <button
              onClick={() => setShowSearch(!showSearch)}
              className="md:hidden p-2 text-gray-600 hover:text-gray-900"
            >
              <Search className="h-5 w-5" />
            </button>
            
            {/* Notifications */}
            <button className="relative p-2 text-gray-600 hover:text-gray-900">
              <Bell className="h-5 w-5" />
              <span className="absolute top-1 right-1 h-2 w-2 bg-red-500 rounded-full"></span>
            </button>
            
            {/* User Avatar */}
            <div className="h-8 w-8 rounded-full bg-primary-600 flex items-center justify-center text-white text-sm font-medium">
              {user?.email?.charAt(0).toUpperCase() || 'U'}
            </div>
          </div>
        </div>
        
        {/* Mobile Search */}
        {showSearch && (
          <div className="md:hidden pb-4">
            <div className="relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 h-5 w-5" />
              <input
                type="text"
                placeholder="Search todos, projects..."
                className="input pl-10 w-full"
                autoFocus
              />
            </div>
          </div>
        )}
      </div>
    </header>
  )
}

