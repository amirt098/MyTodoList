// User types
export interface User {
  user_id: number
  email: string
  username?: string
  first_name?: string
  last_name?: string
  phone?: string
  is_active: boolean
  is_verified: boolean
  created_at: number
}

// Todo types
export interface Todo {
  todo_id: number
  title: string
  description: string
  deadline_timestamp_ms?: number
  priority: 'Low' | 'Medium' | 'High' | 'Critical'
  status: 'ToDo' | 'In Progress' | 'Waiting' | 'Blocked' | 'Done' | 'Cancelled'
  category: string
  labels: string[]
  user_id: number
  project_id?: number
  previous_todo_id?: number
  next_todo_id?: number
  order: number
  created_at: number
  updated_at: number
  completed_at_timestamp_ms?: number
  auto_repeat: string
  progress: number
}

// Subtask types
export interface Subtask {
  subtask_id: number
  title: string
  status: 'ToDo' | 'Done'
  todo_id: number
  order: number
  created_at: number
  updated_at: number
  completed_at_timestamp_ms?: number
}

// Project types
export interface Project {
  project_id: number
  name: string
  description: string
  is_private: boolean
  owner_id: number
  created_at: number
  updated_at: number
}

export interface ProjectMember {
  member_id: number
  project_id: number
  user_id: number
  role: 'Owner' | 'Admin' | 'Member'
  joined_at: number
}

// Kanban types
export interface KanbanColumn {
  column_id: number
  name: string
  status_value: string
  color: string
  project_id?: number
  user_id?: number
  order: number
  is_default: boolean
  is_active: boolean
}

export interface KanbanCard {
  todo_id: number
  title: string
  description: string
  priority: string
  status: string
  labels: string[]
  deadline_timestamp_ms?: number
  project_id?: number
  order: number
  progress: number
}

// Reminder types
export interface Reminder {
  reminder_id: number
  title: string
  message: string
  reminder_time: number
  sent_at?: number
  notification_channels: string[]
  todo_id?: number
  user_id: number
  reminder_type: string
  status: 'Pending' | 'Sent' | 'Failed' | 'Cancelled'
  created_at: number
  updated_at: number
}

// AI types
export interface TodoSuggestion {
  title: string
  description?: string
  priority: string
  category?: string
  labels: string[]
  suggested_deadline?: number
  suggested_project_id?: number
  suggested_subtasks: string[]
  confidence: number
}

// API Response types
export interface ApiResponse<T> {
  data?: T
  error?: {
    message: string
    code: string
  }
}

export interface ListResponse<T> {
  items: T[]
  total: number
}

