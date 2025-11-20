# Standard library
from abc import ABC, abstractmethod

# Internal - from same interface module (direct import, no interface. prefix needed)
from .dataclasses import ExportTodosRequest, ExportTodosResponse


class AbstractExportManagementService(ABC):
    """Interface for export management operations."""
    
    @abstractmethod
    def export_todos(self, request: ExportTodosRequest) -> ExportTodosResponse:
        """
        Export todos in specified format (JSON or CSV).
        
        Args:
            request: ExportTodosRequest with user_id, format, and filter criteria
            
        Returns:
            ExportTodosResponse with exported content and metadata
            
        Raises:
            InvalidExportFormatException: If format is not supported
        """
        pass

