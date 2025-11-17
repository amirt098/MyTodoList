# My Todo List - Requirements & Definitions Document

## 📍 Introduction

My Todo List is a personal and project task management tool with two main operational modes:

1. **Manual Mode** – Simple, manual todo creation and management without AI assistance
2. **AI/LLM Assisted Mode** – AI-powered assistance for todo creation, categorization, subtask suggestions, prioritization, and more

The system will be accessible through:
- Web interface
- Telegram
- Bale (Iranian messaging app)
- Eitaa (Iranian messaging app)
- Email
- Other channels

This document covers all concepts, requirements, and main Use Cases of the system comprehensively.

---

## 🧩 Part 1 — Core System Concepts

### 1. Todo

A task that can be performed, containing:

#### Basic Information
- **Title** - Short description of the task
- **Description** - Full detailed description
- **Deadline** - Due date and time
- **Priority** - One of: `Low`, `Medium`, `High`, `Critical`
- **Status** - One of: `ToDo`, `In Progress`, `Waiting`, `Blocked`, `Done`, `Cancelled`
- **Category** - Classification (Work, Home, University, Personal, etc.)
- **Labels/Tags** - Multiple free-form labels/hashtags
- **Related Project** - Optional project association

#### Advanced Features
- **Subtasks** (Optional) - Simple subtasks with:
  - Title
  - Status
- **Flow/Dependencies**:
  - Next Todo
  - Previous Todo
  - Execution order or precedence/dependency chain
- **Attachments** - Files (PDF, images, text, links)
- **Auto-Repeat** - Recurring tasks (Daily, Weekly, Monthly)
- **Reminders** - Notifications via:
  - Email
  - SMS
  - Messaging apps (Telegram, Bale, Eitaa)

### 2. Project

A collection of todos with the following features:

#### Project Properties
- **Privacy** - Private or Shared
- **Members** - Ability to add team members
- **Roles**:
  - `Owner` - Full control
  - `Admin` - Administrative privileges
  - `Member` - Standard access

#### Project Dashboard
- Total todo count
- Progress tracking
- Overdue todos
- Dedicated Kanban board per project

### 3. Kanban Board

Visual board for managing todos as cards.

#### Default Columns
- `ToDo`
- `In Progress`
- `Done`

#### Customization
- Ability to create custom columns
- Cards represent todos

#### Card Information Display
- Title
- Labels
- Priority
- Deadline
- Progress percentage (based on subtasks)

#### Features
- **Drag & Drop** - Move cards between columns
- **Filter/Search** by:
  - Category
  - Project
  - Deadline
  - Priority
  - Label
  - Status

### 4. Manual Mode (Simple Path)

Simple, manual todo management:
- Manual todo creation
- Simple editing
- Optional simple subtasks
- Sorting, categorization, labeling
- **No AI assistance**

### 5. AI-Assisted Mode (Intelligent Path)

AI/LLM assistance in the following areas:

#### a) Todo Creation from Free Text
User enters multi-line text → LLM analyzes → Suggests:
- Title
- Description
- Appropriate labels and categories
- Suggested project
- Suggested subtasks
- Appropriate deadline
- Flow/dependencies
- Priority

User can:
- ✅ Accept
- ✏️ Edit
- ❌ Reject

suggestions.

#### b) Intelligent Auto-Categorization
System automatically detects based on todo text:
- Which project it belongs to
- Appropriate category/label
- Priority and deadline

#### c) Project Analysis and New Todo Suggestions
LLM reads project status and past todos, then suggests:
- New todos
- Required subtasks
- Next steps
- Dependencies

### 6. Reminder System

Notification delivery through:
- Email
- SMS
- Telegram, Bale, Eitaa

#### Smart Reminders
- Deadline proximity alerts
- Overdue task notifications
- Suggestions for improving schedule

### 7. User Account Management

- Registration / Login
- Password recovery
- User profile
- Notification settings
- Messaging app connections

---

## 🗂 Part 2 — General System Requirements

### 1. Basic Requirements

- ✅ Secure registration and login
- ✅ User management
- ✅ Todo CRUD operations
- ✅ Project management
- ✅ Notification delivery
- ✅ Data storage and security
- ✅ API for messaging platforms

### 2. Advanced Requirements

- ✅ Kanban board functionality
- ✅ Todo flow/dependencies
- ✅ Optional subtasks
- ✅ Comprehensive filtering across all sections
- ✅ Fast search
- ✅ Global and project-specific dashboards

### 3. AI Requirements

- ✅ Free text analysis
- ✅ Project detection
- ✅ Label detection
- ✅ Priority and deadline detection
- ✅ Subtask suggestions
- ✅ Next action suggestions
- ✅ Conversational interaction:
  - "What should I do today?"

---

## 🚦 Part 3 — Use Cases

### Use Case 1: Registration and Login

**Actor:** Any individual

**Scenario:**
1. User registers
2. Email/phone verification
3. User logs in

**Preconditions:**
- User has valid email/phone

**Postconditions:**
- User account created
- User authenticated

---

### Use Case 2: Create Todo (Manual Mode)

**Actor:** Authenticated User

**Main Flow:**
1. User clicks "Create Todo"
2. User enters:
   - Title
   - Description
   - Category
   - Project (optional)
   - Labels
   - Deadline
   - Priority
3. User optionally adds subtasks
4. User saves
5. Todo appears in list/kanban

**Alternative Flows:**
- User cancels creation
- User saves as draft

**Postconditions:**
- New todo created
- Todo visible in user's todo list

---

### Use Case 3: Create Smart Todo from Free Text

**Actor:** Authenticated User

**Main Flow:**
1. User enters multi-line free text
2. System sends text to LLM for processing
3. LLM returns suggestions:
   - Todo structure
   - Subtasks
   - Category
   - Project
   - Deadline
   - Priority
4. System displays suggestions to user
5. User reviews and can:
   - Edit suggestions
   - Accept
   - Reject
6. User confirms
7. Todos are saved

**Alternative Flows:**
- LLM processing fails → Fallback to manual mode
- User rejects all suggestions → Manual creation

**Postconditions:**
- New todos created based on AI suggestions
- Todos visible in appropriate projects/categories

---

### Use Case 4: Project Management

**Actor:** Authenticated User

**Main Flow:**
1. User creates new project
2. User sets project properties (name, privacy, etc.)
3. User adds members (if shared)
4. User assigns roles to members
5. User assigns todos to project
6. User views project progress
7. User manages project kanban board

**Alternative Flows:**
- User deletes project
- User removes members
- User changes member roles

**Postconditions:**
- Project created/updated
- Members have appropriate access
- Todos associated with project

---

### Use Case 5: Kanban Board Management

**Actor:** Authenticated User

**Main Flow:**
1. User opens project kanban board
2. System displays todos as cards in columns
3. User drags and drops cards between columns
4. User creates new card (todo) directly on board
5. User filters cards by various criteria
6. User edits or deletes cards

**Alternative Flows:**
- User creates custom column
- User reorders columns
- User hides/shows columns

**Postconditions:**
- Todo status updated (if moved)
- Board state saved

---

### Use Case 6: View All My Todos

**Actor:** Authenticated User

**Main Flow:**
1. User navigates to "All My Todos"
2. System displays all personal and project todos
3. User applies filters:
   - By project
   - By deadline
   - By priority
   - By label
   - By status
4. User sorts by:
   - Newest first
   - Nearest deadline
   - Most important
5. User views detailed todo information

**Alternative Flows:**
- User exports todos
- User bulk edits todos

**Postconditions:**
- User sees filtered/sorted todo list

---

### Use Case 7: Reminder System

**Actor:** System / Authenticated User

**Main Flow:**
1. User creates reminder for todo
2. User selects delivery channel(s):
   - Email
   - SMS
   - Telegram
   - Bale
   - Eitaa
3. System schedules reminder
4. At reminder time, system sends notification
5. User receives notification

**Alternative Flows:**
- Smart reminder triggers (deadline proximity, overdue)
- User dismisses reminder
- User snoozes reminder

**Postconditions:**
- Reminder sent to user
- Reminder marked as delivered

---

### Use Case 8: Todo Flow / Dependencies

**Actor:** Authenticated User

**Main Flow:**
1. User creates todo
2. User defines dependencies:
   - This todo must be done before: [Todo X]
   - This todo must be done after: [Todo Y]
3. System displays:
   - Previous todo(s)
   - Next todo(s)
4. User views dependency chain
5. System enforces dependency rules (e.g., can't mark done if previous not done)

**Alternative Flows:**
- User removes dependency
- User reorders dependencies

**Postconditions:**
- Dependencies established
- Flow visible in todo view

---

## 🎯 Part 4 — Feature Summary

### ✅ Core Features

- [x] Manual Mode
- [x] AI-Assisted Mode
- [x] Manual todo creation
- [x] Smart todo creation from free text
- [x] Private/shared projects
- [x] Kanban board per project
- [x] Optional subtasks
- [x] Labels and categorization
- [x] Priority and deadline
- [x] Dependencies (Flow) and previous/next lists
- [x] Reminders via messaging platforms
- [x] Unified "All My Todos" view
- [x] Advanced filtering
- [x] LLM interaction for suggestions
- [x] Progress dashboard

---

## 📋 Part 5 — Data Models

### Todo Model

```python
Todo:
  - id: UUID
  - title: String
  - description: Text
  - deadline: DateTime (nullable)
  - priority: Enum (Low, Medium, High, Critical)
  - status: Enum (ToDo, In Progress, Waiting, Blocked, Done, Cancelled)
  - category: String
  - labels: Array[String]
  - project_id: ForeignKey (nullable)
  - user_id: ForeignKey
  - previous_todo_id: ForeignKey (nullable)
  - next_todo_id: ForeignKey (nullable)
  - order: Integer
  - created_at: DateTime
  - updated_at: DateTime
  - completed_at: DateTime (nullable)
  - auto_repeat: Enum (None, Daily, Weekly, Monthly)
  - attachments: Array[File]
```

### Subtask Model

```python
Subtask:
  - id: UUID
  - todo_id: ForeignKey
  - title: String
  - status: Enum (ToDo, Done)
  - order: Integer
  - created_at: DateTime
```

### Project Model

```python
Project:
  - id: UUID
  - name: String
  - description: Text
  - is_private: Boolean
  - owner_id: ForeignKey
  - created_at: DateTime
  - updated_at: DateTime
```

### ProjectMember Model

```python
ProjectMember:
  - id: UUID
  - project_id: ForeignKey
  - user_id: ForeignKey
  - role: Enum (Owner, Admin, Member)
  - joined_at: DateTime
```

### Reminder Model

```python
Reminder:
  - id: UUID
  - todo_id: ForeignKey
  - reminder_time: DateTime
  - channels: Array[Enum] (Email, SMS, Telegram, Bale, Eitaa)
  - sent: Boolean
  - sent_at: DateTime (nullable)
```

---

## 🔌 Part 6 — Integration Requirements

### Messaging Platform APIs

- **Telegram Bot API** - For Telegram integration
- **Bale API** - For Bale integration
- **Eitaa API** - For Eitaa integration
- **SMS Gateway** - For SMS notifications
- **Email Service** - For email notifications

### AI/LLM Integration

- **LLM API** - For text analysis and suggestions
- **Prompt Engineering** - Structured prompts for:
  - Todo extraction from text
  - Categorization
  - Priority detection
  - Deadline suggestion
  - Subtask generation
  - Next action prediction

---

## 🔒 Part 7 — Security & Privacy Requirements

- User authentication and authorization
- Project access control (private/shared)
- Role-based permissions
- Data encryption at rest and in transit
- Secure API endpoints
- Input validation and sanitization
- Rate limiting for AI features
- GDPR/privacy compliance considerations

---

## 📊 Part 8 — Performance Requirements

- Fast todo list loading (< 2 seconds)
- Real-time kanban updates
- Efficient filtering and search
- AI response time (< 5 seconds for suggestions)
- Scalable to handle multiple concurrent users
- Optimized database queries

---

## 🧪 Part 9 — Testing Requirements

- Unit tests for all services
- Integration tests for API endpoints
- End-to-end tests for critical flows
- AI suggestion accuracy testing
- Performance testing
- Security testing

---

## 📱 Part 10 — User Interface Requirements

### Web Interface
- Responsive design (mobile, tablet, desktop)
- Intuitive navigation
- Drag-and-drop kanban
- Real-time updates
- Dark/light theme support

### Messaging Platform Interfaces
- Simple command-based interface
- Quick todo creation
- Status updates
- Reminder notifications

---

## Document Version

- **Version**: 1.0
- **Last Updated**: 2024
- **Status**: Initial Requirements

---

## Appendix: Glossary

- **Todo**: A task or item to be completed
- **Subtask**: A smaller task within a todo
- **Project**: A collection of related todos
- **Kanban Board**: Visual board with columns and cards for task management
- **Flow/Dependencies**: Relationship between todos indicating order of execution
- **Reminder**: Notification sent at a specific time about a todo
- **LLM**: Large Language Model (AI system)
- **Manual Mode**: Simple, non-AI-assisted todo management
- **AI-Assisted Mode**: AI-powered todo creation and management

