import { useState } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { filterApi } from '../../services/api'
import { useAuthStore } from '../../store/authStore'
import Card from '../ui/Card'
import Button from '../ui/Button'
import { Filter, X, Save, Trash2 } from 'lucide-react'

interface AdvancedFiltersProps {
  filters: any
  onFiltersChange: (filters: any) => void
}

export default function AdvancedFilters({ filters, onFiltersChange }: AdvancedFiltersProps) {
  const { user } = useAuthStore()
  const userId = user?.user_id || 1
  const queryClient = useQueryClient()
  const [showFilters, setShowFilters] = useState(false)
  const [filterName, setFilterName] = useState('')

  const { data: savedFiltersResponse } = useQuery({
    queryKey: ['saved-filters', userId],
    queryFn: () => filterApi.getSavedFilters({ user_id: userId }),
  })
  const savedFilters = savedFiltersResponse?.filters || []

  const saveFilterMutation = useMutation({
    mutationFn: (data: any) => filterApi.saveFilter(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['saved-filters', userId] })
      setFilterName('')
    },
  })

  const deleteFilterMutation = useMutation({
    mutationFn: (filterId: number) => filterApi.deleteSavedFilter(filterId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['saved-filters', userId] })
    },
  })

  const handleSaveFilter = () => {
    if (!filterName.trim()) return
    saveFilterMutation.mutate({
      user_id: userId,
      name: filterName,
      filter_data: filters,
    })
  }

  const handleLoadFilter = (savedFilter: any) => {
    if (savedFilter.filter_data) {
      onFiltersChange(savedFilter.filter_data)
    }
  }

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <Button
          variant="secondary"
          size="sm"
          onClick={() => setShowFilters(!showFilters)}
        >
          <Filter className="h-4 w-4 mr-2" />
          {showFilters ? 'Hide' : 'Show'} Advanced Filters
        </Button>
        {savedFilters.length > 0 && (
          <div className="flex items-center gap-2">
            <span className="text-sm text-gray-600">Saved Filters:</span>
            <select
              className="input text-sm"
              onChange={(e) => {
                const filter = savedFilters.find((f: any) => f.filter_id === parseInt(e.target.value))
                if (filter) handleLoadFilter(filter)
              }}
              defaultValue=""
            >
              <option value="">Select a saved filter...</option>
              {savedFilters.map((filter: any) => (
                <option key={filter.filter_id} value={filter.filter_id}>
                  {filter.name}
                </option>
              ))}
            </select>
          </div>
        )}
      </div>

      {showFilters && (
        <Card>
          <div className="space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Status
                </label>
                <select
                  value={filters.status || ''}
                  onChange={(e) => onFiltersChange({ ...filters, status: e.target.value || undefined })}
                  className="input"
                >
                  <option value="">All</option>
                  <option value="ToDo">ToDo</option>
                  <option value="In Progress">In Progress</option>
                  <option value="Waiting">Waiting</option>
                  <option value="Blocked">Blocked</option>
                  <option value="Done">Done</option>
                  <option value="Cancelled">Cancelled</option>
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Priority
                </label>
                <select
                  value={filters.priority || ''}
                  onChange={(e) => onFiltersChange({ ...filters, priority: e.target.value || undefined })}
                  className="input"
                >
                  <option value="">All</option>
                  <option value="Low">Low</option>
                  <option value="Medium">Medium</option>
                  <option value="High">High</option>
                  <option value="Critical">Critical</option>
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Category
                </label>
                <input
                  type="text"
                  value={filters.category || ''}
                  onChange={(e) => onFiltersChange({ ...filters, category: e.target.value || undefined })}
                  className="input"
                  placeholder="Filter by category"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Label
                </label>
                <input
                  type="text"
                  value={filters.label || ''}
                  onChange={(e) => onFiltersChange({ ...filters, label: e.target.value || undefined })}
                  className="input"
                  placeholder="Filter by label"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Deadline After (From)
                </label>
                <input
                  type="date"
                  value={filters.deadline_after__gte ? new Date(filters.deadline_after__gte).toISOString().split('T')[0] : ''}
                  onChange={(e) => onFiltersChange({
                    ...filters,
                    deadline_after__gte: e.target.value ? new Date(e.target.value).getTime() : undefined
                  })}
                  className="input"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Deadline Before (To)
                </label>
                <input
                  type="date"
                  value={filters.deadline_after__lte ? new Date(filters.deadline_after__lte).toISOString().split('T')[0] : ''}
                  onChange={(e) => onFiltersChange({
                    ...filters,
                    deadline_after__lte: e.target.value ? new Date(e.target.value).getTime() : undefined
                  })}
                  className="input"
                />
              </div>
            </div>

            <div className="flex items-center gap-2 pt-2 border-t">
              <input
                type="text"
                value={filterName}
                onChange={(e) => setFilterName(e.target.value)}
                className="input flex-1"
                placeholder="Save filter as..."
              />
              <Button
                size="sm"
                onClick={handleSaveFilter}
                disabled={!filterName.trim() || saveFilterMutation.isPending}
              >
                <Save className="h-4 w-4 mr-2" />
                Save
              </Button>
              <Button
                variant="secondary"
                size="sm"
                onClick={() => onFiltersChange({})}
              >
                <X className="h-4 w-4 mr-2" />
                Clear
              </Button>
            </div>

            {savedFilters.length > 0 && (
              <div className="pt-2 border-t">
                <h4 className="text-sm font-medium text-gray-700 mb-2">Saved Filters</h4>
                <div className="flex flex-wrap gap-2">
                  {savedFilters.map((filter: any) => (
                    <div
                      key={filter.filter_id}
                      className="flex items-center gap-2 px-3 py-1 bg-gray-100 rounded-full"
                    >
                      <button
                        onClick={() => handleLoadFilter(filter)}
                        className="text-sm text-gray-700 hover:text-primary-600"
                      >
                        {filter.name}
                      </button>
                      <button
                        onClick={() => deleteFilterMutation.mutate(filter.filter_id)}
                        className="text-red-600 hover:text-red-700"
                      >
                        <Trash2 className="h-3 w-3" />
                      </button>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        </Card>
      )}
    </div>
  )
}

