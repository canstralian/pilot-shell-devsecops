# Testing and Coverage Guide

## Overview

This document outlines the testing strategy and coverage reporting configuration for the pilot-shell-devsecops project.

## Coverage Reporting

### Configuration

Coverage reporting has been instrumented using Bun's native `--coverage` flag with the following configuration in `console/package.json`:

```json
{
  "coverage": {
    "enabled": true,
    "thresholds": {
      "lines": 60,
      "functions": 60,
      "branches": 50,
      "statements": 60
    },
    "exclude": [
      "**/node_modules/**",
      "**/tests/**",
      "**/scripts/**",
      "**/*.test.ts",
      "**/*.spec.ts",
      "**/vite.config.ts",
      "**/tsconfig.json"
    ]
  }
}
```

### Running Tests with Coverage

```bash
# Run all tests with coverage (default)
cd console && bun test

# Run tests without coverage
cd console && bun run test:no-coverage

# Run specific test suites with coverage
cd console && bun run test:sqlite
cd console && bun run test:context
cd console && bun run test:worker

# Run tests with lcov reporter for CI
cd console && bun run test:ci
```

### Coverage Thresholds

The project maintains the following minimum coverage thresholds to prevent regression:

- **Lines**: 60%
- **Functions**: 60%
- **Branches**: 50%
- **Statements**: 60%

These thresholds are conservative starting points and should be progressively increased as more tests are added.

### Coverage Output

Coverage reports are generated in the `console/coverage/` directory (gitignored):

- **Text format**: Console output showing coverage percentages
- **LCOV format**: Machine-readable format for CI integration (via `--coverage-reporter=lcov`)

## Testing Strategy

### Priority Areas

Based on security-critical paths and DevSecOps principles, testing should be prioritized in the following order:

#### 1. Security-Critical Paths (Highest Priority)

**Authentication Middleware** (`console/src/services/server/middleware/auth.ts`)
- Test authentication token validation
- Test unauthorized access scenarios
- Test authentication bypass attempts
- Test session management

**Rate Limiting** (`console/src/services/server/middleware/rate-limit.ts`)
- Test rate limit enforcement
- Test rate limit threshold configuration
- Test rate limit reset behavior
- Test bypass prevention

**Test Location**: `console/tests/server/middleware/`

#### 2. Route Handler Tests

**Route Groups** (see `console/src/services/worker/http/routes/`):
- AuthRoutes
- SessionRoutes
- DataRoutes
- SettingsRoutes
- ExtensionRoutes
- LicenseRoutes
- SearchRoutes
- NotificationRoutes
- BackupRoutes
- ChangesRoutes
- MemoryRoutes
- MetricsRoutes
- PlanRoutes
- RetentionRoutes
- TeamRemoteRoutes
- UsageRoutes
- ViewerRoutes
- WorktreeRoutes
- LogsRoutes

**Testing Approach**:
- Create a test HTTP server fixture for consistent testing
- Add one test file per route group
- Test all HTTP methods (GET, POST, PUT, DELETE, PATCH)
- Test error handling and validation
- Test authorization checks
- Test input sanitization

**Test Location**: `console/tests/worker/` (following existing patterns)

#### 3. Pilot Module Tests

**Module Integration**:
- Add smoke tests to catch integration breakage
- Test basic module initialization
- Test cross-module communication
- Test error propagation

**Test Location**: `console/tests/integration/`

### Test Structure

Follow the existing test patterns:

```
console/tests/
├── cli/                    # CLI command tests
├── context/                # Context building tests
├── domain/                 # Business logic tests
├── hooks/                  # React hooks tests
├── infrastructure/         # Process management tests
├── integration/            # Cross-component tests
├── queue/                  # Queue processing tests
├── server/                 # Server middleware tests
├── shared/                 # Shared utility tests
├── sqlite/                 # Database tests
├── ui/                     # React component tests
├── unit/                   # Isolated unit tests
├── utils/                  # Utility function tests
└── worker/                 # Worker service tests
```

### Test Naming Convention

- Test files: `*.test.ts` or `*.spec.ts`
- Test descriptions: Clear, descriptive strings
- Test organization: Group related tests using `describe()` blocks

### Test Runner

The project uses **Bun's native test framework** which provides:
- Fast test execution
- Built-in coverage reporting
- TypeScript support out of the box
- Compatible API with Jest/Vitest

## CI/CD Integration

### GitHub Actions

Add the following to your CI workflow:

```yaml
- name: Install dependencies
  run: bun install
  working-directory: ./console

- name: Run tests with coverage
  run: bun run test:ci
  working-directory: ./console

- name: Upload coverage reports
  uses: codecov/codecov-action@v4
  with:
    files: ./console/coverage/lcov.info
    flags: unittests
    name: codecov-umbrella
```

### Local Development

Before committing:

```bash
cd console
bun run typecheck  # Type checking
bun test           # Run tests with coverage
```

## Best Practices

1. **Write tests first**: Follow TDD principles for new features
2. **Test edge cases**: Don't just test the happy path
3. **Mock external dependencies**: Use mocking for external services
4. **Keep tests focused**: Each test should verify one behavior
5. **Use descriptive names**: Test names should clearly describe what they test
6. **Avoid test interdependence**: Tests should be able to run in any order
7. **Test security scenarios**: Always test authentication, authorization, and input validation
8. **Maintain test data**: Keep test fixtures separate and reusable

## Security Testing Checklist

For security-critical code paths, ensure tests cover:

- [ ] Authentication validation
- [ ] Authorization checks
- [ ] Input sanitization (XSS, SQL injection, command injection)
- [ ] Rate limiting enforcement
- [ ] Session management
- [ ] Error handling (no sensitive data in error messages)
- [ ] CORS configuration
- [ ] CSRF protection (if applicable)
- [ ] Secure headers
- [ ] Data encryption/decryption

## Troubleshooting

### Coverage not being generated

Ensure you're using the `--coverage` flag:
```bash
bun test --coverage
```

### Tests failing due to encrypted files

If you encounter git-crypt encrypted files during testing, ensure you have:
1. The git-crypt key installed
2. Run `git-crypt unlock` in the repository

### Bun not found

Install Bun:
```bash
curl -fsSL https://bun.sh/install | bash
source ~/.bash_profile
```

## Contributing

When adding new features:

1. Add corresponding tests
2. Ensure coverage thresholds are met
3. Run the full test suite before submitting PR
4. Update this document if adding new test categories

## Resources

- [Bun Test Documentation](https://bun.sh/docs/cli/test)
- [DevSecOps Testing Principles](https://owasp.org/www-project-devsecops-guideline/)
- [OWASP Testing Guide](https://owasp.org/www-project-web-security-testing-guide/)
