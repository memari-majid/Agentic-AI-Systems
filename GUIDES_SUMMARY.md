# Complete Guides Summary

All guides for running GitHub Pages and keeping your review paper updated.

## 📚 Available Guides

### 1. GitHub Pages Guide (`GITHUB_PAGES_GUIDE.md`)
**Purpose**: Complete instructions for running and deploying documentation

**Covers**:
- ✅ Local development server setup
- ✅ Deploying to GitHub Pages (3 methods)
- ✅ Automatic deployment with GitHub Actions
- ✅ Customization (CSS, JavaScript)
- ✅ Troubleshooting common issues
- ✅ Custom domain setup
- ✅ Testing before deployment

**Quick Commands**:
```bash
# Run locally
mkdocs serve

# Deploy
mkdocs gh-deploy

# Force deploy
mkdocs gh-deploy --force
```

---

### 2. Paper Update Rules (`PAPER_UPDATE_RULES.md`)
**Purpose**: Academic standards and workflows for keeping review current

**Covers**:
- ✅ Source quality requirements (Tier 1-3 venues)
- ✅ Paper discovery process (search strategies)
- ✅ Quality screening checklist
- ✅ Integration rules and workflows
- ✅ Update frequency guidelines
- ✅ Citation etiquette and best practices
- ✅ Quality control checklist

**Acceptable Sources**:
- **Tier 1**: NeurIPS, ICML, ICLR, ACL, Nature, Science
- **Tier 2**: AAMAS, IEEE Access, Information Fusion
- **Tier 3**: Top venue workshops, major lab reports

**Quick Workflow**:
```bash
# 1. Search
python scripts/search_new_papers.py

# 2. Review
cat new_papers.md

# 3. Integrate
# (Follow INTEGRATION_GUIDE.md)

# 4. Build & Deploy
cd arxiv-paper && make
mkdocs gh-deploy
```

---

### 3. Quick Reference (`QUICK_REFERENCE.md`)
**Purpose**: Common commands and workflows for daily use

**Covers**:
- ✅ Essential commands (paper, docs, search)
- ✅ File locations quick lookup
- ✅ Update workflows
- ✅ Quality check commands
- ✅ Weekly/monthly routines
- ✅ Troubleshooting quick fixes

**Daily Use**:
- Keep this handy for quick command lookup
- Reference during paper updates
- Use for troubleshooting

---

### 4. Paper Search Script (`scripts/search_new_papers.py`)
**Purpose**: Automated discovery of relevant academic papers

**Features**:
- ✅ Searches arXiv automatically
- ✅ Searches Semantic Scholar
- ✅ Filters by date and relevance
- ✅ Generates markdown report with assessment template
- ✅ Configurable time window

**Usage**:
```bash
# Basic search (last 7 days)
python scripts/search_new_papers.py

# Longer timeframe
python scripts/search_new_papers.py --days 14

# Custom output
python scripts/search_new_papers.py --output my_papers.md

# View results
cat new_papers.md
```

---

## 🎯 Common Workflows

### Starting Out

1. **Read this summary** (`GUIDES_SUMMARY.md`)
2. **Quick commands**: Check [`QUICK_REFERENCE.md`](QUICK_REFERENCE.md)
3. **Deep dive**: Read [`GITHUB_PAGES_GUIDE.md`](GITHUB_PAGES_GUIDE.md) or [`PAPER_UPDATE_RULES.md`](PAPER_UPDATE_RULES.md) as needed

### Running Documentation

```bash
# Step 1: Run locally
mkdocs serve
# Open: http://127.0.0.1:8000

# Step 2: Make changes to docs/*.md

# Step 3: Preview (auto-reload)
# Changes appear automatically

# Step 4: Deploy when ready
mkdocs gh-deploy
```

**Full details**: [`GITHUB_PAGES_GUIDE.md`](GITHUB_PAGES_GUIDE.md)

### Updating Paper

```bash
# Step 1: Find papers
python scripts/search_new_papers.py

# Step 2: Review candidates
cat new_papers.md

# Step 3: Check quality
# (Use checklist in PAPER_UPDATE_RULES.md)

# Step 4: Add to references
nano arxiv-paper/references.bib

# Step 5: Integrate content
nano arxiv-paper/paper.tex

# Step 6: Build and check
cd arxiv-paper && make && make view

# Step 7: Update docs
nano papers/PAPERS_SUMMARY.md

# Step 8: Deploy everything
mkdocs gh-deploy
```

**Full details**: [`PAPER_UPDATE_RULES.md`](PAPER_UPDATE_RULES.md)

### Weekly Routine

**Monday Morning (30 min)**:
```bash
# Search for new papers
python scripts/search_new_papers.py

# Review results
cat new_papers.md

# Add promising papers to review queue
# (Manual review and prioritization)
```

**Monthly Deep Dive (2 hours)**:
```bash
# 1. Extended search
python scripts/search_new_papers.py --days 30

# 2. Review and prioritize
cat new_papers.md

# 3. Integrate 2-3 high-priority papers
# (Follow PAPER_UPDATE_RULES.md)

# 4. Update all documentation
nano papers/PAPERS_SUMMARY.md
nano papers/INTEGRATION_GUIDE.md

# 5. Rebuild and deploy
cd arxiv-paper && make clean && make
mkdocs gh-deploy
```

---

## 📊 Academic Standards Summary

### Acceptable Venues

**Tier 1 (Highest Priority)**:
- **ML/AI**: NeurIPS, ICML, ICLR, AAAI, IJCAI
- **NLP**: ACL, EMNLP, NAACL
- **Journals**: Nature, Science, IEEE TPAMI, JMLR

**Tier 2 (Strong)**:
- **MAS**: AAMAS
- **Robotics**: CoRL, ICRA, IROS
- **Journals**: IEEE Access, Information Fusion

**Tier 3 (Acceptable if Recent)**:
- Top venue workshops
- Recent arXiv with citations
- Major lab technical reports (OpenAI, DeepMind, Google)

### Unacceptable Sources
❌ Blogs, Medium articles, Wikipedia, company marketing, personal websites

### Quality Criteria

**Must Have**:
- ✅ Peer-reviewed (or exceptional preprint)
- ✅ Recent (< 3 years, prefer 2022+)
- ✅ Relevant to agentic AI
- ✅ Clear contributions
- ✅ Cited by others (if > 6 months old)

**Nice to Have**:
- High citation count
- Multiple authors from institutions
- Code/data availability
- Reproducibility claims

---

## 🔧 Technical Setup

### Prerequisites

```bash
# Install LaTeX
sudo apt-get install texlive-full

# Install Python dependencies
pip install -r requirements.txt

# Make scripts executable
chmod +x scripts/*.py
```

### First-Time Setup

```bash
# 1. Test paper compilation
cd arxiv-paper && make

# 2. Test documentation
mkdocs serve

# 3. Test paper search
python scripts/search_new_papers.py --days 7

# 4. Deploy docs (if GitHub Pages enabled)
mkdocs gh-deploy
```

---

## 🆘 Getting Help

### Documentation Hierarchy

1. **Quick lookup**: [`QUICK_REFERENCE.md`](QUICK_REFERENCE.md)
2. **This summary**: `GUIDES_SUMMARY.md`
3. **Deep dives**:
   - GitHub Pages: [`GITHUB_PAGES_GUIDE.md`](GITHUB_PAGES_GUIDE.md)
   - Paper updates: [`PAPER_UPDATE_RULES.md`](PAPER_UPDATE_RULES.md)
4. **Repository structure**: [`ORGANIZATION.md`](ORGANIZATION.md)

### Common Issues

**"mkdocs: command not found"**
```bash
pip install -r requirements.txt
```

**"LaTeX compilation fails"**
```bash
cd arxiv-paper
make clean
make
# Check error messages
```

**"GitHub Pages not updating"**
```bash
mkdocs gh-deploy --force
# Wait 1-2 minutes, clear browser cache
```

**"Script won't run"**
```bash
# Check Python version
python --version  # Need 3.7+

# Install dependencies
pip install requests

# Make executable
chmod +x scripts/search_new_papers.py
```

### Contact

**Author**: Majid Memari  
**Email**: mmemari@uvu.edu  
**Institution**: Utah Valley University

---

## 📈 Success Metrics

### For Documentation

- ✅ Site deploys successfully
- ✅ All pages load
- ✅ Search works
- ✅ PDF downloads
- ✅ Mobile responsive

### For Paper Updates

- ✅ Paper compiles without errors
- ✅ All citations render
- ✅ References are current (< 3 years avg)
- ✅ High-quality venues represented
- ✅ Sections well-balanced
- ✅ Professional appearance

### For Repository

- ✅ Clear documentation
- ✅ Easy to navigate
- ✅ Scripts work
- ✅ Regular updates
- ✅ Academic standards maintained

---

## 🎓 Best Practices

### Documentation
1. Update docs with every paper change
2. Keep local preview running while editing
3. Test thoroughly before deploying
4. Clear browser cache after deployment

### Paper Updates
1. Follow academic standards strictly
2. Prioritize peer-reviewed sources
3. Recent papers over older
4. Quality over quantity
5. Document every addition
6. Build and check before committing

### Workflow
1. Work in batches (weekly, monthly)
2. Use checklists
3. Keep documentation current
4. Test everything locally first
5. Deploy only when ready

---

## 🚀 Next Steps

1. **First Time?**
   - Read [`QUICK_REFERENCE.md`](QUICK_REFERENCE.md)
   - Run `mkdocs serve`
   - Try `python scripts/search_new_papers.py`

2. **Regular Use?**
   - Check [`QUICK_REFERENCE.md`](QUICK_REFERENCE.md) for commands
   - Follow weekly/monthly routines
   - Refer to specific guides as needed

3. **Issues?**
   - Check troubleshooting sections
   - Review error messages
   - Contact maintainer

---

**Created**: November 15, 2025  
**Last Updated**: November 15, 2025  
**Version**: 1.0  
**Status**: Production Ready

**Keep this as your main reference for guides!**

