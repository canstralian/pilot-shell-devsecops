```markdown
# pilot-shell-devsecops Development Patterns

> Auto-generated skill from repository analysis

## Overview
This skill teaches you the core development patterns and conventions used in the `pilot-shell-devsecops` TypeScript repository. You'll learn how to structure files, write imports/exports, follow commit message guidelines, and organize tests. This guide also suggests commands for common workflows to streamline your development process.

## Coding Conventions

### File Naming
- Use **kebab-case** for all filenames.
  - Example:  
    ```
    user-service.ts
    config-loader.test.ts
    ```

### Import Style
- Use **relative imports** for all modules.
  - Example:
    ```typescript
    import { getConfig } from './config-loader';
    import { User } from '../models/user';
    ```

### Export Style
- Use **named exports** for all modules.
  - Example:
    ```typescript
    // In user-service.ts
    export function createUser() { ... }
    export function deleteUser() { ... }
    ```

### Commit Messages
- Follow **conventional commit** style.
- Use the `chore` prefix for maintenance and non-feature commits.
- Example:
  ```
  chore: update dependencies and fix lint errors
  ```

## Workflows

### Code Contribution
**Trigger:** When adding new features, fixing bugs, or making changes  
**Command:** `/contribute`

1. Create a new branch using a descriptive name (e.g., `feature/add-auth-module`).
2. Write your code following the coding conventions above.
3. Add or update tests as needed.
4. Commit your changes using the conventional commit format.
5. Push your branch and open a pull request for review.

### Dependency Update
**Trigger:** When dependencies need to be updated  
**Command:** `/update-deps`

1. Run the package manager to update dependencies (e.g., `npm update`).
2. Test the codebase to ensure compatibility.
3. Commit changes with a message like:
   ```
   chore: update dependencies
   ```
4. Push and create a pull request if required.

## Testing Patterns

- Test files use the `*.test.*` naming pattern, e.g., `user-service.test.ts`.
- The testing framework is **unknown**, but tests should be colocated with code or in a `tests` directory.
- Example test file structure:
  ```
  src/
    user-service.ts
    user-service.test.ts
  ```
- Write tests for all exported functions and modules.

## Commands
| Command         | Purpose                                      |
|-----------------|----------------------------------------------|
| /contribute     | Start a new code contribution workflow       |
| /update-deps    | Update project dependencies                  |
```
