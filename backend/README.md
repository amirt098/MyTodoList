# My Todo List - Backend

Django-based backend for the My Todo List application, built using Clean Architecture principles.

## Architecture

This backend follows a **Modular Clean Architecture** with the following layers:

- **Presentation Layer** (`presentation/`) - REST, GraphQL, WebSocket interfaces
- **UseCase Layer** (`usecase/`) - Application services and business logic
- **Repository Layer** (`repository/`) - Data access and Django models
- **Externals Layer** (`externals/`) - External service integrations
- **Clients Layer** (`clients/`) - External API clients
- **Infrastructure Layer** (`infrastructure/`) - Database, cache, messaging
- **Utils Layer** (`utils/`) - Pure functions and helpers
- **Lib Layer** (`lib/`) - Base models, exceptions, validators

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run migrations:
```bash
python manage.py migrate
```

3. Run development server:
```bash
python manage.py runserver
```

## Project Structure

```
backend/
├── runner/              # Django settings, URLs, bootstrapper
├── presentation/        # REST, GraphQL, WebSocket
├── usecase/            # Application services
├── repository/          # Data access layer
├── externals/           # External services
├── clients/             # API clients
├── infrastructure/      # Infrastructure components
├── utils/               # Utilities
└── lib/                 # Foundation components
```

## Development Phases

See `../docs/PHASES.md` for detailed development phases.

**Current Phase:** Phase 0 - Foundation & Infrastructure Setup

## Code Standards

- Follow import order: Standard library → Third-party → Internal
- All DTOs extend from `lib.base_models` (BaseRequest, BaseResponse, BaseFilter)
- All exceptions extend from `lib.exceptions`
- Manual logging in all service methods (input at start, output at end)
- Docstrings in abstract classes/interfaces, not implementations
- No cross-module ForeignKey relationships (use IDs/UUIDs instead)

See `../docs/ARCHITECTURE_CODE_STANDARDS.md` for complete coding standards.

