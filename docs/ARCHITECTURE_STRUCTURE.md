# Directory Structure & Module Organization

[← Back to Architecture Index](./ARCHITECTURE.md)

---

## Directory Structure

```
project_root/
├── runner/
│   ├── settings.py
│   ├── urls.py
│   └── bootstrap.py
│
├── presentation/
│   ├── rest/
│   │   ├── user_views.py
│   │   └── todo_views.py
│   ├── graphql/
│   │   └── schema.py
│   └── websocket/
│       └── handlers.py
│
├── usecase/
│   ├── user_management/
│   │   ├── service.py
│   │   └── interface/
│   │       ├── abstraction.py
│   │       ├── dataclasses.py
│   │       └── externals.py
│   ├── todo_management/
│   │   ├── service.py
│   │   └── interface/
│   │       ├── abstraction.py
│   │       ├── dataclasses.py
│   │       └── externals.py
│   └── common_usecase/
│       ├── validators/
│       ├── workflows/
│       └── policies/
│
├── repository/
│   ├── user/
│   │   ├── models.py
│   │   ├── service.py
│   │   └── interface/
│   │       ├── abstraction.py
│   │       ├── dataclasses.py
│   │       └── externals.py
│   └── todo/
│       ├── models.py
│       ├── service.py
│       └── interface/
│           ├── abstraction.py
│           ├── dataclasses.py
│           └── externals.py
│
├── externals/
│   ├── payment_gateway/
│   │   ├── service.py
│   │   └── interface/
│   │       ├── abstraction.py
│   │       ├── dataclasses.py
│   │       └── externals.py
│   ├── sms/
│   │   ├── service.py
│   │   └── interface/
│   │       ├── abstraction.py
│   │       ├── dataclasses.py
│   │       └── externals.py
│   └── email/
│       ├── service.py
│       └── interface/
│           ├── abstraction.py
│           ├── dataclasses.py
│           └── externals.py
│
├── clients/
│   ├── redis/
│   │   ├── service.py
│   │   └── interface/
│   │       ├── abstraction.py
│   │       ├── dataclasses.py
│   │       └── externals.py
│   └── kafka/
│       ├── service.py
│       └── interface/
│           ├── abstraction.py
│           ├── dataclasses.py
│           └── externals.py
│
├── infrastructure/
│   ├── cache/
│   ├── db/
│   ├── redis/
│   └── kafka/
│
├── lib/
│   ├── base_models.py          # Base Pydantic models
│   ├── validators.py           # Common Pydantic validators
│   ├── exceptions.py           # Base exceptions (BadRequestRootException, etc.)
│   └── base_interfaces.py     # Common interface patterns
│
├── utils/
│   ├── common/
│   │   ├── service.py
│   │   └── interface/
│   │       ├── abstraction.py
│   │       └── dataclasses.py
│   ├── constants/
│   └── date_utils/
│
└── docs/
    └── ARCHITECTURE.md
```

---

## Module Internal Structure

Each module follows a uniform folder pattern:

### Standard Module Structure

```
module_name/
├── service.py              # Main implementation
└── interface/
    ├── __init__.py         # Exports everything from submodules
    ├── abstraction.py      # Abstract class definitions (AbstractTodoRepository, etc.)
    ├── dataclasses.py      # Pydantic model-based DTOs
    ├── exceptions.py      # Module-specific exceptions (if any)
    └── externals.py        # External dependencies interface
```

**Interface `__init__.py` Structure:**
```python
# interface/__init__.py
from .abstraction import *
from .dataclasses import *
from .exceptions import *  # if exists
from .externals import *   # if exists
```

This allows importing everything directly from `interface`:
```python
from interface import AbstractTodoRepository, CreateTodoRequest, TodoDTO
```

For detailed code examples, see [ARCHITECTURE_EXAMPLES.md](./ARCHITECTURE_EXAMPLES.md).

---

[← Back to Architecture Index](./ARCHITECTURE.md) | [Next: Code Examples →](./ARCHITECTURE_EXAMPLES.md)

