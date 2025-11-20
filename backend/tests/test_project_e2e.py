# Standard library
import json

# Third-party
from django.test import TestCase, Client

# Internal - from other modules
from repository.project.models import Project, ProjectMember
from repository.project import interface as project_repository_interface
from usecase.project_management import interface as project_management_interface
from runner.bootstrap import bootstrapper

# Internal - from same module
# (none needed)


class ProjectEndToEndTest(TestCase):
    """End-to-end tests for Project models and processes using Django TestCase."""
    
    def setUp(self):
        """Set up test data."""
        self.client = Client()
        
        # Get services from bootstrapper
        self.project_management_service = bootstrapper.get_project_management_service()
        self.date_time_service = bootstrapper.date_time_service
        
        # Create test users
        self.owner_id = 1
        self.member_id = 2
        self.other_user_id = 3
        
        # Get current timestamp
        now_dto = self.date_time_service.now()
        self.current_timestamp = now_dto.timestamp_ms
    
    def test_project_model_creation(self):
        """Test Project model creation and basic operations."""
        # Create project directly in database
        project = Project.objects.create(
            name="Test Project",
            description="Test Description",
            is_private=True,
            owner_id=self.owner_id,
            created_at=self.current_timestamp,
            updated_at=self.current_timestamp
        )
        
        # Verify project was created
        self.assertIsNotNone(project.id)
        self.assertEqual(project.name, "Test Project")
        self.assertEqual(project.description, "Test Description")
        self.assertTrue(project.is_private)
        self.assertEqual(project.owner_id, self.owner_id)
        self.assertEqual(project.created_at, self.current_timestamp)
        self.assertEqual(project.updated_at, self.current_timestamp)
        
        # Test string representation
        self.assertEqual(str(project), "Test Project")
    
    def test_project_member_model_creation(self):
        """Test ProjectMember model creation and basic operations."""
        # Create project first
        project = Project.objects.create(
            name="Test Project",
            description="Test Description",
            is_private=True,
            owner_id=self.owner_id,
            created_at=self.current_timestamp,
            updated_at=self.current_timestamp
        )
        
        # Create project member
        member = ProjectMember.objects.create(
            project_id=project.id,
            user_id=self.member_id,
            role='Member',
            joined_at=self.current_timestamp
        )
        
        # Verify member was created
        self.assertIsNotNone(member.id)
        self.assertEqual(member.project_id, project.id)
        self.assertEqual(member.user_id, self.member_id)
        self.assertEqual(member.role, 'Member')
        self.assertEqual(member.joined_at, self.current_timestamp)
        
        # Test string representation
        self.assertIn(str(project.id), str(member))
        self.assertIn(str(self.member_id), str(member))
    
    def test_project_repository_service_create(self):
        """Test ProjectRepositoryService create operation."""
        # Get repository service from bootstrapper
        service = bootstrapper.project_repo
        
        # Create project via repository
        create_request = project_repository_interface.ProjectCreateRequest(
            name="Repository Test Project",
            description="Repository Test Description",
            is_private=False,
            owner_id=self.owner_id,
            created_at=self.current_timestamp,
            updated_at=self.current_timestamp
        )
        
        result = service.create(create_request)
        
        # Verify result
        self.assertIsNotNone(result.project_id)
        self.assertEqual(result.name, "Repository Test Project")
        self.assertEqual(result.description, "Repository Test Description")
        self.assertFalse(result.is_private)
        self.assertEqual(result.owner_id, self.owner_id)
        
        # Verify in database
        project = Project.objects.get(id=result.project_id)
        self.assertEqual(project.name, "Repository Test Project")
    
    def test_project_repository_service_get_by_id(self):
        """Test ProjectRepositoryService get_by_id operation."""
        # Get repository service from bootstrapper
        service = bootstrapper.project_repo
        
        # Create project first
        project = Project.objects.create(
            name="Get Test Project",
            description="Get Test Description",
            is_private=True,
            owner_id=self.owner_id,
            created_at=self.current_timestamp,
            updated_at=self.current_timestamp
        )
        
        # Get project via repository
        result = service.get_by_id(project.id)
        
        # Verify result
        self.assertIsNotNone(result)
        self.assertEqual(result.project_id, project.id)
        self.assertEqual(result.name, "Get Test Project")
        
        # Test non-existent project
        result_none = service.get_by_id(99999)
        self.assertIsNone(result_none)
    
    def test_project_repository_service_update(self):
        """Test ProjectRepositoryService update operation."""
        # Get repository service from bootstrapper
        service = bootstrapper.project_repo
        
        # Create project first
        project = Project.objects.create(
            name="Update Test Project",
            description="Original Description",
            is_private=True,
            owner_id=self.owner_id,
            created_at=self.current_timestamp,
            updated_at=self.current_timestamp
        )
        
        # Update project
        new_timestamp = self.current_timestamp + 1000
        update_request = project_repository_interface.ProjectUpdateRequest(
            name="Updated Project Name",
            description="Updated Description",
            is_private=False,
            updated_at=new_timestamp
        )
        
        result = service.update(project.id, update_request)
        
        # Verify result
        self.assertEqual(result.name, "Updated Project Name")
        self.assertEqual(result.description, "Updated Description")
        self.assertFalse(result.is_private)
        self.assertEqual(result.updated_at, new_timestamp)
        
        # Verify in database
        project.refresh_from_db()
        self.assertEqual(project.name, "Updated Project Name")
        self.assertEqual(project.updated_at, new_timestamp)
    
    def test_project_repository_service_delete(self):
        """Test ProjectRepositoryService delete operation."""
        # Get repository service from bootstrapper
        service = bootstrapper.project_repo
        
        # Create project first
        project = Project.objects.create(
            name="Delete Test Project",
            description="Delete Test Description",
            is_private=True,
            owner_id=self.owner_id,
            created_at=self.current_timestamp,
            updated_at=self.current_timestamp
        )
        project_id = project.id
        
        # Delete project
        service.delete(project_id)
        
        # Verify project is deleted
        self.assertFalse(Project.objects.filter(id=project_id).exists())
    
    def test_project_repository_service_member_operations(self):
        """Test ProjectRepositoryService member operations."""
        # Get repository service from bootstrapper
        service = bootstrapper.project_repo
        
        # Create project first
        project = Project.objects.create(
            name="Member Test Project",
            description="Member Test Description",
            is_private=True,
            owner_id=self.owner_id,
            created_at=self.current_timestamp,
            updated_at=self.current_timestamp
        )
        
        # Create member
        member_create_request = project_repository_interface.ProjectMemberCreateRequest(
            project_id=project.id,
            user_id=self.member_id,
            role='Admin',
            joined_at=self.current_timestamp
        )
        
        member_result = service.create_member(member_create_request)
        
        # Verify member was created
        self.assertIsNotNone(member_result.member_id)
        self.assertEqual(member_result.project_id, project.id)
        self.assertEqual(member_result.user_id, self.member_id)
        self.assertEqual(member_result.role, 'Admin')
        
        # Get member
        member = service.get_member(project.id, self.member_id)
        self.assertIsNotNone(member)
        self.assertEqual(member.role, 'Admin')
        
        # Update member role
        member_update_request = project_repository_interface.ProjectMemberUpdateRequest(
            role='Member'
        )
        updated_member = service.update_member(project.id, self.member_id, member_update_request)
        self.assertEqual(updated_member.role, 'Member')
        
        # Delete member
        service.delete_member(project.id, self.member_id)
        deleted_member = service.get_member(project.id, self.member_id)
        self.assertIsNone(deleted_member)
    
    def test_project_management_service_create_project(self):
        """Test ProjectManagementService create_project operation."""
        # Use service from bootstrapper
        service = self.project_management_service
        
        # Create project via usecase
        create_request = project_management_interface.CreateProjectRequest(
            name="UseCase Test Project",
            description="UseCase Test Description",
            is_private=True,
            owner_id=self.owner_id
        )
        
        result = service.create_project(create_request)
        
        # Verify result
        self.assertIsNotNone(result.project_id)
        self.assertEqual(result.name, "UseCase Test Project")
        self.assertTrue(result.is_private)
        self.assertEqual(result.owner_id, self.owner_id)
        self.assertIsNotNone(result.created_at)
        
        # Verify project exists in database
        project = Project.objects.get(id=result.project_id)
        self.assertEqual(project.name, "UseCase Test Project")
        
        # Verify owner was added as member
        member = ProjectMember.objects.get(project_id=result.project_id, user_id=self.owner_id)
        self.assertEqual(member.role, 'Owner')
    
    def test_project_management_service_get_project_by_id(self):
        """Test ProjectManagementService get_project_by_id operation."""
        # Use service from bootstrapper
        service = self.project_management_service
        
        # Create project first
        project = Project.objects.create(
            name="Get UseCase Test Project",
            description="Get UseCase Test Description",
            is_private=False,  # Public project
            owner_id=self.owner_id,
            created_at=self.current_timestamp,
            updated_at=self.current_timestamp
        )
        
        # Get project as owner
        get_request = project_management_interface.GetProjectRequest(
            project_id=project.id,
            user_id=self.owner_id
        )
        
        result = service.get_project_by_id(get_request)
        self.assertEqual(result.project_id, project.id)
        self.assertEqual(result.name, "Get UseCase Test Project")
        
        # Get project as other user (public project)
        get_request_other = project_management_interface.GetProjectRequest(
            project_id=project.id,
            user_id=self.other_user_id
        )
        
        result_other = service.get_project_by_id(get_request_other)
        self.assertEqual(result_other.project_id, project.id)
        
        # Test private project access denied
        project.is_private = True
        project.save()
        
        with self.assertRaises(project_management_interface.ProjectAccessDeniedException):
            service.get_project_by_id(get_request_other)
    
    def test_project_management_service_update_project(self):
        """Test ProjectManagementService update_project operation."""
        # Use service from bootstrapper
        service = self.project_management_service
        
        # Create project first
        project = Project.objects.create(
            name="Update UseCase Test Project",
            description="Original Description",
            is_private=True,
            owner_id=self.owner_id,
            created_at=self.current_timestamp,
            updated_at=self.current_timestamp
        )
        
        # Add member as admin
        ProjectMember.objects.create(
            project_id=project.id,
            user_id=self.member_id,
            role='Admin',
            joined_at=self.current_timestamp
        )
        
        # Update as owner
        update_request = project_management_interface.UpdateProjectRequest(
            project_id=project.id,
            user_id=self.owner_id,
            name="Updated UseCase Project Name",
            description="Updated Description"
        )
        
        result = service.update_project(update_request)
        self.assertEqual(result.name, "Updated UseCase Project Name")
        self.assertEqual(result.description, "Updated Description")
        
        # Update as admin
        update_request_admin = project_management_interface.UpdateProjectRequest(
            project_id=project.id,
            user_id=self.member_id,
            is_private=False
        )
        
        result_admin = service.update_project(update_request_admin)
        self.assertFalse(result_admin.is_private)
        
        # Test access denied for member
        ProjectMember.objects.filter(project_id=project.id, user_id=self.member_id).update(role='Member')
        
        with self.assertRaises(project_management_interface.ProjectAccessDeniedException):
            update_request_member = project_management_interface.UpdateProjectRequest(
                project_id=project.id,
                user_id=self.member_id,
                name="Should Fail"
            )
            service.update_project(update_request_member)
    
    def test_project_management_service_delete_project(self):
        """Test ProjectManagementService delete_project operation."""
        # Use service from bootstrapper
        service = self.project_management_service
        
        # Create project first
        project = Project.objects.create(
            name="Delete UseCase Test Project",
            description="Delete UseCase Test Description",
            is_private=True,
            owner_id=self.owner_id,
            created_at=self.current_timestamp,
            updated_at=self.current_timestamp
        )
        
        # Add members
        ProjectMember.objects.create(
            project_id=project.id,
            user_id=self.member_id,
            role='Member',
            joined_at=self.current_timestamp
        )
        
        # Delete project
        delete_request = project_management_interface.DeleteProjectRequest(
            project_id=project.id,
            user_id=self.owner_id
        )
        
        result = service.delete_project(delete_request)
        self.assertTrue(result.success)
        
        # Verify project and members are deleted
        self.assertFalse(Project.objects.filter(id=project.id).exists())
        self.assertFalse(ProjectMember.objects.filter(project_id=project.id).exists())
        
        # Test access denied for non-owner
        project2 = Project.objects.create(
            name="Delete Test Project 2",
            description="Test",
            is_private=True,
            owner_id=self.owner_id,
            created_at=self.current_timestamp,
            updated_at=self.current_timestamp
        )
        
        with self.assertRaises(project_management_interface.ProjectAccessDeniedException):
            delete_request_denied = project_management_interface.DeleteProjectRequest(
                project_id=project2.id,
                user_id=self.member_id
            )
            service.delete_project(delete_request_denied)
    
    def test_project_management_service_member_operations(self):
        """Test ProjectManagementService member operations."""
        # Use service from bootstrapper
        service = self.project_management_service
        
        # Create project first
        project = Project.objects.create(
            name="Member UseCase Test Project",
            description="Member UseCase Test Description",
            is_private=True,
            owner_id=self.owner_id,
            created_at=self.current_timestamp,
            updated_at=self.current_timestamp
        )
        
        # Add member as owner
        add_request = project_management_interface.AddMemberRequest(
            project_id=project.id,
            user_id=self.owner_id,
            new_user_id=self.member_id,
            role='Admin'
        )
        
        add_result = service.add_member(add_request)
        self.assertEqual(add_result.user_id, self.member_id)
        self.assertEqual(add_result.role, 'Admin')
        
        # Update member role as owner
        update_role_request = project_management_interface.UpdateMemberRoleRequest(
            project_id=project.id,
            user_id=self.owner_id,
            update_user_id=self.member_id,
            new_role='Member'
        )
        
        update_role_result = service.update_member_role(update_role_request)
        self.assertEqual(update_role_result.role, 'Member')
        
        # Remove member as owner
        remove_request = project_management_interface.RemoveMemberRequest(
            project_id=project.id,
            user_id=self.owner_id,
            remove_user_id=self.member_id
        )
        
        remove_result = service.remove_member(remove_request)
        self.assertTrue(remove_result.success)
        
        # Verify member is removed
        member = ProjectMember.objects.filter(project_id=project.id, user_id=self.member_id).first()
        self.assertIsNone(member)
    
    def test_rest_api_create_project(self):
        """Test REST API create project endpoint."""
        url = '/api/projects/create/'
        data = {
            'name': 'REST API Test Project',
            'description': 'REST API Test Description',
            'is_private': True,
            'owner_id': self.owner_id
        }
        
        response = self.client.post(
            url,
            data=json.dumps(data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 201)
        response_data = json.loads(response.content)
        self.assertEqual(response_data['name'], 'REST API Test Project')
        self.assertIn('project_id', response_data)
        self.assertIn('created_at', response_data)
        
        # Verify project exists in database
        project = Project.objects.get(id=response_data['project_id'])
        self.assertEqual(project.name, 'REST API Test Project')
    
    def test_rest_api_get_project(self):
        """Test REST API get project endpoint."""
        # Create project first
        project = Project.objects.create(
            name='REST Get Test Project',
            description='REST Get Test Description',
            is_private=False,  # Public
            owner_id=self.owner_id,
            created_at=self.current_timestamp,
            updated_at=self.current_timestamp
        )
        
        url = f'/api/projects/{project.id}/?user_id={self.owner_id}'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.content)
        self.assertEqual(response_data['project_id'], project.id)
        self.assertEqual(response_data['name'], 'REST Get Test Project')
    
    def test_rest_api_get_projects_list(self):
        """Test REST API get projects list endpoint."""
        # Create multiple projects
        for i in range(3):
            Project.objects.create(
                name=f'REST List Test Project {i+1}',
                description=f'Description {i+1}',
                is_private=False,
                owner_id=self.owner_id,
                created_at=self.current_timestamp + i,
                updated_at=self.current_timestamp + i
            )
        
        url = f'/api/projects/?user_id={self.owner_id}'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.content)
        self.assertIn('projects', response_data)
        self.assertIn('total', response_data)
        self.assertGreaterEqual(len(response_data['projects']), 3)
    
    def test_rest_api_update_project(self):
        """Test REST API update project endpoint."""
        # Create project first
        project = Project.objects.create(
            name='REST Update Test Project',
            description='Original Description',
            is_private=True,
            owner_id=self.owner_id,
            created_at=self.current_timestamp,
            updated_at=self.current_timestamp
        )
        
        url = f'/api/projects/{project.id}/update/'
        data = {
            'user_id': self.owner_id,
            'name': 'Updated REST Project Name',
            'description': 'Updated Description',
            'is_private': False
        }
        
        response = self.client.put(
            url,
            data=json.dumps(data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.content)
        self.assertEqual(response_data['name'], 'Updated REST Project Name')
        self.assertEqual(response_data['description'], 'Updated Description')
        self.assertFalse(response_data['is_private'])
    
    def test_rest_api_delete_project(self):
        """Test REST API delete project endpoint."""
        # Create project first
        project = Project.objects.create(
            name='REST Delete Test Project',
            description='REST Delete Test Description',
            is_private=True,
            owner_id=self.owner_id,
            created_at=self.current_timestamp,
            updated_at=self.current_timestamp
        )
        project_id = project.id
        
        url = f'/api/projects/{project_id}/delete/?user_id={self.owner_id}'
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.content)
        self.assertTrue(response_data['success'])
        
        # Verify project is deleted
        self.assertFalse(Project.objects.filter(id=project_id).exists())
    
    def test_rest_api_add_member(self):
        """Test REST API add member endpoint."""
        # Create project first
        project = Project.objects.create(
            name='REST Add Member Test Project',
            description='Test Description',
            is_private=True,
            owner_id=self.owner_id,
            created_at=self.current_timestamp,
            updated_at=self.current_timestamp
        )
        
        url = f'/api/projects/{project.id}/members/add/'
        data = {
            'user_id': self.owner_id,
            'new_user_id': self.member_id,
            'role': 'Admin'
        }
        
        response = self.client.post(
            url,
            data=json.dumps(data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 201)
        response_data = json.loads(response.content)
        self.assertEqual(response_data['user_id'], self.member_id)
        self.assertEqual(response_data['role'], 'Admin')
        
        # Verify member exists in database
        member = ProjectMember.objects.get(project_id=project.id, user_id=self.member_id)
        self.assertEqual(member.role, 'Admin')
    
    def test_rest_api_remove_member(self):
        """Test REST API remove member endpoint."""
        # Create project and member first
        project = Project.objects.create(
            name='REST Remove Member Test Project',
            description='Test Description',
            is_private=True,
            owner_id=self.owner_id,
            created_at=self.current_timestamp,
            updated_at=self.current_timestamp
        )
        
        ProjectMember.objects.create(
            project_id=project.id,
            user_id=self.member_id,
            role='Member',
            joined_at=self.current_timestamp
        )
        
        url = f'/api/projects/{project.id}/members/remove/'
        data = {
            'user_id': self.owner_id,
            'remove_user_id': self.member_id
        }
        
        response = self.client.delete(
            url,
            data=json.dumps(data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.content)
        self.assertTrue(response_data['success'])
        
        # Verify member is removed
        self.assertFalse(ProjectMember.objects.filter(project_id=project.id, user_id=self.member_id).exists())
    
    def test_rest_api_update_member_role(self):
        """Test REST API update member role endpoint."""
        # Create project and member first
        project = Project.objects.create(
            name='REST Update Role Test Project',
            description='Test Description',
            is_private=True,
            owner_id=self.owner_id,
            created_at=self.current_timestamp,
            updated_at=self.current_timestamp
        )
        
        ProjectMember.objects.create(
            project_id=project.id,
            user_id=self.member_id,
            role='Member',
            joined_at=self.current_timestamp
        )
        
        url = f'/api/projects/{project.id}/members/update-role/'
        data = {
            'user_id': self.owner_id,
            'update_user_id': self.member_id,
            'new_role': 'Admin'
        }
        
        response = self.client.put(
            url,
            data=json.dumps(data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.content)
        self.assertEqual(response_data['role'], 'Admin')
        
        # Verify role updated in database
        member = ProjectMember.objects.get(project_id=project.id, user_id=self.member_id)
        self.assertEqual(member.role, 'Admin')
    
    def test_full_workflow_e2e(self):
        """Test complete end-to-end workflow from API to database."""
        # Step 1: Create project via REST API
        create_url = '/api/projects/create/'
        create_data = {
            'name': 'E2E Workflow Project',
            'description': 'End-to-end test project',
            'is_private': True,
            'owner_id': self.owner_id
        }
        
        create_response = self.client.post(
            create_url,
            data=json.dumps(create_data),
            content_type='application/json'
        )
        self.assertEqual(create_response.status_code, 201)
        project_data = json.loads(create_response.content)
        project_id = project_data['project_id']
        
        # Step 2: Verify project in database
        project = Project.objects.get(id=project_id)
        self.assertEqual(project.name, 'E2E Workflow Project')
        self.assertEqual(project.owner_id, self.owner_id)
        
        # Step 3: Verify owner is added as member
        owner_member = ProjectMember.objects.get(project_id=project_id, user_id=self.owner_id)
        self.assertEqual(owner_member.role, 'Owner')
        
        # Step 4: Add member via REST API
        add_member_url = f'/api/projects/{project_id}/members/add/'
        add_member_data = {
            'user_id': self.owner_id,
            'new_user_id': self.member_id,
            'role': 'Admin'
        }
        
        add_member_response = self.client.post(
            add_member_url,
            data=json.dumps(add_member_data),
            content_type='application/json'
        )
        self.assertEqual(add_member_response.status_code, 201)
        
        # Step 5: Verify member in database
        member = ProjectMember.objects.get(project_id=project_id, user_id=self.member_id)
        self.assertEqual(member.role, 'Admin')
        
        # Step 6: Update member role via REST API
        update_role_url = f'/api/projects/{project_id}/members/update-role/'
        update_role_data = {
            'user_id': self.owner_id,
            'update_user_id': self.member_id,
            'new_role': 'Member'
        }
        
        update_role_response = self.client.put(
            update_role_url,
            data=json.dumps(update_role_data),
            content_type='application/json'
        )
        self.assertEqual(update_role_response.status_code, 200)
        
        # Step 7: Verify role updated in database
        member.refresh_from_db()
        self.assertEqual(member.role, 'Member')
        
        # Step 8: Update project via REST API
        update_url = f'/api/projects/{project_id}/update/'
        update_data = {
            'user_id': self.owner_id,
            'name': 'Updated E2E Project',
            'is_private': False
        }
        
        update_response = self.client.put(
            update_url,
            data=json.dumps(update_data),
            content_type='application/json'
        )
        self.assertEqual(update_response.status_code, 200)
        
        # Step 9: Verify project updated in database
        project.refresh_from_db()
        self.assertEqual(project.name, 'Updated E2E Project')
        self.assertFalse(project.is_private)
        
        # Step 10: Get project via REST API
        get_url = f'/api/projects/{project_id}/?user_id={self.owner_id}'
        get_response = self.client.get(get_url)
        self.assertEqual(get_response.status_code, 200)
        get_data = json.loads(get_response.content)
        self.assertEqual(get_data['name'], 'Updated E2E Project')
        
        # Step 11: Remove member via REST API
        remove_member_url = f'/api/projects/{project_id}/members/remove/'
        remove_member_data = {
            'user_id': self.owner_id,
            'remove_user_id': self.member_id
        }
        
        remove_member_response = self.client.delete(
            remove_member_url,
            data=json.dumps(remove_member_data),
            content_type='application/json'
        )
        self.assertEqual(remove_member_response.status_code, 200)
        
        # Step 12: Verify member removed from database
        self.assertFalse(ProjectMember.objects.filter(project_id=project_id, user_id=self.member_id).exists())
        
        # Step 13: Delete project via REST API
        delete_url = f'/api/projects/{project_id}/delete/?user_id={self.owner_id}'
        delete_response = self.client.delete(delete_url)
        self.assertEqual(delete_response.status_code, 200)
        
        # Step 14: Verify project and all members deleted from database
        self.assertFalse(Project.objects.filter(id=project_id).exists())
        self.assertFalse(ProjectMember.objects.filter(project_id=project_id).exists())

