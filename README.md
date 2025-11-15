# Agentic AI Systems

A comprehensive review paper and research repository on Agentic AI systems, covering theoretical foundations, implementation frameworks, and practical applications.

[![Documentation](https://img.shields.io/badge/docs-latest-blue.svg)](https://memari-majid.github.io/Agentic-AI-Systems/)
[![arXiv Paper](https://img.shields.io/badge/arXiv-paper-red.svg)](arxiv-paper/paper.pdf)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 🌐 Live Resources

- **📖 Documentation**: https://memari-majid.github.io/Agentic-AI-Systems/
- **📄 Review Paper**: [43-page PDF](arxiv-paper/paper.pdf) (104 peer-reviewed references)
- **🔗 Repository**: https://github.com/memari-majid/Agentic-AI-Systems

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

**New here?** → Read [`START-HERE.md`](START-HERE.md)

---

## 📚 What's Included

### Review Paper (43 pages)
- **104 peer-reviewed references** from NeurIPS, ICML, Nature, IEEE, etc.
- **15 code examples** (LangChain, LangGraph, Pydantic AI, DSPy)
- **Covers**: Theory, implementation, multi-agent systems, RAG, production deployment
- **Status**: Ready for arXiv submission

### Research Papers (5)
1. Agentic AI Needs a Systems Theory (IBM Research, 2025)
2. Agentic AI: Autonomous Intelligence (IEEE Access, 2025)
3. Agentic AI Systems: Opportunities (IEEE EIT, 2025)
4. AI Agents vs. Agentic AI (Information Fusion, 2026)
5. The Rise of Agentic AI (Future Internet, 2025)

See [`papers/PAPERS_SUMMARY.md`](papers/PAPERS_SUMMARY.md) for extracted insights.

### Documentation & Guides
- **[GITHUB_PAGES_GUIDE.md](GITHUB_PAGES_GUIDE.md)** - Run and deploy documentation
- **[PAPER_UPDATE_RULES.md](PAPER_UPDATE_RULES.md)** - Keep review current (academic standards)
- **[QUICK_REFERENCE.md](QUICK_REFERENCE.md)** - Common commands
- **[papers/INTEGRATION_GUIDE.md](papers/INTEGRATION_GUIDE.md)** - LaTeX integration snippets

### Automation
- **search_new_papers.py** - Automated paper discovery from arXiv & Semantic Scholar
- **Academic filtering** - Only peer-reviewed sources (Tier 1-3 venues)
- **Update workflows** - Weekly, monthly, quarterly routines

---

## 📖 Repository Structure

```
Agentic-AI-Systems/
├── arxiv-paper/          # Review paper (LaTeX + PDF)
├── papers/               # 5 research papers + summaries
├── docs/                 # Documentation source
├── site/                 # Built website (GitHub Pages)
├── scripts/              # Automation (paper search, etc.)
├── GITHUB_PAGES_GUIDE.md # Deployment guide
├── PAPER_UPDATE_RULES.md # Academic standards
└── QUICK_REFERENCE.md    # Command cheat sheet
```

See [`ORGANIZATION.md`](ORGANIZATION.md) for complete structure.

---

## 🎯 Main Topics Covered

- Agency and autonomy in AI systems
- LangChain, LangGraph, Pydantic AI, DSPy frameworks
- Multi-agent coordination patterns
- RAG vs Fine-Tuning decision framework
- Production deployment (monitoring, safety, testing)
- Strategic considerations and ethics

---

## 🔄 Keeping Updated

### Find New Papers
```bash
python scripts/search_new_papers.py
```

### Academic Standards
- **Tier 1**: NeurIPS, ICML, ICLR, ACL, Nature, Science
- **Tier 2**: AAMAS, IEEE Access, Information Fusion
- **Tier 3**: Top workshops, major lab reports
- **Only peer-reviewed sources**

Full guidelines: [`PAPER_UPDATE_RULES.md`](PAPER_UPDATE_RULES.md)

---

## 📧 Contact

**Majid Memari**  
Department of Computer Science, Utah Valley University  
📧 mmemari@uvu.edu | 🔗 [ORCID: 0000-0001-5654-4996](https://orcid.org/0000-0001-5654-4996)

---

## 📖 Citation

```bibtex
@article{memari2025agentic,
  title={Agentic AI Systems: A Comprehensive Framework for Building Autonomous Intelligent Agents},
  author={Memari, Majid},
  journal={arXiv preprint arXiv:XXXX.XXXXX},
  year={2025},
  institution={Utah Valley University}
}
```

---

## 📜 License

MIT License - See [LICENSE](LICENSE) file for details.

---

**Last Updated**: November 15, 2025 | **Status**: Published & Live 🚀
