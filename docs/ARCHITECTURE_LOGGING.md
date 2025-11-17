# Logging Implementation

[← Back to Architecture Index](./ARCHITECTURE.md)

---

## Manual Logging (Required)

All service methods must manually log input at the start and output at the end. No decorators are used.

```python
import logging

logger = logging.getLogger(__name__)

def some_method(self, request: SomeRequest) -> SomeResponse:
    # Log input at start
    logger.info(
        f"Starting {self.__class__.__name__}.some_method",
        extra={"input": request.model_dump()}
    )
    
    # ... method logic ...
    
    # Log output at end
    logger.info(
        f"Completed {self.__class__.__name__}.some_method",
        extra={"output": response.model_dump()}
    )
    return response
```

## Logging Best Practices

1. **Log input at method start**: Include request/model_dump() in extra field
2. **Log output at method end**: Include response/model_dump() in extra field
3. **Log errors**: Use logger.error() with exc_info=True for exceptions
4. **Use structured logging**: Put data in `extra` dict for better parsing
5. **Limit sensitive data**: Don't log passwords, tokens, or PII in production

---

[← Back to Architecture Index](./ARCHITECTURE.md) | [Next: Lib Directory →](./ARCHITECTURE_LIB.md)

