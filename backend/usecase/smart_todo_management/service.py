# Standard library
import logging

# Third-party
# (none needed)

# Internal - from other modules
from externals.llm import interface as llm_interface
from usecase.todo_management import interface as todo_management_interface
from usecase.subtask_management import interface as subtask_management_interface
from utils.date_utils import interface as date_utils_interface

# Internal - from same module
from . import interface

logger = logging.getLogger(__name__)


class SmartTodoManagementService(interface.AbstractSmartTodoManagementService):
    """Service for managing smart todo operations with AI assistance."""
    
    def __init__(
        self,
        llm_service: llm_interface.AbstractLLMService,
        todo_management_service: todo_management_interface.AbstractTodoManagementService,
        subtask_management_service: subtask_management_interface.AbstractSubtaskManagementService | None = None,
        date_time_service: date_utils_interface.AbstractDateTimeService | None = None,
    ):
        self.llm_service = llm_service
        self.todo_management_service = todo_management_service
        self.subtask_management_service = subtask_management_service
        self.date_time_service = date_time_service
    
    def analyze_free_text(self, request: interface.AnalyzeFreeTextRequest) -> interface.AnalyzeFreeTextResponse:
        logger.info(f"Analyzing free text for user: {request.user_id}", extra={"input": request.model_dump()})
        
        if not request.text or not request.text.strip():
            logger.warning("Text analysis failed - text is empty")
            raise interface.InvalidTextException("Text cannot be empty")
        
        try:
            # Call LLM service
            llm_request = llm_interface.AnalyzeTextRequest(
                text=request.text,
                context=request.context
            )
            llm_response = self.llm_service.analyze_text(llm_request)
            
            # Convert LLM suggestions to usecase DTOs
            suggestions = [
                interface.TodoSuggestion(
                    title=sug.title,
                    description=sug.description,
                    priority=sug.priority,
                    category=sug.category,
                    labels=sug.labels,
                    suggested_deadline=sug.suggested_deadline,
                    suggested_project_id=sug.suggested_project_id,
                    suggested_subtasks=sug.suggested_subtasks,
                    confidence=sug.confidence
                )
                for sug in llm_response.suggestions
            ]
            
            response = interface.AnalyzeFreeTextResponse(
                suggestions=suggestions,
                detected_intent=llm_response.detected_intent,
                confidence=llm_response.confidence
            )
            
            logger.info(f"Text analyzed: {len(suggestions)} suggestions, intent={llm_response.detected_intent}", 
                       extra={"output": response.model_dump()})
            return response
            
        except llm_interface.LLMServiceUnavailableException as e:
            logger.exception("LLM service unavailable")
            raise interface.LLMServiceUnavailableException(str(e))
        except Exception as e:
            logger.exception("Failed to analyze text")
            raise interface.SmartTodoManagementInternalServerErrorException(f"Failed to analyze text: {str(e)}")
    
    def create_smart_todo(self, request: interface.CreateSmartTodoRequest) -> interface.CreateSmartTodoResponse:
        logger.info(f"Creating smart todo from suggestion", extra={"input": request.model_dump()})
        
        # Create todo using TodoManagementService
        create_request = todo_management_interface.CreateTodoRequest(
            title=request.suggestion.title,
            description=request.suggestion.description,
            deadline_timestamp_ms=request.suggestion.suggested_deadline,
            priority=request.suggestion.priority,
            category=request.suggestion.category,
            labels=request.suggestion.labels,
            user_id=request.user_id,
            project_id=request.suggestion.suggested_project_id
        )
        
        create_response = self.todo_management_service.create_todo(create_request)
        
        # Create subtasks if suggested
        if request.suggestion.suggested_subtasks and self.subtask_management_service:
            for subtask_title in request.suggestion.suggested_subtasks:
                try:
                    subtask_request = subtask_management_interface.AddSubtaskRequest(
                        todo_id=create_response.todo_id,
                        title=subtask_title,
                        user_id=request.user_id
                    )
                    self.subtask_management_service.add_subtask(subtask_request)
                except Exception as e:
                    logger.warning(f"Failed to create subtask: {subtask_title}, error: {str(e)}")
        
        response = interface.CreateSmartTodoResponse(
            todo_id=create_response.todo_id,
            title=create_response.title,
            created_at=create_response.created_at
        )
        
        logger.info(f"Smart todo created successfully: {response.todo_id}", extra={"output": response.model_dump()})
        return response
    
    def auto_categorize(self, request: interface.AutoCategorizeRequest) -> interface.AutoCategorizeResponse:
        logger.info(f"Auto-categorizing todo: {request.title}", extra={"input": request.model_dump()})
        
        try:
            # Use LLM to analyze and categorize
            text = f"{request.title} {request.description or ''}"
            llm_request = llm_interface.AnalyzeTextRequest(text=text)
            llm_response = self.llm_service.analyze_text(llm_request)
            
            if llm_response.suggestions:
                suggestion = llm_response.suggestions[0]
                response = interface.AutoCategorizeResponse(
                    category=suggestion.category,
                    labels=suggestion.labels,
                    priority=suggestion.priority,
                    confidence=suggestion.confidence
                )
            else:
                response = interface.AutoCategorizeResponse(
                    category=None,
                    labels=[],
                    priority='Medium',
                    confidence=0.0
                )
            
            logger.info(f"Auto-categorization completed", extra={"output": response.model_dump()})
            return response
            
        except Exception as e:
            logger.exception("Failed to auto-categorize")
            raise interface.SmartTodoManagementInternalServerErrorException(f"Failed to auto-categorize: {str(e)}")
    
    def suggest_subtasks(self, request: interface.SuggestSubtasksRequest) -> interface.SuggestSubtasksResponse:
        logger.info(f"Suggesting subtasks for todo: {request.todo_title}", extra={"input": request.model_dump()})
        
        try:
            # Use LLM to generate subtask suggestions
            prompt = f"Suggest subtasks for this todo: {request.todo_title}. {request.todo_description or ''}"
            llm_request = llm_interface.GenerateSuggestionsRequest(
                prompt=prompt,
                max_suggestions=request.max_subtasks
            )
            llm_response = self.llm_service.generate_suggestions(llm_request)
            
            response = interface.SuggestSubtasksResponse(
                subtasks=llm_response.suggestions,
                confidence=llm_response.confidence
            )
            
            logger.info(f"Generated {len(llm_response.suggestions)} subtask suggestions", 
                       extra={"output": response.model_dump()})
            return response
            
        except Exception as e:
            logger.exception("Failed to suggest subtasks")
            raise interface.SmartTodoManagementInternalServerErrorException(f"Failed to suggest subtasks: {str(e)}")
    
    def suggest_next_action(self, request: interface.SuggestNextActionRequest) -> interface.SuggestNextActionResponse:
        logger.info(f"Suggesting next action for user: {request.user_id}", extra={"input": request.model_dump()})
        
        try:
            # Use LLM to suggest next actions
            prompt = "What should I do next? Suggest actionable tasks."
            if request.context:
                prompt += f" Context: {request.context}"
            
            llm_request = llm_interface.GenerateSuggestionsRequest(
                prompt=prompt,
                max_suggestions=5
            )
            llm_response = self.llm_service.generate_suggestions(llm_request)
            
            response = interface.SuggestNextActionResponse(
                suggestions=llm_response.suggestions,
                confidence=llm_response.confidence
            )
            
            logger.info(f"Generated {len(llm_response.suggestions)} next action suggestions", 
                       extra={"output": response.model_dump()})
            return response
            
        except Exception as e:
            logger.exception("Failed to suggest next action")
            raise interface.SmartTodoManagementInternalServerErrorException(f"Failed to suggest next action: {str(e)}")
    
    def conversational_query(self, request: interface.ConversationalQueryRequest) -> interface.ConversationalQueryResponse:
        logger.info(f"Processing conversational query: {request.query[:50]}...", extra={"input": request.model_dump()})
        
        try:
            # Use LLM to analyze query
            llm_request = llm_interface.AnalyzeTextRequest(
                text=request.query,
                context=request.context
            )
            llm_response = self.llm_service.analyze_text(llm_request)
            
            # Generate response based on intent
            if llm_response.detected_intent == 'query':
                response_text = f"I found {len(llm_response.suggestions)} relevant items based on your query."
            else:
                response_text = f"I can help you with that. Here are {len(llm_response.suggestions)} suggestions."
            
            # Convert suggestions
            suggestions = [
                interface.TodoSuggestion(
                    title=sug.title,
                    description=sug.description,
                    priority=sug.priority,
                    category=sug.category,
                    labels=sug.labels,
                    suggested_deadline=sug.suggested_deadline,
                    suggested_project_id=sug.suggested_project_id,
                    suggested_subtasks=sug.suggested_subtasks,
                    confidence=sug.confidence
                )
                for sug in llm_response.suggestions
            ]
            
            response = interface.ConversationalQueryResponse(
                response=response_text,
                suggestions=suggestions,
                detected_intent=llm_response.detected_intent,
                confidence=llm_response.confidence
            )
            
            logger.info(f"Conversational query processed: intent={llm_response.detected_intent}", 
                       extra={"output": response.model_dump()})
            return response
            
        except Exception as e:
            logger.exception("Failed to process conversational query")
            raise interface.SmartTodoManagementInternalServerErrorException(f"Failed to process query: {str(e)}")

