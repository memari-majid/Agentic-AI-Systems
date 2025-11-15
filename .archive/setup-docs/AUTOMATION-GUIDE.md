# Automation Guide - Keep Content Updated

This guide explains how to set up automated content updates for the Agentic AI Systems review using GitHub Actions and OpenAI API.

## 🎯 Overview

The automated update system:
- ✅ Searches arXiv for new relevant papers weekly
- ✅ Checks for framework version updates
- ✅ Verifies internal and external links
- ✅ Generates content improvement suggestions using GPT-4
- ✅ Creates GitHub issues with findings

## 🚀 Quick Setup

### Step 1: Add OpenAI API Key to GitHub Secrets

1. **Get your OpenAI API Key**
   - Go to [OpenAI API Keys](https://platform.openai.com/api-keys)
   - Create a new secret key if you don't have one
   - Copy the key (it starts with `sk-proj-...`)

2. **Add to GitHub Secrets**
   - Go to your repository on GitHub
   - Click **Settings** → **Secrets and variables** → **Actions**
   - Click **New repository secret**
   - Name: `OPENAI_API_KEY`
   - Value: Paste your API key
   - Click **Add secret**

### Step 2: Enable GitHub Actions

1. Go to your repository **Settings** → **Actions** → **General**
2. Under **Workflow permissions**, select:
   - ✅ **Read and write permissions**
   - ✅ **Allow GitHub Actions to create and approve pull requests**
3. Click **Save**

### Step 3: Test the Workflow

You can trigger the workflow manually:

1. Go to **Actions** tab
2. Select **Update Agentic AI Systems Review**
3. Click **Run workflow** → **Run workflow**
4. Wait for completion (~5-10 minutes)
5. Check the **Issues** tab for the automated report

## 📅 Schedule

The workflow runs automatically:
- **Every Monday at 9:00 AM UTC**
- **On manual trigger** (via Actions tab)
- **On push** to workflow files (for testing)

## 📊 What Gets Checked

### 1. New Research Papers (arXiv)
- Searches using 15 curated prompts from `SEARCH-PROMPTS-FOR-IMPROVEMENT.md`
- Uses GPT-4o-mini to analyze relevance
- Scores papers on 0-10 relevance scale
- Suggests appropriate sections for inclusion

### 2. Framework Updates
- Checks PyPI for latest versions of:
  - LangChain, LangGraph
  - Pydantic AI
  - DSPy
  - CrewAI
  - AutoGPT

### 3. Link Verification
- Scans `README.md` and `paper.tex`
- Verifies external links (HTTP HEAD requests)
- Reports broken or unreachable links

### 4. Content Suggestions
- Uses GPT-4o to analyze current content
- Suggests emerging topics and improvements
- Provides actionable recommendations

## 📝 Output

### GitHub Issue
An issue is created/updated with:
- Summary of findings
- Top 10 relevant new papers with details
- Framework version updates
- Broken links to fix
- Content improvement suggestions
- Prioritized action items

### Artifacts
Downloadable from workflow run:
- `update_report.md` - Full markdown report
- `update_suggestions.json` - Structured JSON data

## 💰 Cost Estimation

Typical weekly run costs (OpenAI API):
- **GPT-4o-mini** (paper analysis): ~15-20 calls × $0.0001 = ~$0.002
- **GPT-4o** (suggestions): 1 call × $0.005 = ~$0.005
- **Total per week**: ~$0.007 (less than 1 cent)
- **Total per year**: ~$0.36

Note: arXiv searches are free, no API key required.

## 🔧 Customization

### Adjust Search Prompts

Edit `arxiv-paper/SEARCH-PROMPTS-FOR-IMPROVEMENT.md`:
- Add new search prompts
- Modify existing ones
- The agent uses the first 15 prompts

### Change Schedule

Edit `.github/workflows/update-review.yml`:

```yaml
on:
  schedule:
    # Custom cron schedule
    - cron: '0 9 * * 1'  # Every Monday at 9 AM UTC
```

Examples:
- Daily: `'0 9 * * *'`
- Bi-weekly: `'0 9 1,15 * *'`
- Monthly: `'0 9 1 * *'`

### Adjust Search Limits

Edit `scripts/update_agent.py`:

```python
# Line ~172: Number of search prompts to use
for i, prompt in enumerate(self.search_prompts[:10], 1):

# Line ~48: Papers per search
max_results=5

# Line ~189: Final paper count
)[:15]  # Top 15 papers
```

## 🧪 Local Testing

Test the update agent locally:

```bash
# Install dependencies
pip install -r requirements.txt

# Set API key
export OPENAI_API_KEY="sk-proj-your-key-here"

# Run agent
python scripts/update_agent.py

# Check output
cat update_report.md
```

## 🔍 Monitoring

### Check Workflow Status
1. Go to **Actions** tab
2. View recent runs
3. Click run for detailed logs

### View Reports
1. Go to workflow run
2. Download artifacts
3. Or check the created/updated issue

## 🛡️ Security Best Practices

✅ **DO:**
- Store API key in GitHub Secrets
- Use separate API key for this repo
- Set spending limits in OpenAI dashboard
- Monitor API usage regularly

❌ **DON'T:**
- Commit API keys to repository
- Share API keys in issues/PRs
- Use personal API key for shared repos

## 🐛 Troubleshooting

### "OPENAI_API_KEY environment variable is required"
- Check that secret is added correctly in GitHub Settings
- Ensure secret name is exactly `OPENAI_API_KEY`

### "Permission denied" errors
- Enable read/write permissions in repository settings
- Check workflow permissions under Actions settings

### "Rate limit exceeded"
- The script includes rate limiting (1s delay between searches)
- Reduce number of search prompts if needed
- Check OpenAI API usage dashboard

### Workflow not running on schedule
- GitHub Actions can be delayed by up to 15 minutes
- Repository must have recent activity
- Try manual trigger to test

## 📚 Advanced Usage

### Create Pull Request Instead of Issue

Modify `.github/workflows/update-review.yml` to create PR:

```yaml
- name: Create Pull Request
  uses: peter-evans/create-pull-request@v6
  with:
    title: '🤖 Automated Review Updates'
    body-path: update_report.md
    branch: automated-updates
    labels: automated-update
```

### Notify via Slack/Discord

Add webhook notification step:

```yaml
- name: Notify Slack
  if: success()
  uses: slackapi/slack-github-action@v1
  with:
    webhook-url: ${{ secrets.SLACK_WEBHOOK }}
    payload: |
      {
        "text": "New updates available for Agentic AI Systems review!"
      }
```

### Email Notifications

Enable in repository **Settings** → **Notifications**

## 🤝 Contributing

To improve the automation:
1. Modify `scripts/update_agent.py` for new features
2. Update search prompts in `SEARCH-PROMPTS-FOR-IMPROVEMENT.md`
3. Enhance workflow in `.github/workflows/update-review.yml`
4. Test locally before pushing
5. Update this guide with changes

## 📞 Support

For issues with:
- **GitHub Actions**: Check Actions tab logs
- **OpenAI API**: Visit [OpenAI Help Center](https://help.openai.com/)
- **This automation**: Open an issue in the repository

---

**Last Updated**: 2025-11-15  
**Version**: 1.0.0

