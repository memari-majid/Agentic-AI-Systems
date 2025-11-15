# GitHub Actions Workflows

This directory contains automated workflows for maintaining the Agentic AI Systems repository.

## 📋 Available Workflows

### 1. AI-Powered Paper Update Agent ⭐ (Recommended)
**File**: `workflows/ai-paper-update.yml`  
**Trigger**: Weekly (Monday 9 AM UTC), Manual, or on workflow changes  
**Purpose**: AI-powered automated updates to keep the paper current

**What it does:**
- 🤖 Runs AI Update Agent (`scripts/update_agent.py`)
  - Searches arXiv for relevant new papers (15 curated queries)
  - Uses GPT-4o-mini to analyze paper relevance (0-10 score)
  - Suggests which section papers belong to
- 📦 Checks PyPI for framework version updates (LangChain, LangGraph, etc.)
- 🔗 Verifies links in README and paper
- 💡 Generates AI-powered content suggestions
- 📝 Updates paper version automatically (YYYY.MM.DD format)
- 📊 Creates/updates GitHub issue with comprehensive report
- 🌐 Deploys updated documentation to GitHub Pages
- 💾 Commits changes automatically

**Requirements:**
- `OPENAI_API_KEY` secret must be set (see [SETUP_GITHUB_ACTIONS.md](SETUP_GITHUB_ACTIONS.md))
- Workflow permissions: read/write for contents, issues, PRs

**Estimated runtime**: 5-10 minutes  
**Cost**: ~$0.03 per run in OpenAI API credits

**Manual trigger:**
```bash
# Via GitHub UI:
Actions → AI-Powered Paper Update Agent → Run workflow

# Via GitHub CLI:
gh workflow run ai-paper-update.yml
```

### 2. Weekly Paper Update (Basic)
**File**: `workflows/weekly-paper-update.yml`  
**Trigger**: Weekly (Monday 9 AM UTC), Manual  
**Purpose**: Basic weekly paper search and version update (no AI)

**What it does:**
- 📚 Searches for new papers (basic search, no AI analysis)
- 📝 Updates paper version automatically
- 💾 Commits changes
- 🌐 Deploys documentation
- 📊 Creates GitHub issue with findings

**Requirements:**
- No API key needed (free)
- Workflow permissions: read/write for contents, issues

**Estimated runtime**: 2-3 minutes  
**Cost**: FREE (GitHub Actions)

**Manual trigger:**
```bash
# Via GitHub UI:
Actions → Weekly Paper Update → Run workflow

# Via GitHub CLI:
gh workflow run weekly-paper-update.yml
```

## 🔧 Configuration

### Secrets Required

Add in **Settings → Secrets and variables → Actions**:

| Secret Name | Description | Required By |
|------------|-------------|-------------|
| `OPENAI_API_KEY` | OpenAI API key for GPT-4 analysis | ai-paper-update.yml |

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
| AI-Powered Paper Update | Every Monday 9 AM UTC | `0 9 * * 1` |
| Weekly Paper Update | Every Monday 9 AM UTC | `0 9 * * 1` |

### Customizing Schedule

Edit the `cron` expression in `ai-paper-update.yml` or `weekly-paper-update.yml`:

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

**ai-paper-update.yml**:
- `update_report.md` - Human-readable markdown report with AI analysis
- `update_suggestions.json` - Machine-readable JSON data
- Retained for 30 days

**weekly-paper-update.yml**:
- `new_papers_weekly.md` - Basic paper search results
- `update_summary.md` - Update summary
- Retained for 30 days

**Access artifacts:**
1. Go to Actions → Select workflow run
2. Scroll to "Artifacts" section
3. Click to download

### Issues

**ai-paper-update.yml** creates/updates an issue:
- **Title**: `🤖 AI-Powered Paper Update - YYYY-MM-DD`
- **Labels**: `ai-update`, `paper-review`, `automated`
- **Content**: Full AI analysis report with paper recommendations
- **Location**: Issues tab

**weekly-paper-update.yml** creates/updates an issue:
- **Title**: `📚 Weekly Paper Update - YYYY-MM-DD`
- **Labels**: `weekly-update`, `paper-review`, `automated`
- **Content**: Basic paper search results
- **Location**: Issues tab

If an existing issue with matching labels exists (and is open), it will be updated instead of creating a new one.

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

- **[SETUP_GITHUB_ACTIONS.md](SETUP_GITHUB_ACTIONS.md)** - Complete setup guide ⭐
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

