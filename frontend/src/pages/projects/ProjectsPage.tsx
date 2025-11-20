import { useQuery } from '@tanstack/react-query'
import { projectApi } from '../../services/api'
import Card from '../../components/ui/Card'
import Button from '../../components/ui/Button'
import { Plus, FolderKanban, Users } from 'lucide-react'
import { Link } from 'react-router-dom'

export default function ProjectsPage() {
  const { data: projects, isLoading } = useQuery({
    queryKey: ['projects'],
    queryFn: () => projectApi.getProjects({ user_id: 1 }),
  })

  return (
    <div className="space-y-6 pb-20 lg:pb-6">
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h1 className="text-2xl sm:text-3xl font-bold text-gray-900">Projects</h1>
          <p className="text-gray-600 mt-1">Manage your projects and collaborate</p>
        </div>
        <Button>
          <Plus className="h-4 w-4 mr-2" />
          New Project
        </Button>
      </div>

      {isLoading ? (
        <div className="text-center py-12 text-gray-500">Loading projects...</div>
      ) : projects?.length === 0 ? (
        <Card>
          <div className="text-center py-12">
            <FolderKanban className="h-12 w-12 text-gray-400 mx-auto mb-4" />
            <p className="text-gray-500 mb-4">No projects yet</p>
            <Button>Create your first project</Button>
          </div>
        </Card>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {projects?.map((project: any) => (
            <Link key={project.project_id} to={`/projects/${project.project_id}`}>
              <Card className="h-full hover:shadow-md transition-shadow">
                <div className="flex items-start justify-between mb-3">
                  <FolderKanban className="h-8 w-8 text-primary-600" />
                  {project.is_private && (
                    <span className="text-xs px-2 py-1 bg-gray-100 text-gray-700 rounded">
                      Private
                    </span>
                  )}
                </div>
                <h3 className="font-semibold text-gray-900 mb-2">{project.name}</h3>
                {project.description && (
                  <p className="text-sm text-gray-600 line-clamp-2 mb-4">
                    {project.description}
                  </p>
                )}
                <div className="flex items-center gap-2 text-sm text-gray-500">
                  <Users className="h-4 w-4" />
                  <span>Members</span>
                </div>
              </Card>
            </Link>
          ))}
        </div>
      )}
    </div>
  )
}

