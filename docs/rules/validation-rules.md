---
description:
globs: **/*.ts
alwaysApply: false
---
# Error Prevention

## Validation Rules

During implementation, ensure the following:

1.  **Type Consistency:** Verify that variables, function parameters, and return types are consistent and strictly typed. Avoid implicit `any`.
2.  **Null/Undefined Checks:** Check for potential `null` or `undefined` values, especially when accessing object properties or array elements retrieved from external sources or complex logic.
3.  **Business Logic Validation:** Validate inputs and state against defined business rules before performing operations.
4.  **Error Handling:** Implement appropriate error handling (e.g., try-catch blocks, specific error types) for operations that might fail (API calls, file I/O, complex calculations).
