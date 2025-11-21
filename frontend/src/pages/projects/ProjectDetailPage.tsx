import { useState } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { useQuery } from '@tanstack/react-query'
import { projectApi } from '../../services/api'
import { useAuthStore } from '../../store/authStore'
import Card from '../../components/ui/Card'
import Button from '../../components/ui/Button'
import { ArrowLeft, Settings, Users, LayoutGrid, ListTodo } from 'lucide-react'
import ProjectKanbanBoard from '../../components/projects/ProjectKanbanBoard'
import ProjectTodosList from '../../components/projects/ProjectTodosList'
import ProjectMembers from '../../components/projects/ProjectMembers'

type TabType = 'overview' | 'kanban' | 'todos' | 'members'

export default function ProjectDetailPage() {
  const { id } = useParams<{ id: string }>()
  const navigate = useNavigate()
  const { user } = useAuthStore()
  const userId = user?.user_id || 1
  const projectId = parseInt(id || '0')
  const [activeTab, setActiveTab] = useState<TabType>('overview')

  const { data: project, isLoading } = useQuery({
    queryKey: ['project', projectId],
    queryFn: () => projectApi.getProject(projectId, {}), // user_id comes from auth token
    enabled: !!projectId,
  })

  if (isLoading) {
    return <div className="text-center py-12 text-gray-500">Loading...</div>
  }

  if (!project) {
    return (
      <div className="text-center py-12">
        <p className="text-gray-500 mb-4">Project not found</p>
        <Button onClick={() => navigate('/projects')}>Back to Projects</Button>
      </div>
    )
  }

  const projectData = project as any

  return (
    <div className="space-y-6 pb-20 lg:pb-6">
      <div className="flex items-center gap-4">
        <Button variant="ghost" size="sm" onClick={() => navigate('/projects')}>
          <ArrowLeft className="h-4 w-4 mr-2" />
          Back
        </Button>
        <div className="flex-1">
          <h1 className="text-2xl sm:text-3xl font-bold text-gray-900">{projectData.name}</h1>
        </div>
        <Button variant="ghost" size="sm">
          <Settings className="h-4 w-4" />
        </Button>
      </div>

      {/* Tabs */}
      <div className="border-b border-gray-200">
        <nav className="flex gap-4">
          <button
            onClick={() => setActiveTab('overview')}
            className={`px-4 py-2 text-sm font-medium border-b-2 transition-colors ${
              activeTab === 'overview'
                ? 'border-primary-600 text-primary-600'
                : 'border-transparent text-gray-500 hover:text-gray-700'
            }`}
          >
            Overview
          </button>
          <button
            onClick={() => setActiveTab('kanban')}
            className={`px-4 py-2 text-sm font-medium border-b-2 transition-colors flex items-center gap-2 ${
              activeTab === 'kanban'
                ? 'border-primary-600 text-primary-600'
                : 'border-transparent text-gray-500 hover:text-gray-700'
            }`}
          >
            <LayoutGrid className="h-4 w-4" />
            Kanban Board
          </button>
          <button
            onClick={() => setActiveTab('todos')}
            className={`px-4 py-2 text-sm font-medium border-b-2 transition-colors flex items-center gap-2 ${
              activeTab === 'todos'
                ? 'border-primary-600 text-primary-600'
                : 'border-transparent text-gray-500 hover:text-gray-700'
            }`}
          >
            <ListTodo className="h-4 w-4" />
            Todos
          </button>
          <button
            onClick={() => setActiveTab('members')}
            className={`px-4 py-2 text-sm font-medium border-b-2 transition-colors flex items-center gap-2 ${
              activeTab === 'members'
                ? 'border-primary-600 text-primary-600'
                : 'border-transparent text-gray-500 hover:text-gray-700'
            }`}
          >
            <Users className="h-4 w-4" />
            Members
          </button>
        </nav>
      </div>

      {/* Tab Content */}
      {activeTab === 'overview' && (
        <Card>
          <div className="space-y-4">
            {projectData.description && (
              <div>
                <h3 className="text-sm font-medium text-gray-700 mb-2">Description</h3>
                <p className="text-gray-900">{projectData.description}</p>
              </div>
            )}

            <div className="flex items-center gap-4">
              <div className="flex items-center gap-2 text-sm text-gray-600">
                <Users className="h-4 w-4" />
                <span>Members</span>
              </div>
              {projectData.is_private && (
                <span className="text-xs px-2 py-1 bg-gray-100 text-gray-700 rounded">
                  Private Project
                </span>
              )}
            </div>
          </div>
        </Card>
      )}

      {activeTab === 'kanban' && (
        <ProjectKanbanBoard projectId={projectId} userId={userId} />
      )}

      {activeTab === 'todos' && (
        <ProjectTodosList projectId={projectId} userId={userId} />
      )}

      {activeTab === 'members' && (
        <ProjectMembers projectId={projectId} />
      )}
    </div>
  )
}

