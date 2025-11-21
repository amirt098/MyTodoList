"""
URL configuration for runner project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.http import JsonResponse
from django.views import View

# Internal - from other modules
from presentation.rest.auth_views import (
    RegisterView,
    LoginView,
    PasswordRecoveryView,
    UpdateProfileView
)
from presentation.rest.todo_views import (
    CreateTodoView,
    GetTodoView,
    GetTodosView,
    UpdateTodoView,
    DeleteTodoView
)
from presentation.rest.project_views import (
    CreateProjectView,
    GetProjectView,
    GetProjectsView,
    UpdateProjectView,
    DeleteProjectView,
    AddMemberView,
    RemoveMemberView,
    UpdateMemberRoleView
)
from presentation.rest.kanban_views import (
    GetKanbanBoardView,
    MoveTodoView,
    CreateColumnView,
    DeleteColumnView,
    ReorderColumnsView
)
from presentation.rest.advanced_todo_views import (
    AddSubtaskView,
    UpdateSubtaskView,
    DeleteSubtaskView,
    MarkSubtaskDoneView,
    GetSubtasksView,
    SetDependencyView,
    RemoveDependencyView,
    ValidateDependencyView,
    GetDependencyChainView
)
from presentation.rest.advanced_filtering_views import (
    GetAllMyTodosView,
    SaveFilterView,
    GetSavedFiltersView,
    DeleteSavedFilterView,
    BulkUpdateView,
    BulkDeleteView,
    ExportTodosView
)
from presentation.rest.reminder_views import (
    CreateReminderView,
    UpdateReminderView,
    DeleteReminderView,
    GetRemindersView,
    ProcessRemindersView
)
from presentation.rest.ai_views import (
    AnalyzeTextView,
    CreateSmartTodoView,
    AutoCategorizeView,
    SuggestSubtasksView,
    SuggestNextActionView,
    ConversationalQueryView
)


class APIRootView(View):
    """Root API endpoint that provides API information."""
    
    def get(self, request):
        return JsonResponse({
            "message": "MyTodoList API",
            "version": "1.0.0",
            "status": "running",
            "endpoints": {
                "auth": "/api/auth/",
                "todos": "/api/todos/",
                "projects": "/api/projects/",
                "kanban": "/api/kanban/",
                "reminders": "/api/reminders/",
                "ai": "/api/ai/",
                "filters": "/api/filters/",
                "admin": "/admin/"
            },
            "frontend": "http://localhost:3000"
        })


urlpatterns = [
    path('', APIRootView.as_view(), name='api-root'),
    path('admin/', admin.site.urls),
    # Auth endpoints
    path('api/auth/register/', RegisterView.as_view(), name='register'),
    path('api/auth/login/', LoginView.as_view(), name='login'),
    path('api/auth/password-recovery/', PasswordRecoveryView.as_view(), name='password-recovery'),
    path('api/auth/profile/', UpdateProfileView.as_view(), name='update-profile'),
    # Todo endpoints
    path('api/todos/', GetTodosView.as_view(), name='get-todos'),
    path('api/todos/create/', CreateTodoView.as_view(), name='create-todo'),
    path('api/todos/<int:todo_id>/', GetTodoView.as_view(), name='get-todo'),
    path('api/todos/<int:todo_id>/update/', UpdateTodoView.as_view(), name='update-todo'),
    path('api/todos/<int:todo_id>/delete/', DeleteTodoView.as_view(), name='delete-todo'),
    # Project endpoints
    path('api/projects/', GetProjectsView.as_view(), name='get-projects'),
    path('api/projects/create/', CreateProjectView.as_view(), name='create-project'),
    path('api/projects/<int:project_id>/', GetProjectView.as_view(), name='get-project'),
    path('api/projects/<int:project_id>/update/', UpdateProjectView.as_view(), name='update-project'),
    path('api/projects/<int:project_id>/delete/', DeleteProjectView.as_view(), name='delete-project'),
    path('api/projects/<int:project_id>/members/add/', AddMemberView.as_view(), name='add-member'),
    path('api/projects/<int:project_id>/members/remove/', RemoveMemberView.as_view(), name='remove-member'),
    path('api/projects/<int:project_id>/members/update-role/', UpdateMemberRoleView.as_view(), name='update-member-role'),
    # Kanban endpoints
    path('api/kanban/board/', GetKanbanBoardView.as_view(), name='get-kanban-board'),
    path('api/kanban/move-todo/', MoveTodoView.as_view(), name='move-todo'),
    path('api/kanban/columns/create/', CreateColumnView.as_view(), name='create-column'),
    path('api/kanban/columns/<int:column_id>/delete/', DeleteColumnView.as_view(), name='delete-column'),
    path('api/kanban/columns/reorder/', ReorderColumnsView.as_view(), name='reorder-columns'),
    # Subtask endpoints
    path('api/todos/<int:todo_id>/subtasks/', GetSubtasksView.as_view(), name='get-subtasks'),
    path('api/todos/<int:todo_id>/subtasks/add/', AddSubtaskView.as_view(), name='add-subtask'),
    path('api/subtasks/<int:subtask_id>/update/', UpdateSubtaskView.as_view(), name='update-subtask'),
    path('api/subtasks/<int:subtask_id>/delete/', DeleteSubtaskView.as_view(), name='delete-subtask'),
    path('api/subtasks/<int:subtask_id>/mark-done/', MarkSubtaskDoneView.as_view(), name='mark-subtask-done'),
    # Dependency endpoints
    path('api/todos/dependencies/set/', SetDependencyView.as_view(), name='set-dependency'),
    path('api/todos/<int:todo_id>/dependencies/remove/', RemoveDependencyView.as_view(), name='remove-dependency'),
    path('api/todos/<int:todo_id>/dependencies/validate/', ValidateDependencyView.as_view(), name='validate-dependency'),
    path('api/todos/<int:todo_id>/dependencies/chain/', GetDependencyChainView.as_view(), name='get-dependency-chain'),
    # Advanced filtering endpoints
    path('api/todos/all-my-todos/', GetAllMyTodosView.as_view(), name='get-all-my-todos'),
    path('api/filters/save/', SaveFilterView.as_view(), name='save-filter'),
    path('api/filters/', GetSavedFiltersView.as_view(), name='get-saved-filters'),
    path('api/filters/<int:filter_id>/delete/', DeleteSavedFilterView.as_view(), name='delete-saved-filter'),
    path('api/todos/bulk-update/', BulkUpdateView.as_view(), name='bulk-update'),
    path('api/todos/bulk-delete/', BulkDeleteView.as_view(), name='bulk-delete'),
    path('api/todos/export/', ExportTodosView.as_view(), name='export-todos'),
    # Reminder endpoints
    path('api/reminders/', GetRemindersView.as_view(), name='get-reminders'),
    path('api/reminders/create/', CreateReminderView.as_view(), name='create-reminder'),
    path('api/reminders/<int:reminder_id>/update/', UpdateReminderView.as_view(), name='update-reminder'),
    path('api/reminders/<int:reminder_id>/delete/', DeleteReminderView.as_view(), name='delete-reminder'),
    path('api/reminders/process/', ProcessRemindersView.as_view(), name='process-reminders'),
    # AI endpoints
    path('api/ai/analyze-text/', AnalyzeTextView.as_view(), name='analyze-text'),
    path('api/ai/create-smart-todo/', CreateSmartTodoView.as_view(), name='create-smart-todo'),
    path('api/ai/auto-categorize/', AutoCategorizeView.as_view(), name='auto-categorize'),
    path('api/ai/suggest-subtasks/', SuggestSubtasksView.as_view(), name='suggest-subtasks'),
    path('api/ai/suggest-next-action/', SuggestNextActionView.as_view(), name='suggest-next-action'),
    path('api/ai/query/', ConversationalQueryView.as_view(), name='conversational-query'),
]
