# Quick Reference Guide

Essential commands and workflows for managing the Agentic AI Systems repository.

## 🚀 Common Commands

### GitHub Pages

```bash
# Run locally
mkdocs serve
# Visit: http://127.0.0.1:8000

# Deploy to GitHub Pages
mkdocs gh-deploy

# Force redeploy
mkdocs gh-deploy --force
```

### Paper Building

```bash
cd arxiv-paper

# Full build
make

# Quick build
make quick

# View PDF
make view

# Clean files
make clean

# Word count
make wordcount
```

### Finding New Papers

```bash
# Automated search (last 7 days)
python scripts/search_new_papers.py

# Longer time window
python scripts/search_new_papers.py --days 14

# Custom output
python scripts/search_new_papers.py --output my_papers.md
```

## 📚 Key File Locations

| What | Where |
|------|-------|
| **Paper PDF** | `arxiv-paper/paper.pdf` |
| **LaTeX source** | `arxiv-paper/paper.tex` |
| **Bibliography** | `arxiv-paper/references.bib` |
| **Research papers** | `papers/*.pdf` |
| **Paper summaries** | `papers/PAPERS_SUMMARY.md` |
| **Integration guide** | `papers/INTEGRATION_GUIDE.md` |
| **Update rules** | `PAPER_UPDATE_RULES.md` |
| **GitHub Pages guide** | `GITHUB_PAGES_GUIDE.md` |

## 🔄 Update Workflows

### Adding a New Paper

```bash
# 1. Search for papers
python scripts/search_new_papers.py

# 2. Review new_papers.md
cat new_papers.md

# 3. Download PDF to papers/
cp downloaded.pdf papers/NewPaper2025.pdf

# 4. Add BibTeX entry
nano arxiv-paper/references.bib

# 5. Integrate into paper
nano arxiv-paper/paper.tex

# 6. Build and check
cd arxiv-paper && make && make view

# 7. Update documentation
nano papers/PAPERS_SUMMARY.md

# 8. Deploy docs
mkdocs gh-deploy
```

### Quick Paper Check

```bash
# Check compilation
cd arxiv-paper && make quick

# Check citations
cd arxiv-paper && grep -o '\\cite{[^}]*}' paper.tex | sort -u

# Count references
cd arxiv-paper && grep -c '^@' references.bib
```

### Documentation Update

```bash
# Edit content
nano docs/some-page.md

# Preview
mkdocs serve

# Deploy
mkdocs gh-deploy
```

## 🔍 Search Queries

### Google Scholar Alerts

Set up alerts for:
- "agentic AI"
- "autonomous agents" + "large language models"
- "multi-agent systems" + LLM
- "tool use" + "language models"

### Manual Search Commands

```bash
# arXiv
curl "http://export.arxiv.org/api/query?search_query=all:agentic+AI&sortBy=submittedDate&sortOrder=descending&max_results=10"

# Semantic Scholar (requires API key)
curl "https://api.semanticscholar.org/graph/v1/paper/search?query=agentic+AI&limit=10"
```

## 📊 Quality Checks

### Before Committing

```bash
# Build paper
cd arxiv-paper && make

# Check for errors
echo $?  # Should be 0

# View PDF
make view

# Count pages
pdfinfo paper.pdf | grep Pages

# Count references
grep -c '^@' references.bib
```

### Before Deploying Docs

```bash
# Build locally
mkdocs build

# Check for warnings
mkdocs build --strict

# Test locally
mkdocs serve

# Then deploy
mkdocs gh-deploy
```

## 🎯 Weekly Routine

### Monday Morning (30 min)

```bash
# 1. Search for new papers
python scripts/search_new_papers.py

# 2. Check report
cat new_papers.md

# 3. Add to review queue
# (Manually review and prioritize)
```

### Monthly Update (2 hours)

```bash
# 1. Deep search
python scripts/search_new_papers.py --days 30

# 2. Integrate 2-3 high-priority papers
# (Follow PAPER_UPDATE_RULES.md)

# 3. Update documentation
nano papers/PAPERS_SUMMARY.md

# 4. Rebuild everything
cd arxiv-paper && make clean && make
mkdocs build

# 5. Deploy
mkdocs gh-deploy
```

## 🆘 Troubleshooting

### LaTeX won't compile

```bash
cd arxiv-paper

# Clean and rebuild
make clean
make

# Check for errors in output
# Look for lines starting with "!"
```

### Missing citation

```bash
cd arxiv-paper

# Find undefined citations
grep "Citation.*undefined" paper.log

# Check if in references.bib
grep "@.*{keyname" references.bib
```

### GitHub Pages not updating

```bash
# Force deployment
mkdocs gh-deploy --force

# Check GitHub Pages status
# Go to: Settings → Pages
```

### Script not working

```bash
# Check Python version
python --version  # Should be 3.7+

# Install dependencies
pip install -r requirements.txt

# Run with verbose output
python scripts/search_new_papers.py --verbose
```

## 📧 Getting Help

**Documentation**:
- Full GitHub Pages guide: `GITHUB_PAGES_GUIDE.md`
- Update rules: `PAPER_UPDATE_RULES.md`
- Organization: `ORGANIZATION.md`

**Quick Links**:
- Main README: `README.md`
- Start here: `START-HERE.md`
- Structure: `STRUCTURE_VISUAL.md`

**Contact**:
- Email: mmemari@uvu.edu
- Issues: GitHub Issues tab

---

**Last Updated**: November 15, 2025  
**Keep this handy for daily use!**

