# AI Agent Automation Guide

> **Keep your knowledge base automatically updated with AI agents**

This guide shows you how to create AI agents that automatically maintain and update your knowledge base content.

---

## 🤖 Quick Overview

We've created **3 automation approaches**:

1. **GitHub Actions Agent** - Automated weekly updates (`.github/workflows/content-update-agent.yml`)
2. **Python Update Agent** - Script-based updates (`.github/scripts/update_agent.py`)
3. **LangGraph Agent** - Advanced graph-based workflow (`.github/scripts/langgraph_update_agent.py`)

---

## 🚀 Option 1: GitHub Actions (Easiest)

### Setup

1. **Add API Keys to GitHub Secrets**
   ```
   Repository Settings → Secrets → Actions → New secret
   
   Add:
   - OPENAI_API_KEY (your OpenAI key)
   - ANTHROPIC_API_KEY (optional, for Claude)
   ```

2. **Enable GitHub Actions**
   - The workflow file is already in `.github/workflows/`
   - It runs automatically every Monday at 9 AM UTC
   - Or trigger manually: Actions → Content Update Agent → Run workflow

3. **Review Pull Requests**
   - Agent creates PRs with proposed changes
   - Review and merge or request modifications

### What It Does

✅ Checks for framework version updates (LangChain, LangGraph, Pydantic AI)  
✅ Verifies links aren't broken  
✅ Updates technology comparisons  
✅ Flags outdated content  
✅ Creates PR with all changes  

### Cost

- **Free tier**: ~$0-5/month (depending on API usage)
- **Paid**: ~$10-20/month for comprehensive updates

---

## 🐍 Option 2: Run Locally

### Setup

```bash
# Install dependencies
pip install openai anthropic requests beautifulsoup4

# Set API keys
export OPENAI_API_KEY="your-key"
export ANTHROPIC_API_KEY="your-key"

# Run the agent
python .github/scripts/update_agent.py
```

### What It Does

1. **Checks Framework Updates**
   ```python
   # Monitors GitHub releases for:
   - LangChain
   - LangGraph
   - Pydantic AI
   - DSPy
   ```

2. **Verifies Links**
   ```python
   # Scans all .md files
   # Checks HTTP status codes
   # Reports broken links
   ```

3. **Reviews Content**
   ```python
   # Flags outdated dates
   # Suggests updates
   # Generates report
   ```

### Output

Creates `agent-report.json` with all findings:
```json
{
  "timestamp": "2025-11-14T...",
  "changes_count": 5,
  "changes": [...]
}
```

---

## 🔄 Option 3: Advanced LangGraph Agent

### Setup

```bash
# Install LangGraph
pip install langgraph langchain-openai

# Run the agent
python .github/scripts/langgraph_update_agent.py
```

### Workflow

The agent uses a graph-based workflow:

```
┌─────────────┐
│  Research   │ ─→ Gather latest AI/ML info
└──────┬──────┘
       ↓
┌─────────────┐
│  Planning   │ ─→ Decide what to update
└──────┬──────┘
       ↓
┌─────────────┐
│  Update     │ ─→ Make changes to files
└──────┬──────┘
       ↓
┌─────────────┐
│ Verification│ ─→ Verify accuracy
└──────┬──────┘
       ↓
┌─────────────┐
│  PR Create  │ ─→ Generate pull request
└─────────────┘
```

### Customization

Edit the agent to:
- Add more research topics
- Change update frequency
- Customize verification rules
- Adjust PR templates

---

## 🛠️ Customizing the Agents

### Add New Frameworks to Monitor

Edit `.github/scripts/update_agent.py`:

```python
frameworks = {
    "langchain": "https://api.github.com/repos/langchain-ai/langchain/releases/latest",
    "your-framework": "https://api.github.com/repos/owner/repo/releases/latest",
}
```

### Change Update Schedule

Edit `.github/workflows/content-update-agent.yml`:

```yaml
on:
  schedule:
    - cron: '0 9 * * 1'  # Every Monday at 9 AM
    # Change to:
    - cron: '0 0 * * *'  # Every day at midnight
```

### Add Custom Checks

In `update_agent.py`, add a new method:

```python
def check_custom_content(self):
    """Your custom check logic"""
    print("🔍 Running custom checks...")
    # Your code here
    self.changes.append({
        "type": "custom_check",
        "result": "..."
    })
```

Then call it in `run()`:

```python
def run(self):
    self.check_framework_updates()
    self.verify_links()
    self.check_custom_content()  # Add this
    self.generate_report()
```

---

## 💡 Best Practices

### 1. Start Simple
- Begin with basic link checking
- Add framework monitoring
- Gradually add AI-powered updates

### 2. Review Everything
- Never auto-merge agent PRs
- Always review changes manually
- Verify accuracy before merging

### 3. Monitor Costs
- Set API rate limits
- Use caching when possible
- Monitor monthly bills

### 4. Version Control
- Keep agent changes in separate branches
- Use clear commit messages
- Tag releases after updates

### 5. Test Locally First
```bash
# Test before committing
python .github/scripts/update_agent.py
# Review agent-report.json
# Commit only if satisfied
```

---

## 🎯 Use Cases

### Weekly Content Updates
```yaml
schedule:
  - cron: '0 9 * * 1'  # Monday mornings
```
**Best for**: Regular maintenance

### Daily Link Checks
```yaml
schedule:
  - cron: '0 0 * * *'  # Every day
```
**Best for**: Catching broken links quickly

### Monthly Deep Reviews
```yaml
schedule:
  - cron: '0 9 1 * *'  # First of month
```
**Best for**: Comprehensive content audits

---

## 🔐 Security Notes

### Protect API Keys
- Never commit keys to repo
- Use GitHub Secrets for automation
- Rotate keys regularly
- Use environment-specific keys

### Review Agent Changes
- Always review PRs from agents
- Verify accuracy of updates
- Check for unintended changes
- Test locally when possible

### Limit Permissions
- Agent only needs read/write access
- No admin permissions required
- Use fine-grained tokens
- Monitor activity logs

---

## 📊 Monitoring

### Track Agent Performance

```python
# Add to agent
def log_metrics(self):
    metrics = {
        "runtime": self.end_time - self.start_time,
        "changes": len(self.changes),
        "api_calls": self.api_call_count,
        "cost_estimate": self.api_call_count * 0.002
    }
    print(json.dumps(metrics))
```

### GitHub Actions Logs
- View in GitHub Actions tab
- Check run duration
- Monitor success rate
- Review error logs

---

## 🚨 Troubleshooting

### Agent Not Running
- Check GitHub Actions is enabled
- Verify workflow file syntax
- Check API keys in Secrets
- Review permissions

### API Rate Limits
```python
import time
time.sleep(1)  # Add delays between requests
```

### Broken Links False Positives
```python
# Ignore certain domains
IGNORE_DOMAINS = ['example.com']
if any(domain in url for domain in IGNORE_DOMAINS):
    continue
```

---

## 🎓 Advanced: Multi-Agent System

Create specialized agents:

```
┌──────────────────┐
│ Framework Agent  │ ─→ Monitors releases
└────────┬─────────┘
         │
         ↓
┌──────────────────┐
│  Content Agent   │ ─→ Updates docs
└────────┬─────────┘
         │
         ↓
┌──────────────────┐
│   Quality Agent  │ ─→ Verifies changes
└────────┬─────────┘
         │
         ↓
┌──────────────────┐
│  Merge Agent     │ ─→ Creates PR
└──────────────────┘
```

---

## 📚 Next Steps

1. **Setup**: Add API keys to GitHub Secrets
2. **Test**: Run agent locally first
3. **Deploy**: Enable GitHub Actions workflow
4. **Monitor**: Check weekly PRs
5. **Customize**: Add your own checks
6. **Scale**: Create specialized agents

---

## 💰 Cost Estimates

| Approach | API Calls/Week | Est. Cost/Month |
|----------|----------------|-----------------|
| Basic checks | ~100 | $0-2 |
| With AI updates | ~500 | $5-10 |
| Comprehensive | ~2000 | $20-40 |

---

## 🤝 Contributing

Improve the agents:
1. Fork repository
2. Enhance agent logic
3. Test thoroughly
4. Submit PR
5. Share improvements

---

**Your knowledge base can now maintain itself! 🤖✨**

Questions? Check the agent logs or modify the scripts to fit your needs.
