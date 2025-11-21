import axios, { AxiosInstance, AxiosError } from 'axios'

class ApiClient {
  private client: AxiosInstance

  constructor() {
    this.client = axios.create({
      baseURL: '/api',
      headers: {
        'Content-Type': 'application/json',
      },
    })

    // Request interceptor
    this.client.interceptors.request.use(
      (config) => {
        // Add auth token if available
        const token = localStorage.getItem('auth_token')
        if (token) {
          config.headers.Authorization = `Bearer ${token}`
        }
        return config
      },
      (error) => {
        return Promise.reject(error)
      }
    )

    // Response interceptor
    this.client.interceptors.response.use(
      (response) => response,
      (error: AxiosError) => {
        if (error.response?.status === 401) {
          // Unauthorized - clear auth and redirect to login
          localStorage.removeItem('auth_token')
          localStorage.removeItem('user')
          window.location.href = '/login'
        }
        return Promise.reject(error)
      }
    )
  }

  async get<T>(url: string, params?: Record<string, any>): Promise<T> {
    const response = await this.client.get<T>(url, { params })
    return response.data
  }

  async post<T>(url: string, data?: any): Promise<T> {
    const response = await this.client.post<T>(url, data)
    return response.data
  }

  async put<T>(url: string, data?: any): Promise<T> {
    const response = await this.client.put<T>(url, data)
    return response.data
  }

  async delete<T>(url: string): Promise<T> {
    const response = await this.client.delete<T>(url)
    return response.data
  }
}

export const apiClient = new ApiClient()

// Auth API
export const authApi = {
  register: (data: { email: string; password: string; username: string }) =>
    apiClient.post('/auth/register/', data),
  
  login: (data: { email: string; password: string }) =>
    apiClient.post('/auth/login/', data),
  
  updateProfile: (data: any) =>
    apiClient.post('/auth/profile/', data),
}

// Todo API
export const todoApi = {
  getTodos: (params?: any) =>
    apiClient.get('/todos/', params),
  
  getTodo: (id: number, params?: any) =>
    apiClient.get(`/todos/${id}/`, params),
  
  createTodo: (data: any) =>
    apiClient.post('/todos/create/', data),
  
  updateTodo: (id: number, data: any) =>
    apiClient.post(`/todos/${id}/update/`, data),
  
  deleteTodo: (id: number) =>
    apiClient.delete(`/todos/${id}/delete/`),
  
  getAllMyTodos: (params?: any) =>
    apiClient.get('/todos/all-my-todos/', params),
}

// Subtask API
export const subtaskApi = {
  getSubtasks: (todoId: number, params?: any) =>
    apiClient.get(`/todos/${todoId}/subtasks/`, params),
  
  addSubtask: (todoId: number, data: any) =>
    apiClient.post(`/todos/${todoId}/subtasks/add/`, data),
  
  updateSubtask: (subtaskId: number, data: any) =>
    apiClient.put(`/subtasks/${subtaskId}/update/`, data),
  
  deleteSubtask: (subtaskId: number) =>
    apiClient.delete(`/subtasks/${subtaskId}/delete/`),
  
  markSubtaskDone: (subtaskId: number, data: any) =>
    apiClient.post(`/subtasks/${subtaskId}/mark-done/`, data),
}

// Project API
export const projectApi = {
  getProjects: (params?: any) =>
    apiClient.get('/projects/', params),
  
  getProject: (id: number, params?: any) =>
    apiClient.get(`/projects/${id}/`, params),
  
  createProject: (data: any) =>
    apiClient.post('/projects/create/', data),
  
  updateProject: (id: number, data: any) =>
    apiClient.post(`/projects/${id}/update/`, data),
  
  deleteProject: (id: number) =>
    apiClient.delete(`/projects/${id}/delete/`),
}

// Kanban API
export const kanbanApi = {
  getBoard: (params?: any) =>
    apiClient.get('/kanban/board/', params),
  
  moveTodo: (data: any) =>
    apiClient.post('/kanban/move-todo/', data),
  
  createColumn: (data: any) =>
    apiClient.post('/kanban/columns/create/', data),
  
  deleteColumn: (id: number) =>
    apiClient.delete(`/kanban/columns/${id}/delete/`),
  
  reorderColumns: (data: any) =>
    apiClient.post('/kanban/columns/reorder/', data),
}

// AI API
export const aiApi = {
  analyzeText: (data: any) =>
    apiClient.post('/ai/analyze-text/', data),
  
  createSmartTodo: (data: any) =>
    apiClient.post('/ai/create-smart-todo/', data),
  
  autoCategorize: (data: any) =>
    apiClient.post('/ai/auto-categorize/', data),
  
  suggestSubtasks: (data: any) =>
    apiClient.post('/ai/suggest-subtasks/', data),
  
  suggestNextAction: (data: any) =>
    apiClient.post('/ai/suggest-next-action/', data),
  
  conversationalQuery: (data: any) =>
    apiClient.post('/ai/query/', data),
}

// Reminder API
export const reminderApi = {
  getReminders: (params?: any) =>
    apiClient.get('/reminders/', params),
  
  createReminder: (data: any) =>
    apiClient.post('/reminders/create/', data),
  
  updateReminder: (id: number, data: any) =>
    apiClient.put(`/reminders/${id}/update/`, data),
  
  deleteReminder: (id: number) =>
    apiClient.delete(`/reminders/${id}/delete/`),
}

// Filter API
export const filterApi = {
  saveFilter: (data: any) =>
    apiClient.post('/filters/save/', data),
  
  getSavedFilters: (params?: any) =>
    apiClient.get('/filters/', params),
  
  deleteSavedFilter: (id: number) =>
    apiClient.delete(`/filters/${id}/delete/`),
}

// Bulk Operations API
export const bulkApi = {
  bulkUpdate: (data: any) =>
    apiClient.post('/todos/bulk-update/', data),
  
  bulkDelete: (data: any) =>
    apiClient.post('/todos/bulk-delete/', data),
}

// Export API
export const exportApi = {
  exportTodos: (params?: any) =>
    apiClient.get('/todos/export/', params),
}

// Dependency API
export const dependencyApi = {
  setDependency: (data: any) =>
    apiClient.post('/todos/dependencies/set/', data),
  
  removeDependency: (todoId: number, data?: any) =>
    apiClient.post(`/todos/${todoId}/dependencies/remove/`, data),
  
  validateDependency: (todoId: number, params?: any) =>
    apiClient.get(`/todos/${todoId}/dependencies/validate/`, params),
  
  getDependencyChain: (todoId: number, params?: any) =>
    apiClient.get(`/todos/${todoId}/dependencies/chain/`, params),
}

// Project Member API
export const projectMemberApi = {
  addMember: (projectId: number, data: any) =>
    apiClient.post(`/projects/${projectId}/members/add/`, data),
  
  removeMember: (projectId: number, data: any) =>
    apiClient.post(`/projects/${projectId}/members/remove/`, data),
  
  updateMemberRole: (projectId: number, data: any) =>
    apiClient.post(`/projects/${projectId}/members/update-role/`, data),
}

