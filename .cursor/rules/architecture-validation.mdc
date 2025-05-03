---
description:
globs:
alwaysApply: true
---
@file ../docs/architecture.mermaid

# Architecture Understanding & Validation

## Reading Architecture

**File:** `docs/architecture.mermaid`

**Required Parsing:**

1.  Load and parse the complete Mermaid diagram.
2.  Extract and understand:
    *   Module boundaries and relationships
    *   Data flow patterns
    *   System interfaces
    *   Component dependencies
3.  Validate any proposed code changes against these architectural constraints.
4.  Ensure new code maintains the defined separation of concerns.

## Error Handling

1.  **File Not Found:** If `docs/architecture.mermaid` is missing, STOP execution and notify the user.
2.  **Diagram Parse Failure:** If the Mermaid diagram cannot be parsed, REQUEST clarification or correction from the user.
3.  **Architectural Violation:** If a proposed change violates the defined architecture, WARN the user and suggest alternatives or require justification.
