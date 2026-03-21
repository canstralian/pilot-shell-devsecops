# GitHub Actions Setup Guide

## Issue: Claude Code Action Authentication Failure

### Problem Statement

The GitHub Actions workflow at `.github/workflows/claude.yml` is failing with the following error:

```
##[error]Action failed with error: Environment variable validation failed:
  - Either ANTHROPIC_API_KEY or CLAUDE_CODE_OAUTH_TOKEN is required when using direct Anthropic API.
```

**Affected Workflow Run**: [Job #68031779100](https://github.com/canstralian/pilot-shell-devsecops/actions/runs/23385521287/job/68031779100)

### Root Cause

The workflow is configured to use the `anthropics/claude-code-action@v1` action, which requires authentication via either:
1. `ANTHROPIC_API_KEY` (direct API key)
2. `CLAUDE_CODE_OAUTH_TOKEN` (OAuth token)

The workflow references `${{ secrets.CLAUDE_CODE_OAUTH_TOKEN }}` (lines 56, 88, and 108 in `.github/workflows/claude.yml`), but this secret is not configured in the repository.

### Impact

The following GitHub Actions jobs are currently non-functional:
- **claude-mention**: Responds to `@claude` mentions in issues and pull requests
- **claude-review**: Performs automatic code reviews on pull requests

## Fix Options

### Option 1: Add CLAUDE_CODE_OAUTH_TOKEN Secret (Recommended)

This is the recommended approach for production use as it provides better security and rate limiting.

**Steps:**

1. **Obtain a Claude Code OAuth Token**:
   - Visit the [Anthropic Console](https://console.anthropic.com/)
   - Navigate to API Keys or OAuth Applications
   - Generate a new OAuth token for GitHub Actions
   - Copy the token (you won't be able to see it again)

2. **Add the Secret to GitHub**:
   - Navigate to: `https://github.com/canstralian/pilot-shell-devsecops/settings/secrets/actions`
   - Click "New repository secret"
   - Name: `CLAUDE_CODE_OAUTH_TOKEN`
   - Value: Paste the OAuth token from step 1
   - Click "Add secret"

3. **Verify the Fix**:
   - Navigate to the Actions tab
   - Re-run the failed workflow
   - Verify that the job completes successfully

### Option 2: Add ANTHROPIC_API_KEY Secret (Alternative)

If you prefer to use a direct API key instead of OAuth:

**Steps:**

1. **Obtain an Anthropic API Key**:
   - Visit the [Anthropic Console](https://console.anthropic.com/)
   - Navigate to API Keys
   - Generate a new API key
   - Copy the API key

2. **Add the Secret to GitHub**:
   - Navigate to: `https://github.com/canstralian/pilot-shell-devsecops/settings/secrets/actions`
   - Click "New repository secret"
   - Name: `ANTHROPIC_API_KEY`
   - Value: Paste the API key from step 1
   - Click "Add secret"

3. **Update the Workflow** (if using ANTHROPIC_API_KEY):
   - Edit `.github/workflows/claude.yml`
   - Replace all instances of:
     ```yaml
     claude_code_oauth_token: ${{ secrets.CLAUDE_CODE_OAUTH_TOKEN }}
     ```
   - With:
     ```yaml
     anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
     ```
   - Commit and push the changes

4. **Verify the Fix**:
   - Navigate to the Actions tab
   - Re-run the failed workflow
   - Verify that the job completes successfully

### Option 3: Use OIDC Authentication (Advanced)

The workflow already has `id-token: write` permissions configured, which allows for OIDC authentication. However, this requires additional setup with Anthropic and may not be available for all accounts.

If you want to use OIDC:
- Consult the [Claude Code Action documentation](https://github.com/anthropics/claude-code-action) for OIDC setup
- No secrets are required with OIDC, but you need to configure trust relationships

## Workflow Configuration Reference

The current workflow configuration expects authentication at three locations:

1. **Line 56** (claude-mention job - on-demand assistance):
   ```yaml
   claude_code_oauth_token: ${{ secrets.CLAUDE_CODE_OAUTH_TOKEN }}
   ```

2. **Line 88** (claude-review job - full review):
   ```yaml
   claude_code_oauth_token: ${{ secrets.CLAUDE_CODE_OAUTH_TOKEN }}
   ```

3. **Line 108** (claude-review job - incremental review):
   ```yaml
   claude_code_oauth_token: ${{ secrets.CLAUDE_CODE_OAUTH_TOKEN }}
   ```

## Security Considerations

### Best Practices

1. **Secret Rotation**: Regularly rotate your API keys and OAuth tokens
2. **Least Privilege**: Ensure the token has only the permissions needed for code review
3. **Audit Logs**: Monitor the Anthropic Console for unexpected API usage
4. **Secret Scanning**: GitHub's secret scanning may detect leaked tokens

### Current Permissions

The workflow jobs have the following permissions:

**claude-mention job**:
```yaml
permissions:
  contents: read
  pull-requests: read
  issues: read
  id-token: write
  actions: read
```

**claude-review job**:
```yaml
permissions:
  contents: read
  pull-requests: write
  issues: write
  id-token: write
```

These permissions are appropriate for the Claude Code Action's functionality:
- **Read** access to code and issues for context
- **Write** access to pull requests and issues for posting reviews
- **id-token: write** for OIDC authentication (if used)

## Verification Steps

After adding the secret, verify the fix:

1. **Check Secret Configuration**:
   - Navigate to repository settings → Secrets and variables → Actions
   - Verify that `CLAUDE_CODE_OAUTH_TOKEN` or `ANTHROPIC_API_KEY` is listed

2. **Test the Workflow**:
   - Option A: Create a test pull request and mention `@claude` in a comment
   - Option B: Re-run the failed workflow from the Actions tab
   - Option C: Use workflow_dispatch to manually trigger a review

3. **Monitor the Job**:
   - Navigate to the Actions tab
   - Click on the running workflow
   - Verify that the "Run Claude Code" step completes without authentication errors

4. **Confirm Functionality**:
   - For `@claude` mentions: Verify that Claude responds in the issue/PR comment
   - For automatic reviews: Verify that Claude posts a review comment on new PRs

## Troubleshooting

### Issue: "Invalid token" error

**Symptoms**: The workflow runs but fails with "Invalid token" or "Unauthorized"

**Solutions**:
1. Verify the token is correctly copied (no trailing spaces)
2. Ensure the token hasn't expired
3. Check that the token has the necessary permissions
4. Regenerate the token in the Anthropic Console

### Issue: "Rate limit exceeded"

**Symptoms**: The workflow fails with rate limit errors

**Solutions**:
1. Switch from API key to OAuth token (better rate limits)
2. Contact Anthropic support for rate limit increases
3. Consider implementing workflow throttling

### Issue: Workflow doesn't trigger

**Symptoms**: No workflow runs appear when expected

**Solutions**:
1. Verify the workflow file is in `.github/workflows/`
2. Check that the trigger conditions match your actions
3. Ensure the workflow is enabled in repository settings
4. Review branch protection rules that may block the action

## Related Documentation

- [Claude Code Action Documentation](https://github.com/anthropics/claude-code-action)
- [Anthropic API Documentation](https://docs.anthropic.com/)
- [GitHub Actions Secrets](https://docs.github.com/en/actions/security-guides/encrypted-secrets)
- [GitHub OIDC with Third-Party Cloud Providers](https://docs.github.com/en/actions/deployment/security-hardening-your-deployments/about-security-hardening-with-openid-connect)

## Next Steps

Once authentication is configured:

1. **Test the Setup**: Create a test PR and mention `@claude`
2. **Monitor Usage**: Track API usage in the Anthropic Console
3. **Document for Team**: Share this guide with repository maintainers
4. **Plan Rotation**: Schedule regular token rotation (e.g., quarterly)

## Support

For issues with:
- **Claude Code Action**: [Open an issue](https://github.com/anthropics/claude-code-action/issues)
- **Anthropic API**: Contact [Anthropic Support](https://support.anthropic.com/)
- **This Fork**: Open an issue in this repository
