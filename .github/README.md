# GitHub Actions Workflows

This directory contains automated workflows for maintaining the Agentic AI Systems repository.

## 📋 Available Workflows

### 1. Update Agentic AI Systems Review
**File**: `workflows/update-review.yml`  
**Trigger**: Weekly (Monday 9 AM UTC), Manual, or on workflow changes  
**Purpose**: Automatically check for updates to the review content

**What it does:**
- 🔍 Searches arXiv for relevant new papers (15 search queries)
- 🤖 Uses GPT-4 to analyze paper relevance
- 📦 Checks PyPI for framework version updates
- 🔗 Verifies links in README and paper
- 💡 Generates AI-powered content suggestions
- 📝 Creates/updates GitHub issue with comprehensive report
- 📊 Uploads artifacts (update_report.md, update_suggestions.json)

**Requirements:**
- `OPENAI_API_KEY` secret must be set
- Workflow permissions: read/write for contents, issues, PRs

**Estimated runtime**: 5-10 minutes  
**Cost**: ~$0.03 per run in OpenAI API credits

**Manual trigger:**
```bash
# Via GitHub UI:
Actions → Update Agentic AI Systems Review → Run workflow

# Via GitHub CLI:
gh workflow run update-review.yml
```

### 2. Test Update Agent
**File**: `workflows/test-update-agent.yml`  
**Trigger**: Pull requests to update agent files, Manual  
**Purpose**: Validate update agent code quality and functionality

**What it does:**
- ✅ Checks Python imports work correctly
- ✅ Runs flake8 linting for syntax errors
- ✅ Checks code formatting with black
- ✅ Ensures no breaking changes

**Requirements:**
- No secrets required (runs without API key)
- Workflow permissions: read only

**Estimated runtime**: 1-2 minutes  
**Cost**: FREE (GitHub Actions)

## 🔧 Configuration

### Secrets Required

Add in **Settings → Secrets and variables → Actions**:

| Secret Name | Description | Required By |
|------------|-------------|-------------|
| `OPENAI_API_KEY` | OpenAI API key for GPT-4 analysis | update-review.yml |

`GITHUB_TOKEN` is automatically provided by GitHub Actions.

### Permissions Required

Set in **Settings → Actions → General → Workflow permissions**:

- ✅ Read and write permissions
- ✅ Allow GitHub Actions to create and approve pull requests

This allows workflows to:
- Create and update issues
- Upload artifacts
- (Optional) Create pull requests

## 📅 Schedule

### Current Schedule

| Workflow | Schedule | Cron Expression |
|----------|----------|----------------|
| Update Review | Every Monday 9 AM UTC | `0 9 * * 1` |
| Test Agent | On PR only | N/A |

### Customizing Schedule

Edit the `cron` expression in `update-review.yml`:

```yaml
on:
  schedule:
    - cron: '0 9 * * 1'  # minute hour day month weekday
```

**Common schedules:**
- Daily: `'0 9 * * *'`
- Twice weekly: `'0 9 * * 1,4'` (Mon & Thu)
- Bi-weekly: `'0 9 1,15 * *'` (1st & 15th)
- Monthly: `'0 9 1 * *'` (1st of month)

**Cron format:**
```
┌───────────── minute (0 - 59)
│ ┌───────────── hour (0 - 23)
│ │ ┌───────────── day of month (1 - 31)
│ │ │ ┌───────────── month (1 - 12)
│ │ │ │ ┌───────────── day of week (0 - 6) (Sunday to Saturday)
│ │ │ │ │
* * * * *
```

[Cron expression generator](https://crontab.guru/)

## 📊 Outputs

### Artifacts

Each workflow run produces downloadable artifacts:

**update-review.yml**:
- `update_report.md` - Human-readable markdown report
- `update_suggestions.json` - Machine-readable JSON data
- Retained for 30 days

**Access artifacts:**
1. Go to Actions → Select workflow run
2. Scroll to "Artifacts" section
3. Click to download

### Issues

**update-review.yml** creates/updates an issue:
- **Title**: `🤖 Automated Review Update - YYYY-MM-DD`
- **Labels**: `automated-update`, `enhancement`
- **Content**: Full update report with findings
- **Location**: Issues tab

If an existing issue with `automated-update` label exists (and is open), it will be updated instead of creating a new one.

## 🔍 Monitoring

### View Workflow Status

1. Go to **Actions** tab
2. Select workflow from sidebar
3. View run history with status

**Status indicators:**
- ✅ Green: Success
- ❌ Red: Failed
- 🟡 Yellow: In progress
- ⚪ Gray: Queued

### Debugging Failed Runs

1. Click on failed run
2. Click on failed job
3. Expand failed step
4. Review error logs

**Common errors:**
- `OPENAI_API_KEY not set` → Check Secrets
- `Permission denied` → Check workflow permissions
- `Rate limit exceeded` → Wait or adjust rate limits in code
- `API error` → Check OpenAI status

### Usage Tracking

**GitHub Actions usage:**
- Settings → Billing → Plans and usage
- Free tier: 2,000 minutes/month
- These workflows: ~20 minutes/month

**OpenAI API usage:**
- [OpenAI Usage Dashboard](https://platform.openai.com/usage)
- Expected: ~$0.12/week, ~$0.50/month

## 🛡️ Security

### Best Practices

✅ **DO:**
- Store API keys in Secrets
- Use minimum required permissions
- Review workflow changes in PRs
- Monitor API usage regularly
- Set OpenAI spending limits

❌ **DON'T:**
- Commit API keys to repository
- Grant excessive permissions
- Ignore security warnings
- Share secrets between repos

### Secret Security

Secrets are:
- Encrypted at rest
- Redacted in logs
- Only accessible during workflow execution
- Not exposed to forked repositories

### Third-party Actions

We only use official GitHub actions:
- `actions/checkout@v4`
- `actions/setup-python@v5`
- `actions/upload-artifact@v4`
- `actions/github-script@v7`

All pinned to specific versions (v4, v5, v7).

## 🧪 Testing

### Local Testing

Test workflows locally without GitHub Actions:

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Set environment variables
export OPENAI_API_KEY="your-key"
export GITHUB_TOKEN="your-github-token"
export GITHUB_REPOSITORY="owner/repo"

# 3. Run update agent
python scripts/update_agent.py

# 4. Check output
cat update_report.md
```

### Test Mode

To test without API costs, modify `scripts/update_agent.py`:

```python
# Reduce search scope
self.search_prompts[:2]  # Only 2 searches

# Use cheaper model
model="gpt-3.5-turbo"  # Instead of gpt-4o

# Skip API calls
if os.getenv('TEST_MODE'):
    return []  # Return empty results
```

## 📈 Optimization

### Reduce Costs

**Option 1**: Less frequent updates
```yaml
schedule:
  - cron: '0 9 1,15 * *'  # Bi-weekly instead of weekly
```

**Option 2**: Smaller search scope
```python
# In update_agent.py
self.search_prompts[:5]  # Only 5 searches instead of 15
max_results=2  # 2 papers per search instead of 3
)[:10]  # Top 10 instead of 15
```

**Option 3**: Use GPT-3.5 Turbo
```python
# In update_agent.py
model="gpt-3.5-turbo"  # Cheaper than gpt-4o-mini
```

### Speed Up Execution

**Option 1**: Parallel searches (already implemented)
- Uses `asyncio` for concurrent arXiv searches
- Up to 10 searches run simultaneously

**Option 2**: Skip link verification
```python
# Comment out in run() method
# self.findings['broken_links'] = self.verify_links()
```

**Option 3**: Cache results
- Store findings in repository
- Only check for new items since last run

## 🔄 Continuous Improvement

### Adding New Checks

1. Edit `scripts/update_agent.py`
2. Add new method to `UpdateAgent` class
3. Call from `run()` method
4. Update `generate_report()` to include findings
5. Test locally
6. Submit PR

Example:
```python
async def check_new_feature(self):
    """Check for something new."""
    results = []
    # Your implementation
    return results

async def run(self):
    # ... existing checks ...
    self.findings['new_feature'] = await self.check_new_feature()
```

### Modifying Search Prompts

Edit `arxiv-paper/SEARCH-PROMPTS-FOR-IMPROVEMENT.md`:
- Add new `**Prompt**:` lines
- Agent automatically picks them up
- No code changes needed

### Custom Notifications

Add notification steps to workflow:

**Slack:**
```yaml
- name: Notify Slack
  uses: slackapi/slack-github-action@v1
  with:
    webhook-url: ${{ secrets.SLACK_WEBHOOK }}
    payload: |
      {
        "text": "Update report available!"
      }
```

**Discord:**
```yaml
- name: Notify Discord
  uses: Ilshidur/action-discord@0.3.2
  with:
    webhook: ${{ secrets.DISCORD_WEBHOOK }}
    message: "New updates found!"
```

**Email** is built-in (enable in Settings → Notifications)

## 📚 Related Documentation

- [QUICK-START.md](../QUICK-START.md) - 2-minute setup guide
- [AUTOMATION-GUIDE.md](../AUTOMATION-GUIDE.md) - Complete automation guide
- [scripts/README.md](../scripts/README.md) - Update agent documentation
- [SECURITY.md](../SECURITY.md) - Security best practices

## 🆘 Support

### Troubleshooting

1. Check workflow logs (Actions tab)
2. Review [AUTOMATION-GUIDE.md](../AUTOMATION-GUIDE.md) troubleshooting section
3. Search existing [Issues](https://github.com/memari-majid/Agentic-AI-Systems/issues)
4. Open new issue with:
   - Workflow run link
   - Error logs
   - Steps to reproduce

### Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [OpenAI API Documentation](https://platform.openai.com/docs)
- [arXiv API Documentation](https://arxiv.org/help/api)

---

**Last Updated**: 2025-11-15  
**Workflows Version**: 1.0.0  
**Maintainer**: Majid Memari (mmemari@uvu.edu)

