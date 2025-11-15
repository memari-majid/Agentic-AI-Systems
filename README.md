# Agentic AI Systems

A comprehensive knowledge base and research repository on Agentic AI systems, covering theoretical foundations, implementation frameworks, and practical applications.

[![Documentation](https://img.shields.io/badge/docs-latest-blue.svg)](https://memari-majid.github.io/Agentic-AI-Systems/)
[![arXiv Paper](https://img.shields.io/badge/arXiv-paper-red.svg)](arxiv-paper/paper.pdf)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

> 📚 **Complete Guides Available**  
> • [GitHub Pages Setup](GITHUB_PAGES_GUIDE.md) - Run and deploy documentation  
> • [Paper Update Rules](PAPER_UPDATE_RULES.md) - Keep review current with academic standards  
> • [Quick Reference](QUICK_REFERENCE.md) - Common commands and workflows

---

## 🚀 Quick Start

```bash
# View the paper
cd arxiv-paper && make view

# Run documentation locally
mkdocs serve  # Visit http://127.0.0.1:8000

# Search for new papers
python scripts/search_new_papers.py

# Deploy documentation
mkdocs gh-deploy
```

**New here?** → Start with [`START-HERE.md`](START-HERE.md)

## 📚 Repository Structure

```
Agentic-AI-Systems/
├── arxiv-paper/          # Review paper (LaTeX source + PDF)
│   ├── paper.tex         # Main LaTeX document
│   ├── paper.pdf         # Compiled PDF (43 pages, 104 refs)
│   ├── references.bib    # Bibliography
│   └── README.md         # Paper documentation
├── papers/               # Research papers collection
│   ├── *.pdf             # 5 converted research papers
│   ├── PAPERS_SUMMARY.md # Extracted key findings
│   ├── INTEGRATION_GUIDE.md # Integration instructions
│   └── README.md         # Papers documentation
├── docs/                 # MkDocs documentation source
│   ├── index.md          # Landing page
│   └── arxiv-paper/      # Paper documentation pages
├── site/                 # Built documentation (GitHub Pages)
├── scripts/              # Automation scripts
│   └── search_new_papers.py  # Automated paper discovery
├── GITHUB_PAGES_GUIDE.md    # Complete GitHub Pages guide
├── PAPER_UPDATE_RULES.md    # Academic standards & workflows
└── QUICK_REFERENCE.md       # Common commands

```

## 📄 Main Paper

**Title**: Agentic AI Systems: A Comprehensive Framework for Building Autonomous Intelligent Agents

**Author**: Majid Memari (Utah Valley University)

**Status**: Ready for arXiv submission

**Statistics**:
- **Pages**: 43
- **References**: 104 peer-reviewed sources
- **Word Count**: ~21,000 words
- **Code Examples**: 15 complete implementations

### Paper Highlights

1. **Unified Framework**: Theory to production
2. **Autonomy Spectrum**: 5-level classification
3. **7 Core Principles**: Essential design patterns
4. **Pattern Library**: 15+ implementations
5. **RAG vs Fine-Tuning**: Decision framework
6. **Production Playbook**: Complete deployment guide
7. **Strategic Framework**: Organizational adoption

## 🌐 Documentation & Deployment

### GitHub Pages

**Live Site**: https://YOUR-USERNAME.github.io/Agentic-AI-Systems/

**Run Locally**:
```bash
mkdocs serve
```

**Deploy**:
```bash
mkdocs gh-deploy
```

**Complete Guide**: [`GITHUB_PAGES_GUIDE.md`](GITHUB_PAGES_GUIDE.md)
- Setup instructions
- Configuration
- Custom domain
- Troubleshooting
- Automated deployment with GitHub Actions

## 🔄 Keeping the Paper Updated

### Automated Paper Discovery

```bash
# Find new papers (last 7 days)
python scripts/search_new_papers.py

# Longer timeframe
python scripts/search_new_papers.py --days 14

# Review results
cat new_papers.md
```

### Update Rules

See [`PAPER_UPDATE_RULES.md`](PAPER_UPDATE_RULES.md) for complete guidelines on:

**Academic Standards**:
- ✅ Tier 1: NeurIPS, ICML, ICLR, ACL, Nature, Science
- ✅ Tier 2: AAMAS, CoRL, IEEE Access, Information Fusion
- ✅ Tier 3: Workshops at top venues, major lab tech reports
- ❌ Non-peer-reviewed sources

**Discovery Process**:
- Weekly automated searches
- Monthly deep reviews
- Quarterly major updates
- Citation tracking

**Integration Workflow**:
1. Search → 2. Screen → 3. Review → 4. Integrate → 5. Deploy

**Quality Control**:
- Peer-review requirement
- Recent (< 3 years)
- Proper citations
- Section fit
- Value addition

## 📦 Research Papers Collection

Recently added 5 high-quality research papers (converted from PDF):

1. **Agentic AI Needs a Systems Theory** (IBM Research, 2025)
2. **Agentic AI: Autonomous Intelligence** (IEEE Access, 2025)
3. **Agentic AI Systems: Opportunities** (IEEE EIT, 2025)
4. **AI Agents vs. Agentic AI** (Information Fusion, 2026)
5. **The Rise of Agentic AI** (Future Internet, 2025)

**Summary**: [`papers/PAPERS_SUMMARY.md`](papers/PAPERS_SUMMARY.md)  
**Integration**: [`papers/INTEGRATION_GUIDE.md`](papers/INTEGRATION_GUIDE.md)

## 🛠️ Development

### Prerequisites

```bash
# For paper compilation
sudo apt-get install texlive-full

# For documentation
pip install -r requirements.txt

# For paper search
pip install requests
```

### Common Commands

See [`QUICK_REFERENCE.md`](QUICK_REFERENCE.md) for complete list.

**Paper**:
```bash
cd arxiv-paper
make          # Compile
make view     # Open PDF
make clean    # Clean files
make wordcount # Count words
```

**Documentation**:
```bash
mkdocs serve      # Local preview
mkdocs build      # Build site
mkdocs gh-deploy  # Deploy to GitHub Pages
```

**Paper Discovery**:
```bash
python scripts/search_new_papers.py  # Search new papers
cat new_papers.md                     # Review results
```

## 📊 Project Statistics

- **Total References**: 104 peer-reviewed sources
- **Research Papers**: 5 (converted and analyzed)
- **Code Examples**: 15+ complete implementations
- **Documentation Pages**: 60+ topics covered
- **Lines of LaTeX**: ~3,000
- **Repository Size**: ~20 MB

## 🔬 Key Topics Covered

### Theoretical Foundations
- Agency and autonomy definitions
- Functional agency framework
- Cognitive architectures
- System design principles
- Multi-agent systems theory

### Implementation
- LangChain, LangGraph, Pydantic AI, DSPy
- ReAct, Reflection, and Planning patterns
- State management and memory systems
- Tool integration and function calling
- Multi-agent coordination

### Practical Applications
- Customer service automation
- Software development assistance
- Research and scientific discovery
- Healthcare and finance applications
- Robotic coordination

### Production Considerations
- Monitoring and observability
- Safety and guardrails
- Trustworthiness frameworks
- Testing strategies
- Scalability patterns

## 🤝 Contributing

Contributions welcome! Areas for contribution:

1. **Add Papers**: Submit relevant research papers
2. **Improve Documentation**: Enhance explanations
3. **Share Use Cases**: Document applications
4. **Report Issues**: Bug reports and suggestions
5. **Code Examples**: Practical implementations

**Process**:
1. Fork repository
2. Create feature branch
3. Make changes
4. Submit pull request
5. Follow academic standards in [`PAPER_UPDATE_RULES.md`](PAPER_UPDATE_RULES.md)

## 📖 Citation

If you use this work in your research:

```bibtex
@article{memari2025agentic,
  title={Agentic AI Systems: A Comprehensive Framework for Building Autonomous Intelligent Agents},
  author={Memari, Majid},
  journal={arXiv preprint arXiv:XXXX.XXXXX},
  year={2025},
  institution={Utah Valley University}
}
```

## 📧 Contact

**Author**: Majid Memari  
**Institution**: Utah Valley University  
**Email**: mmemari@uvu.edu  
**ORCID**: 0000-0001-5654-4996

## 📜 License

MIT License - See LICENSE file for details

## 🗂️ Documentation Index

- **[START-HERE.md](START-HERE.md)** - Quick start guide ⭐
- **[GITHUB_PAGES_GUIDE.md](GITHUB_PAGES_GUIDE.md)** - Complete GitHub Pages setup
- **[PAPER_UPDATE_RULES.md](PAPER_UPDATE_RULES.md)** - Academic standards & workflows  
- **[QUICK_REFERENCE.md](QUICK_REFERENCE.md)** - Common commands
- **[ORGANIZATION.md](ORGANIZATION.md)** - Repository structure
- **[STRUCTURE_VISUAL.md](STRUCTURE_VISUAL.md)** - Visual directory tree

## 🎯 Quick Links

| Resource | Link |
|----------|------|
| **Paper PDF** | [arxiv-paper/paper.pdf](arxiv-paper/paper.pdf) |
| **Documentation** | https://YOUR-USERNAME.github.io/Agentic-AI-Systems/ |
| **Paper Summaries** | [papers/PAPERS_SUMMARY.md](papers/PAPERS_SUMMARY.md) |
| **Integration Guide** | [papers/INTEGRATION_GUIDE.md](papers/INTEGRATION_GUIDE.md) |
| **GitHub Pages Guide** | [GITHUB_PAGES_GUIDE.md](GITHUB_PAGES_GUIDE.md) |
| **Update Rules** | [PAPER_UPDATE_RULES.md](PAPER_UPDATE_RULES.md) |

## 🙏 Acknowledgments

- Utah Valley University for supporting this research
- The open-source AI community for frameworks and tools
- All authors of referenced papers and research
- Contributors to documentation and examples

---

**Last Updated**: November 15, 2025  
**Version**: 2.0 (Organized & Production-Ready)  
**Status**: Active Development

**Next Steps**: See [START-HERE.md](START-HERE.md) to begin!
