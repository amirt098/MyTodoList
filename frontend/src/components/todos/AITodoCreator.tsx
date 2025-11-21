import { useState } from 'react'
import { useMutation } from '@tanstack/react-query'
import { aiApi, todoApi } from '../../services/api'
import { useAuthStore } from '../../store/authStore'
import Button from '../ui/Button'
import Card from '../ui/Card'
import { Sparkles, Loader2, Check, X, Edit } from 'lucide-react'
import { TodoSuggestion } from '../../types'

interface AITodoCreatorProps {
  onSuccess: () => void
  projectId?: number
}

export default function AITodoCreator({ onSuccess, projectId }: AITodoCreatorProps) {
  const { user } = useAuthStore()
  const userId = user?.user_id || 1
  const [text, setText] = useState('')
  const [suggestions, setSuggestions] = useState<TodoSuggestion[]>([])
  const [selectedSuggestions, setSelectedSuggestions] = useState<Set<number>>(new Set())
  const [isAnalyzing, setIsAnalyzing] = useState(false)

  const analyzeMutation = useMutation({
    mutationFn: (data: any) => aiApi.analyzeText(data),
    onSuccess: (response) => {
      setSuggestions(response.suggestions || [])
      setSelectedSuggestions(new Set(response.suggestions?.map((_: any, i: number) => i) || []))
    },
  })

  const createTodoMutation = useMutation({
    mutationFn: (data: any) => todoApi.createTodo(data),
    onSuccess: () => {
      onSuccess()
      setText('')
      setSuggestions([])
      setSelectedSuggestions(new Set())
    },
  })

  const handleAnalyze = () => {
    if (!text.trim()) return
    setIsAnalyzing(true)
    analyzeMutation.mutate(
      {
        free_text: text,
        user_id: userId,
        project_id: projectId,
      },
      {
        onSettled: () => setIsAnalyzing(false),
      }
    )
  }

  const handleCreateTodos = () => {
    const todosToCreate = suggestions
      .filter((_, index) => selectedSuggestions.has(index))
      .map((suggestion) => ({
        title: suggestion.title,
        description: suggestion.description || '',
        priority: suggestion.priority,
        status: 'ToDo',
        category: suggestion.category || null,
        labels: suggestion.labels || [],
        deadline: suggestion.suggested_deadline || null,
        project_id: suggestion.suggested_project_id || projectId || null,
        // user_id comes from auth token
      }))

    todosToCreate.forEach((todo) => {
      createTodoMutation.mutate(todo)
    })
  }

  const toggleSuggestion = (index: number) => {
    const newSet = new Set(selectedSuggestions)
    if (newSet.has(index)) {
      newSet.delete(index)
    } else {
      newSet.add(index)
    }
    setSelectedSuggestions(newSet)
  }

  return (
    <Card>
      <div className="space-y-4">
        <div className="flex items-center gap-2">
          <Sparkles className="h-5 w-5 text-primary-600" />
          <h3 className="text-lg font-semibold text-gray-900">AI-Powered Todo Creation</h3>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Enter your tasks in free text
          </label>
          <textarea
            value={text}
            onChange={(e) => setText(e.target.value)}
            className="input min-h-[120px] resize-none"
            placeholder="e.g., I need to finish the project report by Friday, schedule a meeting with the team, and review the budget proposal..."
            rows={5}
          />
          <p className="text-xs text-gray-500 mt-1">
            Describe your tasks naturally, and AI will extract and organize them for you.
          </p>
        </div>

        <Button
          onClick={handleAnalyze}
          disabled={!text.trim() || isAnalyzing}
          className="w-full"
        >
          {isAnalyzing ? (
            <>
              <Loader2 className="h-4 w-4 mr-2 animate-spin" />
              Analyzing...
            </>
          ) : (
            <>
              <Sparkles className="h-4 w-4 mr-2" />
              Analyze & Suggest Todos
            </>
          )}
        </Button>

        {suggestions.length > 0 && (
          <div className="space-y-3 pt-4 border-t">
            <div className="flex items-center justify-between">
              <h4 className="text-sm font-medium text-gray-700">
                AI Suggestions ({selectedSuggestions.size} selected)
              </h4>
              <div className="flex gap-2">
                <Button
                  size="sm"
                  variant="secondary"
                  onClick={() => setSelectedSuggestions(new Set(suggestions.map((_, i) => i)))}
                >
                  Select All
                </Button>
                <Button
                  size="sm"
                  variant="secondary"
                  onClick={() => setSelectedSuggestions(new Set())}
                >
                  Deselect All
                </Button>
              </div>
            </div>

            <div className="space-y-2 max-h-[400px] overflow-y-auto">
              {suggestions.map((suggestion, index) => (
                <div
                  key={index}
                  className={`p-3 rounded-lg border-2 transition-colors ${
                    selectedSuggestions.has(index)
                      ? 'border-primary-500 bg-primary-50'
                      : 'border-gray-200 bg-white'
                  }`}
                >
                  <div className="flex items-start gap-3">
                    <button
                      onClick={() => toggleSuggestion(index)}
                      className={`mt-1 flex-shrink-0 w-5 h-5 rounded border-2 flex items-center justify-center ${
                        selectedSuggestions.has(index)
                          ? 'border-primary-600 bg-primary-600'
                          : 'border-gray-300'
                      }`}
                    >
                      {selectedSuggestions.has(index) && (
                        <Check className="h-3 w-3 text-white" />
                      )}
                    </button>
                    <div className="flex-1 min-w-0">
                      <h5 className="font-medium text-gray-900">{suggestion.title}</h5>
                      {suggestion.description && (
                        <p className="text-sm text-gray-600 mt-1">{suggestion.description}</p>
                      )}
                      <div className="flex items-center gap-2 mt-2 flex-wrap">
                        <span className={`text-xs px-2 py-1 rounded-full ${
                          suggestion.priority === 'Critical' ? 'bg-red-100 text-red-700' :
                          suggestion.priority === 'High' ? 'bg-orange-100 text-orange-700' :
                          suggestion.priority === 'Medium' ? 'bg-yellow-100 text-yellow-700' :
                          'bg-gray-100 text-gray-700'
                        }`}>
                          {suggestion.priority}
                        </span>
                        {suggestion.category && (
                          <span className="text-xs px-2 py-1 bg-blue-100 text-blue-700 rounded-full">
                            {suggestion.category}
                          </span>
                        )}
                        {suggestion.labels && suggestion.labels.length > 0 && (
                          <div className="flex gap-1 flex-wrap">
                            {suggestion.labels.map((label, i) => (
                              <span key={i} className="text-xs px-2 py-1 bg-gray-100 text-gray-700 rounded-full">
                                {label}
                              </span>
                            ))}
                          </div>
                        )}
                        {suggestion.suggested_deadline && (
                          <span className="text-xs text-gray-500">
                            {new Date(suggestion.suggested_deadline).toLocaleDateString()}
                          </span>
                        )}
                        <span className="text-xs text-gray-400">
                          {Math.round(suggestion.confidence * 100)}% confidence
                        </span>
                      </div>
                      {suggestion.suggested_subtasks && suggestion.suggested_subtasks.length > 0 && (
                        <div className="mt-2">
                          <p className="text-xs text-gray-500 mb-1">Suggested subtasks:</p>
                          <ul className="text-xs text-gray-600 list-disc list-inside">
                            {suggestion.suggested_subtasks.map((subtask, i) => (
                              <li key={i}>{subtask}</li>
                            ))}
                          </ul>
                        </div>
                      )}
                    </div>
                  </div>
                </div>
              ))}
            </div>

            <Button
              onClick={handleCreateTodos}
              disabled={selectedSuggestions.size === 0 || createTodoMutation.isPending}
              className="w-full"
            >
              {createTodoMutation.isPending ? (
                <>
                  <Loader2 className="h-4 w-4 mr-2 animate-spin" />
                  Creating...
                </>
              ) : (
                <>
                  <Check className="h-4 w-4 mr-2" />
                  Create {selectedSuggestions.size} Selected Todo(s)
                </>
              )}
            </Button>
          </div>
        )}
      </div>
    </Card>
  )
}

