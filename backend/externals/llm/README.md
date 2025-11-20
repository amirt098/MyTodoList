# LLM Service - DeepSeek Integration

This module provides LLM (Large Language Model) integration using DeepSeek API, which is OpenAI-compatible.

## Configuration

### 1. Install Dependencies

```bash
pip install openai>=1.0.0
```

### 2. Get DeepSeek API Key

1. Sign up at [DeepSeek Platform](https://platform.deepseek.com/)
2. Get your API key from the dashboard

### 3. Configure API Key

You can set the API key in one of two ways:

#### Option A: Environment Variable (Recommended)

```bash
# Windows PowerShell
$env:DEEPSEEK_API_KEY="your-api-key-here"

# Windows CMD
set DEEPSEEK_API_KEY=your-api-key-here

# Linux/Mac
export DEEPSEEK_API_KEY=your-api-key-here
```

#### Option B: Django Settings

Edit `backend/runner/settings.py`:

```python
DEEPSEEK_API_KEY = 'your-api-key-here'
DEEPSEEK_API_BASE_URL = 'https://api.deepseek.com/v1'  # Default
DEEPSEEK_MODEL = 'deepseek-chat'  # Default model
```

### 4. Usage

The LLM service is automatically wired in the bootstrapper and used by `SmartTodoManagementService`.

**API Endpoints:**
- `POST /api/ai/analyze-text/` - Analyze free text and extract todos
- `POST /api/ai/create-smart-todo/` - Create todo from AI suggestion
- `POST /api/ai/auto-categorize/` - Auto-categorize a todo
- `POST /api/ai/suggest-subtasks/` - Suggest subtasks
- `POST /api/ai/suggest-next-action/` - Suggest next actions
- `POST /api/ai/query/` - Conversational queries

## Features

- **Text Analysis**: Extracts todo information from free text
- **Auto-categorization**: Automatically categorizes todos
- **Subtask Generation**: Suggests relevant subtasks
- **Next Action Suggestions**: Provides actionable suggestions
- **Conversational Interface**: Handles natural language queries
- **Fallback Mode**: Uses rule-based analysis if LLM is unavailable

## Fallback Behavior

If the DeepSeek API key is not configured or the service is unavailable, the system automatically falls back to rule-based analysis. This ensures the system continues to work even without LLM access.

## Example Request

```json
POST /api/ai/analyze-text/
{
  "text": "I need to finish the project report by tomorrow. It's urgent and needs to include the budget analysis.",
  "user_id": 1
}
```

## Example Response

```json
{
  "suggestions": [
    {
      "title": "Finish project report",
      "description": "Include budget analysis",
      "priority": "High",
      "category": "work",
      "labels": ["report", "budget"],
      "suggested_deadline": 1234567890000,
      "suggested_subtasks": ["Review budget data", "Write analysis section"],
      "confidence": 0.9
    }
  ],
  "detected_intent": "create_todo",
  "confidence": 0.9
}
```

