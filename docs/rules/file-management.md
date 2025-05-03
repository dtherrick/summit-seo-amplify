---
description:
globs:
alwaysApply: true
---
@file ../docs/architecture.mermaid
@file ../docs/progress.md
@file ../docs/tech-stack.md
@file ../tasks/tasks.md

# File Management Rules

## Post-Change Actions

Required actions after any code changes:

1.  **Verify Architecture:** READ `docs/architecture.mermaid` to verify architectural compliance.
2.  **Update Progress:** UPDATE `docs/progress.md` with:
    *   Current progress
    *   Any new issues encountered
    *   Completed items
3.  **Validate Specs:** VALIDATE changes against `docs/tech-stack.md` specifications.
4.  **Verify Task:** VERIFY task progress against `tasks/tasks.md`.
