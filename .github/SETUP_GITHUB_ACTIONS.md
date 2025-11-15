# 🚀 GitHub Actions Setup Guide

This guide explains how to set up GitHub Actions to automatically run the AI-powered update agent to keep your paper updated.

## 📋 Overview

The repository includes two automated workflows:

1. **`weekly-paper-update.yml`** - Basic weekly update (paper search + version update)
2. **`ai-paper-update.yml`** - AI-powered update agent (recommended) ✨

## 🎯 Quick Setup (5 minutes)

### Step 1: Add OpenAI API Key Secret

1. Go to your repository on GitHub
2. Navigate to **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Name: `OPENAI_API_KEY`
5. Value: Your OpenAI API key (starts with `sk-`)
6. Click **Add secret**

### Step 2: Verify Workflow Files

The workflow files are already in place:
- `.github/workflows/weekly-paper-update.yml` ✅
- `.github/workflows/ai-paper-update.yml` ✅

### Step 3: Test the Workflow

1. Go to **Actions** tab in your repository
2. Select **AI-Powered Paper Update Agent** workflow
3. Click **Run workflow** → **Run workflow**
4. Watch it execute!

## 🔧 What Each Workflow Does

### AI-Powered Paper Update Agent (`ai-paper-update.yml`)

**Runs**: Every Monday at 9:00 AM UTC (or manually)

**What it does**:
1. 🤖 **Runs AI Update Agent** (`scripts/update_agent.py`)
   - Searches arXiv for new papers (15 curated queries)
   - Uses GPT-4o-mini to analyze paper relevance
   - Scores papers 0-10 and suggests sections
   - Checks framework version updates (LangChain, LangGraph, etc.)
   - Verifies links in README and paper
   - Generates AI-powered content suggestions

2. 📝 **Updates Paper Version**
   - Updates version number (YYYY.MM.DD format)
   - Updates last modified date in LaTeX and HTML

3. 💾 **Commits Changes**
   - Commits update reports and version changes
   - Pushes to main branch

4. 🌐 **Deploys Documentation**
   - Deploys updated docs to GitHub Pages

5. 📊 **Creates GitHub Issue**
   - Creates/updates issue with findings
   - Includes paper recommendations
   - Labels: `ai-update`, `paper-review`, `automated`

**Requirements**:
- `OPENAI_API_KEY` secret (required)
- Estimated cost: ~$0.03 per run
- Runtime: 5-10 minutes

### Weekly Paper Update (`weekly-paper-update.yml`)

**Runs**: Every Monday at 9:00 AM UTC (or manually)

**What it does**:
1. 📚 Searches for new papers (basic search)
2. 📝 Updates paper version
3. 💾 Commits changes
4. 🌐 Deploys documentation
5. 📊 Creates GitHub issue

**Requirements**:
- No API key needed (free)
- Runtime: 2-3 minutes

## 🔐 Required Secrets

### For AI-Powered Workflow

| Secret Name | Description | Where to Get |
|------------|-------------|--------------|
| `OPENAI_API_KEY` | OpenAI API key for GPT-4 analysis | https://platform.openai.com/api-keys |

**How to add**:
1. Go to: **Settings** → **Secrets and variables** → **Actions**
2. Click **New repository secret**
3. Add the secret name and value
4. Click **Add secret**

## 📅 Schedule Configuration

Both workflows run on a schedule defined by cron syntax:

```yaml
schedule:
  - cron: '0 9 * * 1'  # Every Monday at 9:00 AM UTC
```

**To change the schedule**:
- Edit `.github/workflows/ai-paper-update.yml`
- Modify the cron expression
- Cron format: `minute hour day month weekday`
- Examples:
  - `'0 9 * * 1'` - Every Monday 9 AM UTC
  - `'0 0 * * 0'` - Every Sunday midnight UTC
  - `'0 12 * * *'` - Every day at noon UTC

## 🧪 Testing Locally

Before relying on GitHub Actions, test the agent locally:

```bash
# Set API key
export OPENAI_API_KEY="sk-your-key-here"

# Install dependencies
pip install -r requirements.txt

# Run the agent
python scripts/update_agent.py

# Check outputs
cat update_report.md
cat update_suggestions.json
```

## 📊 Monitoring

### Check Workflow Runs

1. Go to: **Actions** tab in your repository
2. Click on a workflow to see run history
3. Click on a specific run to see logs

### Check Generated Issues

1. Go to: **Issues** tab
2. Filter by label: `ai-update` or `weekly-update`
3. See automated findings and recommendations

### Check Artifacts

1. Go to: **Actions** → Select a run
2. Scroll to **Artifacts** section
3. Download `update_report.md` and `update_suggestions.json`

## 🐛 Troubleshooting

### Workflow Fails with "OPENAI_API_KEY not found"

**Solution**: Add the secret in **Settings** → **Secrets and variables** → **Actions**

### Workflow Runs but No Changes Committed

**Possible reasons**:
- No new papers found
- No framework updates
- Version already updated today

**Check**: Look at workflow logs to see what was found

### API Rate Limits

**Solution**: The workflow includes rate limiting and delays. If you hit limits:
- Reduce number of search queries in `update_agent.py`
- Increase delays between API calls
- Use a higher-tier OpenAI plan

### Permission Errors

**Solution**: Ensure workflow has proper permissions:
```yaml
permissions:
  contents: write
  issues: write
  pull-requests: write
```

## 🎯 Best Practices

1. **Monitor First Few Runs**: Check that everything works correctly
2. **Review Generated Issues**: The AI suggestions are helpful but need human review
3. **Adjust Schedule**: Run more/less frequently based on your needs
4. **Set Budget Alerts**: Monitor OpenAI API usage
5. **Keep Secrets Secure**: Never commit API keys to the repository

## 📝 Workflow Customization

### Add More Search Queries

Edit `scripts/update_agent.py`:
```python
def get_default_prompts(self) -> List[str]:
    return [
        "Your new search query here",
        # ... existing queries
    ]
```

### Change Update Frequency

Edit `.github/workflows/ai-paper-update.yml`:
```yaml
schedule:
  - cron: '0 9 * * 1'  # Change this
```

### Modify Issue Labels

Edit the workflow file:
```yaml
labels: ['ai-update', 'paper-review', 'automated', 'your-label']
```

## ✅ Verification Checklist

- [ ] `OPENAI_API_KEY` secret added to repository
- [ ] Workflow files exist in `.github/workflows/`
- [ ] Tested workflow manually (Actions → Run workflow)
- [ ] Verified workflow runs successfully
- [ ] Checked that issues are created
- [ ] Confirmed changes are committed
- [ ] Documentation deploys correctly

## 🎉 You're All Set!

Once configured, the AI agent will:
- ✅ Run automatically every Monday
- ✅ Find new relevant papers
- ✅ Analyze them with AI
- ✅ Update paper version
- ✅ Create issues with recommendations
- ✅ Keep your paper current

## 📚 Additional Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [OpenAI API Documentation](https://platform.openai.com/docs)
- [Cron Expression Guide](https://crontab.guru/)

---

**Questions?** Check the workflow logs or review the scripts in `scripts/` directory.

