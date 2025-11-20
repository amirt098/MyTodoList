import { Link } from 'react-router-dom'
import { Todo } from '../../types'
import { formatRelativeTime } from '../../utils/formatDate'
import { cn } from '../../utils/cn'

interface TodoItemProps {
  todo: Todo
}

export default function TodoItem({ todo }: TodoItemProps) {
  return (
    <Link to={`/todos/${todo.todo_id}`}>
      <div className="card hover:shadow-md transition-shadow">
        <div className="flex items-start justify-between gap-4">
          <div className="flex-1 min-w-0">
            <h3 className="font-medium text-gray-900 truncate">{todo.title}</h3>
            {todo.description && (
              <p className="text-sm text-gray-600 mt-1 line-clamp-2">{todo.description}</p>
            )}
            <div className="flex items-center gap-2 mt-3 flex-wrap">
              <span className={cn(
                'text-xs px-2 py-1 rounded-full font-medium',
                todo.priority === 'Critical' ? 'bg-red-100 text-red-700' :
                todo.priority === 'High' ? 'bg-orange-100 text-orange-700' :
                todo.priority === 'Medium' ? 'bg-yellow-100 text-yellow-700' :
                'bg-gray-100 text-gray-700'
              )}>
                {todo.priority}
              </span>
              <span className={cn(
                'text-xs px-2 py-1 rounded-full font-medium',
                todo.status === 'Done' ? 'bg-green-100 text-green-700' :
                todo.status === 'In Progress' ? 'bg-blue-100 text-blue-700' :
                'bg-gray-100 text-gray-700'
              )}>
                {todo.status}
              </span>
              {todo.progress > 0 && (
                <span className="text-xs text-gray-500">
                  {todo.progress}% done
                </span>
              )}
            </div>
          </div>
          {todo.deadline_timestamp_ms && (
            <div className="text-xs text-gray-500 whitespace-nowrap">
              {formatRelativeTime(todo.deadline_timestamp_ms)}
            </div>
          )}
        </div>
      </div>
    </Link>
  )
}

