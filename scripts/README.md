# Update Agent Scripts

This directory contains automation scripts for keeping the Agentic AI Systems review up to date.

## 📁 Files

### `update_agent.py`
Main automation script that:
- Searches arXiv for new research papers
- Analyzes paper relevance using OpenAI GPT-4
- Checks framework version updates
- Verifies links in documentation
- Generates content improvement suggestions
- Creates detailed update reports

**Usage:**
```bash
export OPENAI_API_KEY="your-key"
python scripts/update_agent.py
```

**Output:**
- `update_report.md` - Human-readable markdown report
- `update_suggestions.json` - Machine-readable JSON data

### `test_update_agent.py`
Test script to validate the environment before running the full update agent.

**Usage:**
```bash
export OPENAI_API_KEY="your-key"
python scripts/test_update_agent.py
```

**Tests:**
- ✅ Environment setup (API key, files)
- ✅ Dependencies installed
- ✅ Search prompts loading
- ✅ OpenAI API connection

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

Required packages:
- `openai>=1.12.0` - OpenAI API client
- `requests>=2.31.0` - HTTP requests
- `aiohttp>=3.9.0` - Async HTTP for parallel searches
- `beautifulsoup4>=4.12.0` - HTML parsing (if needed)
- `python-dateutil>=2.8.2` - Date parsing

### 2. Set Up API Key

**Option A: Environment Variable**
```bash
export OPENAI_API_KEY="sk-proj-your-key-here"
```

**Option B: .env File** (recommended for local dev)
```bash
# Copy example
cp .env.example .env

# Edit .env and add your key
nano .env

# Load in your script
pip install python-dotenv
```

### 3. Test the Setup

```bash
python scripts/test_update_agent.py
```

Should see:
```
✅ OPENAI_API_KEY is set
✅ All required files found
✅ All dependencies installed
✅ API connection successful
```

### 4. Run the Update Agent

```bash
python scripts/update_agent.py
```

Takes ~5-10 minutes. Progress shown in real-time:
```
🤖 Starting Agentic AI Systems Update Agent...
📚 Searching for new research papers...
  [1/10] Searching: Survey of Large Language Model based...
  ...
✅ Found 12 relevant papers
🔧 Checking framework updates...
✅ Checked 6 frameworks
🔗 Verifying links...
✅ Found 3 broken links
💡 Generating content suggestions...
✅ Generated 5 suggestions
📝 Report saved to update_report.md
✨ Update check complete!
```

## 📊 Understanding the Output

### update_report.md

Structured markdown report with:

**1. Summary**
- Quick overview of findings
- Counts for each category

**2. New Relevant Papers**
- Top 10-15 papers by relevance score
- Author, date, summary
- Relevance analysis by AI
- Suggested section for inclusion

**3. Framework Updates**
- Latest versions from PyPI
- Release dates
- Links to documentation

**4. Broken Links**
- Files containing broken links
- Link text and URL
- Error status/message

**5. Content Suggestions**
- AI-generated improvement ideas
- Emerging topics to cover
- Gaps in current content

**6. Action Items**
- Prioritized list of tasks
- Based on findings above

### update_suggestions.json

Machine-readable JSON with:
```json
{
  "new_papers": [...],
  "framework_updates": [...],
  "broken_links": [...],
  "content_suggestions": [...],
  "timestamp": "2025-11-15T12:00:00"
}
```

Can be processed by other tools or scripts.

## ⚙️ Customization

### Adjust Search Prompts

Edit `arxiv-paper/SEARCH-PROMPTS-FOR-IMPROVEMENT.md`:
- Add new prompts
- Modify existing ones
- Agent uses first 15 by default

### Change Search Limits

Edit `update_agent.py`:

```python
# Line ~48: Change number of search prompts
self.search_prompts = self.load_search_prompts()[:10]

# Line ~172: Change papers per search
papers = await self.search_arxiv(prompt, max_results=3)

# Line ~189: Change final paper count
)[:15]  # Top 15 papers
```

### Add New Checks

Extend the `UpdateAgent` class:

```python
async def check_new_feature(self):
    """Add your custom check here."""
    # Your implementation
    pass

# Add to run() method
async def run(self):
    # ... existing checks ...
    self.findings['new_feature'] = await self.check_new_feature()
```

## 🔧 Troubleshooting

### "OPENAI_API_KEY environment variable is required"

```bash
# Check if set
echo $OPENAI_API_KEY

# Set it
export OPENAI_API_KEY="your-key"

# Or use .env file
cp .env.example .env
# Edit .env with your key
```

### "Module not found" errors

```bash
# Install all dependencies
pip install -r requirements.txt

# Or install individually
pip install openai requests aiohttp beautifulsoup4 python-dateutil
```

### API rate limits

The script includes rate limiting:
- 1 second between arXiv searches
- 0.5 seconds between framework checks
- 0.3 seconds between link verifications

If you still hit limits, adjust in the code:
```python
await asyncio.sleep(1)  # Increase delay
```

### "Too many papers" / High costs

Reduce search scope:
```python
# Fewer prompts
self.search_prompts[:5]  # Only first 5

# Fewer papers per search
max_results=2  # Down from 3

# Fewer final papers
)[:10]  # Down from 15
```

### Broken link false positives

Some sites block automated requests. To skip:
```python
# Skip specific domains
if 'example.com' in url:
    continue
```

## 💰 Cost Estimates

### OpenAI API Costs (per run)

**GPT-4o-mini** (paper analysis):
- 15-20 calls
- ~500 tokens per call
- $0.15 per 1M input tokens
- **Cost**: ~$0.002 per run

**GPT-4o** (content suggestions):
- 1 call
- ~5000 tokens input, 1000 output
- $5 per 1M input, $15 per 1M output
- **Cost**: ~$0.025 per run

**Total**: ~$0.027 per run (~3 cents)

**Weekly**: ~$0.11/week  
**Monthly**: ~$0.47/month  
**Yearly**: ~$1.40/year

### arXiv API
- Free
- Rate limited: 1 request/second (we comply)

### GitHub Actions
- Free tier: 2,000 minutes/month
- This workflow: ~5-10 minutes/week
- Monthly: ~40 minutes (~2% of free tier)

## 🧪 Development

### Running Tests

```bash
# Quick validation
python scripts/test_update_agent.py

# Full agent (with API calls)
python scripts/update_agent.py
```

### Adding Tests

Edit `test_update_agent.py`:

```python
def test_my_feature():
    """Test description."""
    # Your test code
    return True

# Add to tests list
tests = [
    # ... existing tests ...
    ("My Feature", test_my_feature),
]
```

### Code Style

We follow Python best practices:
```bash
# Format code
pip install black
black scripts/

# Lint code
pip install flake8
flake8 scripts/
```

## 📚 API Documentation

### OpenAI API
- [Documentation](https://platform.openai.com/docs)
- [API Reference](https://platform.openai.com/docs/api-reference)
- [Rate Limits](https://platform.openai.com/docs/guides/rate-limits)

### arXiv API
- [API Manual](https://arxiv.org/help/api/user-manual)
- [Terms of Use](https://arxiv.org/help/api/tou)

### PyPI API
- [JSON API](https://warehouse.pypa.io/api-reference/json.html)
- [Simple API](https://warehouse.pypa.io/api-reference/legacy.html)

## 🤝 Contributing

To improve these scripts:

1. **Test locally first**
   ```bash
   python scripts/test_update_agent.py
   python scripts/update_agent.py
   ```

2. **Follow conventions**
   - Type hints
   - Docstrings
   - Error handling
   - Rate limiting

3. **Update documentation**
   - This README
   - AUTOMATION-GUIDE.md
   - Code comments

4. **Submit PR**
   - Clear description
   - Test results
   - Example output

## 📝 Changelog

### Version 1.0.0 (2025-11-15)
- ✨ Initial release
- 📚 arXiv paper search and analysis
- 🔧 Framework version checking
- 🔗 Link verification
- 💡 AI-powered content suggestions
- 📊 Comprehensive reporting

## 📞 Support

- **Issues**: Open a GitHub issue
- **Questions**: Check AUTOMATION-GUIDE.md
- **Security**: See SECURITY.md

---

**Last Updated**: 2025-11-15  
**Author**: Majid Memari  
**License**: MIT

