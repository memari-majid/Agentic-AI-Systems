# Repository Organization

This document describes the complete organization of the Agentic AI Systems repository.

## 📁 Directory Structure

```
Agentic-AI-Systems/
│
├── 📄 README.md                    # Main repository documentation
├── 📄 PDF_CONVERSION_SUMMARY.md    # Latest PDF conversion summary
├── 📄 ORGANIZATION.md              # This file
├── 📄 SECURITY.md                  # Security policies
├── 📄 CITATION.cff                 # Citation metadata
├── 📄 requirements.txt             # Python dependencies
├── 📄 mkdocs.yml                   # Documentation configuration
│
├── 📂 arxiv-paper/                 # Review Paper (LaTeX)
│   ├── paper.tex                   # Main LaTeX source
│   ├── paper.pdf                   # Compiled PDF (43 pages)
│   ├── references.bib              # Bibliography (104 references)
│   ├── arxiv.sty                   # arXiv style file
│   ├── abstract.txt                # Standalone abstract
│   ├── Makefile                    # Build automation
│   ├── submission-checklist.md     # Submission guide
│   └── README.md                   # Paper documentation
│
├── 📂 papers/                      # Research Papers Collection
│   ├── *.pdf                       # 5 research papers (PDF format)
│   ├── PAPERS_SUMMARY.md           # Key findings from all papers
│   ├── INTEGRATION_GUIDE.md        # Integration instructions
│   └── README.md                   # Papers documentation
│
├── 📂 docs/                        # Documentation Source (MkDocs)
│   ├── index.md                    # Landing page
│   ├── arxiv-paper/                # Paper documentation pages
│   │   ├── index.md
│   │   ├── overview.md
│   │   └── citation.md
│   ├── javascripts/                # Custom JavaScript
│   │   └── mathjax.js              # Math rendering
│   └── stylesheets/                # Custom CSS
│       └── extra.css
│
├── 📂 site/                        # Built Documentation (GitHub Pages)
│   ├── index.html                  # Generated static site
│   ├── arxiv-paper/                # Paper pages
│   ├── assets/                     # Bundled assets
│   ├── javascripts/                # Compiled JS
│   ├── stylesheets/                # Compiled CSS
│   ├── search/                     # Search index
│   └── sitemap.xml                 # Site map
│
├── 📂 assets/                      # Static Assets
│   └── banner.png                  # Repository banner
│
├── 📂 scripts/                     # Automation Scripts
│   ├── update_agent.py             # Agent update automation
│   ├── test_update_agent.py        # Tests for automation
│   └── README.md                   # Scripts documentation
│
├── 📂 .github/                     # GitHub Configuration
│   ├── workflows/                  # GitHub Actions (if any)
│   └── README.md                   # GitHub-specific docs
│
└── 📂 .archive/                    # Archived Documentation
    ├── setup-docs/                 # Setup and deployment guides
    │   ├── SETUP-COMPLETE.md
    │   ├── GITHUB-PAGES-SETUP.md
    │   ├── AUTOMATION-GUIDE.md
    │   ├── DEPLOY-NOW.md
    │   ├── QUICK-START.md
    │   └── ...
    └── arxiv-status/                # Paper development status files
        ├── BIBLIOGRAPHY-UPDATE.md
        ├── COMPLETE-STATUS.md
        ├── CREATION-SUMMARY.md
        ├── FINAL-CHANGES.md
        ├── FINAL-PAPER-STATUS.md
        └── ...
```

## 📋 File Categories

### Core Documentation
- **README.md** - Main entry point with overview and quick start
- **ORGANIZATION.md** - This file, complete structure documentation
- **PDF_CONVERSION_SUMMARY.md** - Latest work summary (Nov 2025)
- **SECURITY.md** - Security policies and guidelines
- **CITATION.cff** - Citation metadata for the repository

### Configuration Files
- **mkdocs.yml** - MkDocs configuration for documentation site
- **requirements.txt** - Python dependencies for documentation
- **.gitignore** - Git ignore rules

### arXiv Paper (`arxiv-paper/`)
**Purpose**: Complete LaTeX source and PDF for the review paper

**Key Files**:
- `paper.tex` - Main document (43 pages, 21,000 words)
- `paper.pdf` - Compiled PDF
- `references.bib` - 104 references
- `Makefile` - Build commands
- `README.md` - Paper-specific documentation

**Usage**: 
```bash
cd arxiv-paper
make          # Compile paper
make view     # Open PDF
make clean    # Remove aux files
```

### Research Papers (`papers/`)
**Purpose**: Collection of 5 converted research papers with analysis

**Key Files**:
- 5 PDF files - Original research papers
- `PAPERS_SUMMARY.md` - 50+ key concepts extracted
- `INTEGRATION_GUIDE.md` - LaTeX snippets for paper integration
- `README.md` - Papers documentation

**Statistics**:
- Total size: ~13 MB
- Papers from: IBM, IEEE, Elsevier, MDPI
- Publication years: 2025-2026
- Combined content: 150+ pages

### Documentation (`docs/`)
**Purpose**: MkDocs source files for GitHub Pages

**Structure**:
- Markdown files for content
- Custom JavaScript (MathJax)
- Custom CSS for styling
- Paper overview pages

**Build**: 
```bash
mkdocs serve   # Local preview
mkdocs build   # Generate site/
```

### Built Site (`site/`)
**Purpose**: Static site generated by MkDocs

**Contents**:
- HTML files
- Bundled JavaScript
- Compiled CSS
- Search index
- Assets and media

**Deployment**: Automatically deployed to GitHub Pages

### Scripts (`scripts/`)
**Purpose**: Automation and utility scripts

**Files**:
- `update_agent.py` - Agent update automation
- `test_update_agent.py` - Test suite
- `README.md` - Script documentation

### Archive (`.archive/`)
**Purpose**: Historical documentation and status files

**Categories**:
1. **setup-docs/** - Setup and deployment guides
   - GitHub Pages setup
   - Automation guides
   - Quick start guides
   - Deployment instructions

2. **arxiv-status/** - Paper development status
   - Bibliography updates
   - Completion status
   - Restructuring summaries
   - Final changes

**Why Archived**: These files document the development process but are not needed for active use. They're preserved for historical reference.

## 🎯 Common Tasks

### Working with the Paper

```bash
# Navigate to paper directory
cd arxiv-paper

# Build paper
make

# View paper
make view

# Clean build files
make clean
```

### Working with Research Papers

```bash
# Navigate to papers directory
cd papers

# View summaries
cat PAPERS_SUMMARY.md

# Get integration instructions
cat INTEGRATION_GUIDE.md
```

### Working with Documentation

```bash
# Serve documentation locally
mkdocs serve

# Build static site
mkdocs build

# Deploy to GitHub Pages (if configured)
mkdocs gh-deploy
```

### Finding Information

| What You Need | Where to Look |
|---------------|---------------|
| Paper overview | `arxiv-paper/README.md` |
| Research papers summary | `papers/PAPERS_SUMMARY.md` |
| Integration guide | `papers/INTEGRATION_GUIDE.md` |
| Repository structure | `ORGANIZATION.md` (this file) |
| Latest work summary | `PDF_CONVERSION_SUMMARY.md` |
| Setup guides | `.archive/setup-docs/` |
| Development history | `.archive/arxiv-status/` |

## 📊 Size Breakdown

| Directory | Size | Description |
|-----------|------|-------------|
| `papers/` | 13 MB | 5 PDF research papers |
| `site/` | ~5 MB | Built documentation |
| `arxiv-paper/` | 628 KB | LaTeX source + PDF |
| `docs/` | 380 KB | Documentation source |
| `.archive/` | ~500 KB | Historical docs |
| Other | ~200 KB | Config, scripts, assets |
| **Total** | ~20 MB | Complete repository |

## 🗂️ File Types

- **Markdown (.md)**: 30+ files for documentation
- **LaTeX (.tex)**: Paper source
- **BibTeX (.bib)**: Bibliography
- **PDF (.pdf)**: Paper and research papers
- **Python (.py)**: Automation scripts
- **YAML (.yml)**: Configuration
- **HTML/CSS/JS**: Built documentation

## 🔄 Workflow

### For Paper Development
1. Edit `arxiv-paper/paper.tex`
2. Update `arxiv-paper/references.bib` if needed
3. Run `make` to compile
4. Review `paper.pdf`
5. Commit changes

### For Adding Research Papers
1. Place PDF in `papers/`
2. Update `papers/PAPERS_SUMMARY.md`
3. Add BibTeX entry to `arxiv-paper/references.bib`
4. Create integration notes if needed

### For Documentation Updates
1. Edit files in `docs/`
2. Run `mkdocs serve` to preview
3. Commit changes
4. GitHub Pages auto-deploys from `site/`

## 🧹 Maintenance

### Regular Cleanup
```bash
# Remove LaTeX auxiliary files
cd arxiv-paper && make clean

# Remove Python cache
find . -type d -name __pycache__ -exec rm -rf {} +

# Remove MkDocs build artifacts (if rebuilding)
rm -rf site/
```

### Archive Old Files
When files are no longer needed for active development but should be preserved:
```bash
# Move to appropriate archive directory
mv OLD_FILE.md .archive/setup-docs/
```

## 📚 Documentation Hierarchy

```
Main README.md
├── ORGANIZATION.md (this file)
├── PDF_CONVERSION_SUMMARY.md
├── arxiv-paper/README.md
│   └── Detailed paper information
├── papers/README.md
│   ├── PAPERS_SUMMARY.md
│   └── INTEGRATION_GUIDE.md
├── scripts/README.md
└── .archive/
    ├── setup-docs/ (historical)
    └── arxiv-status/ (historical)
```

## 🎓 Best Practices

1. **Keep root clean**: Only essential files at root level
2. **Use READMEs**: Each directory has its own README
3. **Archive history**: Move old status files to `.archive/`
4. **Document changes**: Update relevant READMEs
5. **Clear naming**: Use descriptive file names
6. **Consistent structure**: Follow the established pattern

## 📧 Questions?

If you need to understand the repository structure or locate specific files, refer to:
1. This file (ORGANIZATION.md) for structure
2. Individual README.md files in each directory
3. PDF_CONVERSION_SUMMARY.md for latest work

---

**Last Updated**: November 15, 2025  
**Maintained By**: Majid Memari  
**Version**: 2.0 (Post-Organization)

