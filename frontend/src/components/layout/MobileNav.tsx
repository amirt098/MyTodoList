import { NavLink } from 'react-router-dom'
import { 
  LayoutDashboard, 
  CheckSquare, 
  Columns, 
  FolderKanban,
  Settings
} from 'lucide-react'
import { cn } from '../../utils/cn'

const navItems = [
  { path: '/', icon: LayoutDashboard, label: 'Home' },
  { path: '/todos', icon: CheckSquare, label: 'Todos' },
  { path: '/kanban', icon: Columns, label: 'Board' },
  { path: '/projects', icon: FolderKanban, label: 'Projects' },
  { path: '/settings', icon: Settings, label: 'Settings' },
]

export default function MobileNav() {
  return (
    <nav className="bg-white border-t border-gray-200 safe-area-bottom">
      <div className="flex items-center justify-around h-16">
        {navItems.map((item) => {
          const Icon = item.icon
          return (
            <NavLink
              key={item.path}
              to={item.path}
              className={({ isActive }) =>
                cn(
                  'flex flex-col items-center justify-center gap-1 flex-1 h-full transition-colors',
                  isActive
                    ? 'text-primary-600'
                    : 'text-gray-500'
                )
              }
            >
              <Icon className="h-5 w-5" />
              <span className="text-xs font-medium">{item.label}</span>
            </NavLink>
          )
        })}
      </div>
    </nav>
  )
}

