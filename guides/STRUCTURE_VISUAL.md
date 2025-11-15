# Repository Structure Visualization

## 🌳 Complete Directory Tree

```
Agentic-AI-Systems/
│
├── 📋 Core Documentation
│   ├── README.md                    ⭐ Start here
│   ├── ORGANIZATION.md              📚 This structure guide
│   ├── PDF_CONVERSION_SUMMARY.md    📊 Latest work (Nov 2025)
│   ├── SECURITY.md                  🔒 Security policies
│   └── CITATION.cff                 📖 Citation metadata
│
├── ⚙️ Configuration
│   ├── mkdocs.yml                   🔧 Documentation config
│   └── requirements.txt             📦 Python dependencies
│
├── 📝 arXiv Paper (Review Paper)
│   └── arxiv-paper/
│       ├── paper.tex                📄 LaTeX source (43 pages)
│       ├── paper.pdf                📕 Compiled PDF
│       ├── references.bib           📚 104 references
│       ├── arxiv.sty                🎨 arXiv style
│       ├── abstract.txt             📝 Standalone abstract
│       ├── Makefile                 🔨 Build automation
│       ├── submission-checklist.md  ✅ Submission guide
│       └── README.md                📖 Paper docs
│
├── 📚 Research Papers Collection
│   └── papers/
│       ├── Paper 1.pdf              🔬 IBM Research (Systems Theory)
│       ├── Paper 2.pdf              🔬 IEEE Access (Survey)
│       ├── Paper 3.pdf              🔬 IEEE EIT (Trustworthiness)
│       ├── Paper 4.pdf              🔬 Info Fusion (Taxonomy)
│       ├── Paper 5.pdf              🔬 Future Internet (Review)
│       ├── PAPERS_SUMMARY.md        📊 Key findings
│       ├── INTEGRATION_GUIDE.md     🎯 Integration instructions
│       └── README.md                📖 Papers docs
│
├── 📖 Documentation Source
│   └── docs/
│       ├── index.md                 🏠 Landing page
│       ├── arxiv-paper/             📄 Paper pages
│       │   ├── index.md
│       │   ├── overview.md
│       │   └── citation.md
│       ├── javascripts/             🔧 Custom JS
│       │   └── mathjax.js
│       └── stylesheets/             🎨 Custom CSS
│           └── extra.css
│
├── 🌐 Built Site (GitHub Pages)
│   └── site/
│       ├── index.html               🏠 Home page
│       ├── arxiv-paper/             📄 Paper section
│       ├── assets/                  🎨 Static assets
│       ├── javascripts/             📜 Bundled JS
│       ├── stylesheets/             🎨 Compiled CSS
│       ├── search/                  🔍 Search index
│       └── sitemap.xml              🗺️ Site map
│
├── 🖼️ Assets
│   └── assets/
│       └── banner.png               🎨 Repository banner
│
├── 🤖 Scripts
│   └── scripts/
│       ├── update_agent.py          🔄 Automation
│       ├── test_update_agent.py     🧪 Tests
│       └── README.md                📖 Scripts docs
│
├── 🔧 GitHub Configuration
│   └── .github/
│       └── README.md                📖 GitHub docs
│
└── 📦 Archive (Historical)
    └── .archive/
        ├── setup-docs/              📜 Setup guides (10+ files)
        │   ├── SETUP-COMPLETE.md
        │   ├── GITHUB-PAGES-SETUP.md
        │   ├── AUTOMATION-GUIDE.md
        │   └── ...
        └── arxiv-status/             📜 Paper status (12+ files)
            ├── BIBLIOGRAPHY-UPDATE.md
            ├── COMPLETE-STATUS.md
            └── ...
```

## 📊 Size Overview

```
Total: ~20 MB
├── papers/        13.0 MB  (5 PDF research papers)
├── site/          ~5.0 MB  (Built documentation)
├── arxiv-paper/   628 KB   (LaTeX + PDF)
├── docs/          380 KB   (Documentation source)
├── .archive/      ~500 KB  (Historical files)
└── Other          ~200 KB  (Config, scripts, assets)
```

## 🎯 Quick Navigation

### I want to...

**→ Read the review paper**
```
📍 arxiv-paper/paper.pdf
```

**→ Build the paper**
```bash
cd arxiv-paper && make
```

**→ See extracted research insights**
```
📍 papers/PAPERS_SUMMARY.md
```

**→ Integrate new research into paper**
```
📍 papers/INTEGRATION_GUIDE.md
```

**→ Understand repository structure**
```
📍 ORGANIZATION.md (detailed)
📍 STRUCTURE_VISUAL.md (this file - visual)
```

**→ View the documentation website**
```
🌐 https://memari-majid.github.io/Agentic-AI-Systems/
```

**→ Build documentation locally**
```bash
mkdocs serve
```

**→ Find old setup guides**
```
📍 .archive/setup-docs/
```

**→ See paper development history**
```
📍 .archive/arxiv-status/
```

## 📁 File Type Distribution

```
Document Types:
├── 📄 Markdown (.md)      30+ files
├── 📕 PDF (.pdf)          6 files (1 paper + 5 research)
├── 📝 LaTeX (.tex)        1 file (paper source)
├── 📚 BibTeX (.bib)       1 file (104 references)
├── 🐍 Python (.py)        2 files (scripts)
├── ⚙️ YAML (.yml)         1 file (config)
├── 🎨 CSS (.css)          Multiple (docs)
├── 📜 JavaScript (.js)    Multiple (docs)
└── 🌐 HTML (.html)        Multiple (site/)
```

## 🔄 Typical Workflows

### 1. Paper Development Workflow
```
Edit paper.tex
     ↓
Add/update references.bib
     ↓
make (compile)
     ↓
View paper.pdf
     ↓
Commit changes
```

### 2. Research Integration Workflow
```
Add PDF to papers/
     ↓
Extract key info → PAPERS_SUMMARY.md
     ↓
Create integration notes → INTEGRATION_GUIDE.md
     ↓
Add BibTeX → references.bib
     ↓
Integrate into paper.tex
```

### 3. Documentation Update Workflow
```
Edit docs/*.md
     ↓
mkdocs serve (preview)
     ↓
mkdocs build (generate site/)
     ↓
Commit changes
     ↓
GitHub Pages auto-deploys
```

## 🎨 Directory Colors Legend

- 📋 Core Documentation (Essential reading)
- ⚙️ Configuration (Setup files)
- 📝 Paper Content (LaTeX source)
- 📚 Research (PDF papers)
- 📖 Documentation (MkDocs source)
- 🌐 Website (Built site)
- 🖼️ Media (Images, assets)
- 🤖 Automation (Scripts)
- 🔧 GitHub (Git config)
- 📦 Archive (Historical)

## 📈 Content Statistics

### Paper Statistics
- **Pages**: 43
- **Words**: ~21,000
- **References**: 104
- **Sections**: 11
- **Code Examples**: 15
- **Tables**: 4

### Research Papers
- **Total Papers**: 5
- **Total Pages**: ~150
- **Publication Years**: 2025-2026
- **Publishers**: IBM, IEEE, Elsevier, MDPI
- **Key Concepts Extracted**: 50+

### Documentation
- **Markdown Files**: 30+
- **HTML Pages**: 60+
- **Topics Covered**: Complete agentic AI framework

## 🗂️ Organization Principles

1. **Clarity**: Each directory has clear purpose
2. **Hierarchy**: Logical nesting of related content
3. **Documentation**: README.md in each major directory
4. **Separation**: Source vs. built content separated
5. **Archive**: Historical files preserved but separated
6. **Minimal Root**: Only essential files at top level

## ✨ Recent Changes (Nov 2025)

### Added
- ✅ 5 research papers (PDF)
- ✅ PAPERS_SUMMARY.md
- ✅ INTEGRATION_GUIDE.md
- ✅ 5 new BibTeX entries
- ✅ ORGANIZATION.md
- ✅ STRUCTURE_VISUAL.md

### Organized
- ✅ Moved old setup docs to .archive/setup-docs/
- ✅ Moved paper status files to .archive/arxiv-status/
- ✅ Updated main README.md
- ✅ Updated arxiv-paper/README.md
- ✅ Cleaned root directory

### Improved
- ✅ Clear navigation
- ✅ Better documentation
- ✅ Logical structure
- ✅ Easy to find files

## 🎯 Next Steps

1. **Use the papers**: Follow INTEGRATION_GUIDE.md
2. **Update paper**: Integrate new research
3. **Compile**: Run `make` in arxiv-paper/
4. **Submit**: Follow submission-checklist.md
5. **Share**: GitHub Pages auto-deployed

## 📧 Need Help?

**Finding Files?**
- Check this visual guide
- See ORGANIZATION.md for details
- Look in directory READMEs

**Working with Paper?**
- See arxiv-paper/README.md
- Run `make help` for build commands

**Integrating Research?**
- See papers/INTEGRATION_GUIDE.md
- Check papers/PAPERS_SUMMARY.md

---

**Last Updated**: November 15, 2025  
**Version**: 2.0 (Clean & Organized)  
**Status**: ✅ Repository Organized

