# Standard library
import json
import logging
import os

# Third-party
from openai import OpenAI
from django.conf import settings

# Internal - from other modules
# (none needed)

# Internal - from same module
from . import interface

logger = logging.getLogger(__name__)


class LLMService(interface.AbstractLLMService):
    """
    LLM service implementation using OpenAI-compatible API (DeepSeek).
    
    Uses OpenAI SDK which is compatible with DeepSeek API.
    """
    
    def __init__(self):
        # Get API configuration from settings
        self.api_key = getattr(settings, 'DEEPSEEK_API_KEY', os.getenv('DEEPSEEK_API_KEY', ''))
        self.base_url = getattr(settings, 'DEEPSEEK_API_BASE_URL', 'https://api.deepseek.com/v1')
        self.model = getattr(settings, 'DEEPSEEK_MODEL', 'deepseek-chat')
        
        # Initialize OpenAI client (compatible with DeepSeek)
        if self.api_key:
            self.client = OpenAI(
                api_key=self.api_key,
                base_url=self.base_url
            )
        else:
            self.client = None
            logger.warning("DeepSeek API key not configured. LLM features will be limited.")
    
    def analyze_text(self, request: interface.AnalyzeTextRequest) -> interface.AnalyzeTextResponse:
        logger.info(f"Analyzing text with LLM: {request.text[:50]}...", extra={"input": request.model_dump()})
        
        if not self.client:
            logger.warning("LLM client not available, using fallback")
            return self._fallback_analyze_text(request)
        
        try:
            # Build context for the prompt
            context_str = ""
            if request.context:
                if 'user_id' in request.context:
                    context_str += f"User ID: {request.context['user_id']}. "
                if 'existing_todos' in request.context:
                    context_str += f"User has {len(request.context['existing_todos'])} existing todos. "
            
            # Create prompt for LLM
            system_prompt = """You are a helpful assistant that extracts todo items from free text.
Analyze the text and extract todo information including:
- Title (required)
- Description (optional)
- Priority (Low, Medium, High, Critical)
- Category (work, personal, shopping, health, etc.)
- Labels (array of relevant tags)
- Suggested deadline (timestamp in milliseconds, or null)
- Suggested subtasks (array of strings)

Return a JSON array of todo suggestions. Each suggestion should have:
{
  "title": "string",
  "description": "string or null",
  "priority": "Low|Medium|High|Critical",
  "category": "string or null",
  "labels": ["string"],
  "suggested_deadline": number or null,
  "suggested_subtasks": ["string"],
  "confidence": 0.0-1.0
}

Also detect the intent: 'create_todo', 'query', 'update', or 'other'.
Return confidence score (0.0-1.0) for the analysis."""
            
            user_prompt = f"""{context_str}
Text to analyze:
{request.text}

Extract todo information and return JSON in this format:
{{
  "intent": "create_todo|query|update|other",
  "confidence": 0.0-1.0,
  "suggestions": [
    {{
      "title": "...",
      "description": "...",
      "priority": "...",
      "category": "...",
      "labels": [...],
      "suggested_deadline": ...,
      "suggested_subtasks": [...],
      "confidence": ...
    }}
  ]
}}"""
            
            # Call DeepSeek API
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.7,
                response_format={"type": "json_object"}
            )
            
            # Parse response
            content = response.choices[0].message.content
            result = json.loads(content)
            
            # Convert to response DTO
            suggestions = []
            for sug_data in result.get('suggestions', []):
                suggestion = interface.TodoSuggestion(
                    title=sug_data.get('title', ''),
                    description=sug_data.get('description'),
                    priority=sug_data.get('priority', 'Medium'),
                    category=sug_data.get('category'),
                    labels=sug_data.get('labels', []),
                    suggested_deadline=sug_data.get('suggested_deadline'),
                    suggested_project_id=sug_data.get('suggested_project_id'),
                    suggested_subtasks=sug_data.get('suggested_subtasks', []),
                    confidence=sug_data.get('confidence', 0.7)
                )
                suggestions.append(suggestion)
            
            response_dto = interface.AnalyzeTextResponse(
                suggestions=suggestions,
                detected_intent=result.get('intent', 'create_todo'),
                confidence=result.get('confidence', 0.7),
                raw_response=content
            )
            
            logger.info(f"LLM analysis completed: {len(suggestions)} suggestions, intent={result.get('intent')}", 
                       extra={"output": {"suggestions_count": len(suggestions), "intent": result.get('intent')}})
            return response_dto
            
        except json.JSONDecodeError as e:
            logger.exception("Failed to parse LLM JSON response")
            raise interface.LLMServiceUnavailableException(f"Invalid JSON response from LLM: {str(e)}")
        except Exception as e:
            logger.exception("Failed to analyze text with LLM")
            # Fallback to rule-based
            logger.info("Falling back to rule-based analysis")
            return self._fallback_analyze_text(request)
    
    def generate_suggestions(self, request: interface.GenerateSuggestionsRequest) -> interface.GenerateSuggestionsResponse:
        logger.info(f"Generating suggestions with LLM: {request.prompt[:50]}...", 
                   extra={"input": request.model_dump()})
        
        if not self.client:
            logger.warning("LLM client not available, using fallback")
            return self._fallback_generate_suggestions(request)
        
        try:
            system_prompt = """You are a helpful assistant that provides actionable suggestions.
Generate concise, actionable suggestions based on the user's prompt.
Return a JSON object with:
{
  "suggestions": ["suggestion1", "suggestion2", ...],
  "confidence": 0.0-1.0
}"""
            
            user_prompt = request.prompt
            if request.context:
                user_prompt += f"\n\nContext: {json.dumps(request.context)}"
            
            # Call DeepSeek API
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.7,
                response_format={"type": "json_object"}
            )
            
            # Parse response
            content = response.choices[0].message.content
            result = json.loads(content)
            
            suggestions = result.get('suggestions', [])[:request.max_suggestions]
            confidence = result.get('confidence', 0.7)
            
            response_dto = interface.GenerateSuggestionsResponse(
                suggestions=suggestions,
                confidence=confidence
            )
            
            logger.info(f"Generated {len(suggestions)} suggestions", 
                       extra={"output": {"suggestions_count": len(suggestions)}})
            return response_dto
            
        except Exception as e:
            logger.exception("Failed to generate suggestions with LLM")
            # Fallback to rule-based
            logger.info("Falling back to rule-based suggestions")
            return self._fallback_generate_suggestions(request)
    
    def _fallback_analyze_text(self, request: interface.AnalyzeTextRequest) -> interface.AnalyzeTextResponse:
        """Fallback rule-based text analysis when LLM is unavailable."""
        logger.info("Using fallback rule-based analysis")
        
        text = request.text.strip()
        suggestions = []
        
        # Simple pattern matching
        intent = 'create_todo'
        if any(word in text.lower() for word in ['what', 'when', 'how', 'show', 'list']):
            intent = 'query'
        
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        title = lines[0] if lines else text[:100]
        description = '\n'.join(lines[1:]) if len(lines) > 1 else None
        
        priority = 'Medium'
        text_lower = text.lower()
        if any(word in text_lower for word in ['urgent', 'critical', 'asap', 'immediately']):
            priority = 'Critical'
        elif any(word in text_lower for word in ['important', 'high', 'soon']):
            priority = 'High'
        elif any(word in text_lower for word in ['low', 'later', 'someday']):
            priority = 'Low'
        
        suggested_deadline = None
        if 'today' in text_lower or 'now' in text_lower:
            from utils.date_utils.service import DateTimeService
            date_service = DateTimeService()
            now = date_service.now()
            suggested_deadline = now.timestamp_ms
        elif 'tomorrow' in text_lower:
            from utils.date_utils.service import DateTimeService
            date_service = DateTimeService()
            now = date_service.now()
            suggested_deadline = now.timestamp_ms + (24 * 60 * 60 * 1000)
        
        category = None
        category_keywords = {
            'work': ['work', 'job', 'office', 'meeting'],
            'personal': ['personal', 'home', 'family'],
            'shopping': ['buy', 'purchase', 'shopping', 'store'],
            'health': ['doctor', 'health', 'exercise', 'gym'],
        }
        for cat, keywords in category_keywords.items():
            if any(kw in text_lower for kw in keywords):
                category = cat
                break
        
        suggestion = interface.TodoSuggestion(
            title=title,
            description=description,
            priority=priority,
            category=category,
            labels=[],
            suggested_deadline=suggested_deadline,
            suggested_project_id=None,
            suggested_subtasks=[],
            confidence=0.5  # Lower confidence for fallback
        )
        suggestions.append(suggestion)
        
        return interface.AnalyzeTextResponse(
            suggestions=suggestions,
            detected_intent=intent,
            confidence=0.5,
            raw_response="Fallback rule-based analysis"
        )
    
    def _fallback_generate_suggestions(self, request: interface.GenerateSuggestionsRequest) -> interface.GenerateSuggestionsResponse:
        """Fallback rule-based suggestions when LLM is unavailable."""
        logger.info("Using fallback rule-based suggestions")
        
        suggestions = [
            "Consider breaking this into smaller tasks",
            "Set a deadline to stay on track",
            "Add relevant labels for better organization"
        ]
        
        return interface.GenerateSuggestionsResponse(
            suggestions=suggestions[:request.max_suggestions],
            confidence=0.5
        )
