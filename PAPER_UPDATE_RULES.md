# Review Paper Update Rules & Guidelines

Comprehensive rules for maintaining and updating the Agentic AI Systems review paper with academic rigor.

## 🎯 Core Principles

### Academic Standards
1. **Peer-Reviewed Sources Only**: All new references must be peer-reviewed
2. **Recent & Relevant**: Prioritize papers from last 3 years (2022+)
3. **High-Impact Venues**: Focus on top-tier conferences and journals
4. **Proper Citation**: Every claim must be backed by references
5. **No Preprints Only**: arXiv/preprints acceptable only if highly relevant and recent

---

## 📚 Source Quality Requirements

### Acceptable Sources

#### Tier 1: Premier Venues (Highest Priority)
**Conferences**:
- NeurIPS, ICML, ICLR (Machine Learning)
- ACL, EMNLP, NAACL (NLP)
- AAAI, IJCAI (AI)
- CVPR, ICCV, ECCV (Computer Vision)
- CHI, UIST (HCI)

**Journals**:
- Nature, Science (multidisciplinary)
- IEEE TPAMI, JMLR (ML/AI)
- ACM TIST, JAIR (AI)
- ACM Computing Surveys (reviews)
- IEEE Access (open access)

#### Tier 2: Strong Venues
**Conferences**:
- AAMAS (Multi-agent systems)
- CoRL, ICRA, IROS (Robotics)
- WWW, KDD (Web/Data)
- SIGCHI, IUI (Interaction)

**Journals**:
- Information Fusion
- Future Internet
- AI Magazine
- IEEE Intelligent Systems

#### Tier 3: Acceptable if Recent & Relevant
- Workshop papers at Tier 1 conferences
- arXiv preprints (if cited by others)
- Technical reports from major labs (OpenAI, DeepMind, Google, etc.)

### Unacceptable Sources
- ❌ Non-peer-reviewed blogs
- ❌ Medium articles
- ❌ Company marketing materials
- ❌ Wikipedia
- ❌ Personal websites
- ❌ Uncited preprints older than 6 months
- ❌ Papers with obvious quality issues

---

## 🔍 Paper Discovery Process

### 1. Systematic Search

#### Search Engines
```
Primary:
- Google Scholar (https://scholar.google.com/)
- Semantic Scholar (https://www.semanticscholar.org/)
- arXiv (https://arxiv.org/)
- IEEE Xplore (https://ieeexplore.ieee.org/)
- ACM Digital Library (https://dl.acm.org/)

Secondary:
- Papers With Code (https://paperswithcode.com/)
- Connected Papers (https://www.connectedpapers.com/)
- ResearchGate (for full texts)
```

#### Search Strategy

**Step 1: Core Keywords**
```
Base terms: "agentic AI" OR "autonomous agents" OR "AI agents"

Combined with:
- "large language models"
- "multi-agent systems"
- "tool use"
- "reasoning"
- "planning"
- "memory systems"
```

**Step 2: Specific Topics**
```
For each section of the paper, search:
- Perception: "multimodal perception" + "agents"
- Memory: "agent memory" OR "episodic memory AI"
- Reasoning: "chain-of-thought" OR "ReAct" OR "tree-of-thoughts"
- Action: "tool use LLM" OR "function calling"
- Coordination: "multi-agent coordination" OR "agent collaboration"
```

**Step 3: Citation Tracking**
```
Forward citations: "Papers citing this work"
Backward citations: "References in this paper"
Related work: "Similar papers" suggestions
```

### 2. Quality Screening

#### Initial Filter (30 seconds per paper)
- [ ] Published in acceptable venue?
- [ ] Recent enough (2020+, prefer 2022+)?
- [ ] Title/abstract relevant?
- [ ] Cited by others (at least 3+ citations for papers >6 months old)?

#### Detailed Review (5-10 minutes per paper)
- [ ] Read abstract carefully
- [ ] Skim introduction and conclusion
- [ ] Check methodology
- [ ] Verify novelty and contribution
- [ ] Assess writing quality
- [ ] Check for reproducibility claims

#### Deep Read (30-60 minutes per paper)
- [ ] Read full paper
- [ ] Understand core contributions
- [ ] Identify integration points with review paper
- [ ] Extract key quotes/findings
- [ ] Note limitations

### 3. Documentation

For each paper considered, create entry:

```markdown
## Paper Title
- **Authors**: First Author et al.
- **Venue**: Conference/Journal, Year
- **Citations**: [Number] (as of [Date])
- **DOI**: [DOI link]
- **Status**: ✅ Accepted / ⏳ Under Review / ❌ Rejected

### Summary
[2-3 sentence summary]

### Key Contributions
1. Contribution 1
2. Contribution 2

### Relevant to Sections
- Section X: [How it relates]
- Section Y: [How it relates]

### Integration Notes
[Specific ideas for integration]

### BibTeX
```bibtex
@article{...}
```
```

---

## 📝 Integration Rules

### When to Add a Paper

Add paper if it:
1. **Fills a gap**: Addresses topic not well-covered
2. **Updates knowledge**: More recent work on existing topic
3. **Provides evidence**: Empirical results supporting claims
4. **Contradicts**: Offers alternative perspective worth discussing
5. **Seminal work**: Foundational paper that must be cited

### Where to Integrate

#### Section-Specific Guidelines

**Section 2 (Related Work)**
- Add seminal papers
- Recent comprehensive surveys
- Key frameworks and tools
- Foundational concepts

**Section 3 (Theoretical Foundations)**
- Papers defining agency/autonomy
- Cognitive architecture papers
- Theoretical frameworks

**Section 4 (Architectural Components)**
- Papers on perception systems
- Memory architectures
- Reasoning methods
- Action/tool use

**Section 5 (Implementation)**
- Framework papers (LangChain, etc.)
- Implementation patterns
- System design papers

**Section 6 (Multi-Agent)**
- Coordination mechanisms
- Communication protocols
- Multi-agent learning

**Section 7 (Knowledge Integration)**
- RAG papers
- Fine-tuning methods
- Hybrid approaches

**Section 8 (Production)**
- Monitoring systems
- Safety mechanisms
- Evaluation methods

**Section 9 (Strategic)**
- Adoption studies
- Use cases
- Impact analyses

**Section 10 (Ethics)**
- Bias/fairness papers
- Privacy/security
- Governance frameworks

### How to Integrate

#### Step 1: Read Integration Guide
```bash
cat papers/INTEGRATION_GUIDE.md
```

#### Step 2: Prepare Content

**Format**:
```latex
Recent work by \citet{author2025paper} demonstrates [key finding]. 
Their approach to [specific aspect] shows [result], which [significance]. 
This builds on earlier work \cite{earlier2024} while addressing [limitation].

Key contributions include:
\begin{itemize}
    \item Contribution 1
    \item Contribution 2  
    \item Contribution 3
\end{itemize}

These findings suggest [implication for agentic AI].
```

#### Step 3: Add to references.bib

```bibtex
@article{author2025paper,
  title={Paper Title},
  author={Author, First and Author, Second},
  journal={Journal Name},
  volume={X},
  number={Y},
  pages={ZZ--ZZ},
  year={2025},
  publisher={Publisher},
  doi={10.xxxx/xxxxx},
  url={https://...},
  note={Brief note if needed}
}
```

#### Step 4: Integrate Text

```bash
# Edit paper
nano arxiv-paper/paper.tex

# Add content to appropriate section
# Use \cite{} or \citet{} for citations

# Build to check
cd arxiv-paper && make

# Review PDF
make view
```

#### Step 5: Update Documentation

```bash
# Update papers summary
nano papers/PAPERS_SUMMARY.md

# Add integration notes
nano papers/INTEGRATION_GUIDE.md
```

---

## 🔄 Update Frequency

### Continuous Monitoring (Recommended)

**Weekly** (30 minutes):
- Check Google Scholar alerts
- Scan arXiv for new papers
- Review Twitter/X for paper announcements
- Check Papers With Code trending

**Monthly** (2 hours):
- Deep search for new papers
- Review citations to our key references
- Check for papers in upcoming conferences
- Update integration queue

**Quarterly** (4 hours):
- Major review of all sections
- Identify gaps in coverage
- Plan major updates
- Integrate queued papers

### Batch Updates

**Minor Update** (Add 1-3 papers):
- Time: 2-4 hours
- Process: Find → Read → Integrate → Test
- Trigger: Significant new paper in area

**Major Update** (Add 5-10 papers):
- Time: 1-2 days
- Process: Systematic search → Screen → Integrate → Revise
- Trigger: Quarterly review or major development

**Revision** (10+ papers, restructure):
- Time: 1 week
- Process: Full review → Reorganize → Rewrite sections
- Trigger: Annual update or paradigm shift

---

## 📊 Quality Control Checklist

### Before Adding Paper

- [ ] Paper is peer-reviewed (or exceptional preprint)
- [ ] Venue is reputable (Tier 1-3)
- [ ] Paper is recent (< 3 years old)
- [ ] Paper has clear contributions
- [ ] Paper is relevant to review scope
- [ ] Paper adds value (not redundant)
- [ ] Full text is available
- [ ] BibTeX information is complete

### During Integration

- [ ] Content is paraphrased (not copied)
- [ ] Citations are accurate
- [ ] Contribution is clear
- [ ] Fits section theme
- [ ] Links to other sections if relevant
- [ ] Does not contradict existing content (or notes contradiction)
- [ ] Adds insight, not just citation count

### After Integration

- [ ] LaTeX compiles successfully
- [ ] Citation renders correctly
- [ ] No orphaned references
- [ ] Section flow is maintained
- [ ] Word count is reasonable
- [ ] PDF looks professional
- [ ] All cross-references work

---

## 🤖 Automated Update System (Optional)

### GitHub Actions Workflow

Create `.github/workflows/paper-updates.yml`:

```yaml
name: Monitor New Papers

on:
  schedule:
    - cron: '0 9 * * 1'  # Every Monday at 9 AM
  workflow_dispatch:

jobs:
  search-papers:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.x'
      
      - name: Install dependencies
        run: |
          pip install scholarly semanticscholar arxiv
      
      - name: Search for new papers
        run: python scripts/search_papers.py
      
      - name: Create issue with findings
        uses: actions/github-script@v6
        with:
          script: |
            github.rest.issues.create({
              owner: context.repo.owner,
              repo: context.repo.repo,
              title: 'Weekly Paper Review - ' + new Date().toISOString().split('T')[0],
              body: require('fs').readFileSync('new_papers.md', 'utf8'),
              labels: ['paper-review', 'automated']
            })
```

### Paper Search Script

`scripts/search_papers.py`:

```python
#!/usr/bin/env python3
"""
Search for new papers relevant to Agentic AI review
"""

import arxiv
from scholarly import scholarly
from semanticscholar as sch
from datetime import datetime, timedelta

# Search queries
QUERIES = [
    "agentic AI",
    "autonomous agents LLM",
    "multi-agent systems language models",
    "tool use large language models",
    "ReAct reasoning acting"
]

# Time window
DAYS_BACK = 7
cutoff_date = datetime.now() - timedelta(days=DAYS_BACK)

def search_arxiv(query, max_results=10):
    """Search arXiv for recent papers"""
    search = arxiv.Search(
        query=query,
        max_results=max_results,
        sort_by=arxiv.SortCriterion.SubmittedDate
    )
    
    papers = []
    for result in search.results():
        if result.published.replace(tzinfo=None) > cutoff_date:
            papers.append({
                'title': result.title,
                'authors': [a.name for a in result.authors],
                'summary': result.summary,
                'pdf_url': result.pdf_url,
                'published': result.published,
                'source': 'arXiv'
            })
    return papers

def search_semantic_scholar(query, limit=10):
    """Search Semantic Scholar"""
    # Implementation using semanticscholar API
    pass

def generate_report(all_papers):
    """Generate markdown report"""
    report = f"# Weekly Paper Review - {datetime.now().date()}\n\n"
    report += f"Found **{len(all_papers)}** potentially relevant papers.\n\n"
    
    for paper in all_papers:
        report += f"## {paper['title']}\n\n"
        report += f"**Authors**: {', '.join(paper['authors'][:3])}"
        if len(paper['authors']) > 3:
            report += " et al."
        report += f"\n\n**Published**: {paper['published'].date()}\n\n"
        report += f"**Source**: {paper['source']}\n\n"
        report += f"**Summary**: {paper['summary'][:300]}...\n\n"
        report += f"**Link**: {paper['pdf_url']}\n\n"
        report += "---\n\n"
    
    return report

if __name__ == "__main__":
    all_papers = []
    
    for query in QUERIES:
        papers = search_arxiv(query)
        all_papers.extend(papers)
    
    # Remove duplicates
    unique_papers = {p['title']: p for p in all_papers}.values()
    
    report = generate_report(list(unique_papers))
    
    with open('new_papers.md', 'w') as f:
        f.write(report)
    
    print(f"Found {len(unique_papers)} unique papers")
```

---

## 📈 Metrics & Tracking

### Paper Database

Maintain `papers/PAPER_TRACKER.md`:

```markdown
# Paper Integration Tracker

## Queue (To Review)
| Title | Authors | Venue | Added | Priority |
|-------|---------|-------|-------|----------|
| Paper 1 | Smith et al. | NeurIPS 2025 | 2025-11-15 | High |

## Under Review
| Title | Reviewer | Status | Notes |
|-------|----------|--------|-------|
| Paper 2 | Majid | Reading | Looks promising |

## Integrated
| Title | Venue | Date Added | Sections | Citations |
|-------|-------|------------|----------|-----------|
| Paper 3 | ICML 2024 | 2025-01-15 | 2, 5 | 45 |

## Rejected
| Title | Reason | Date |
|-------|--------|------|
| Paper 4 | Not peer-reviewed | 2025-11-10 |
```

### Reference Statistics

Track in `arxiv-paper/REFERENCE_STATS.md`:

```markdown
# Reference Statistics

**Total References**: 104
**Last Updated**: 2025-11-15

## By Year
- 2025: 15 papers
- 2024: 30 papers  
- 2023: 25 papers
- 2022: 20 papers
- Older: 14 papers

## By Venue Type
- Conferences: 45 (43%)
- Journals: 35 (34%)
- Preprints: 15 (14%)
- Technical Reports: 9 (9%)

## By Topic
- Foundations: 10
- LLMs: 12
- Reasoning: 8
- Tools: 6
- Multi-Agent: 10
- RAG: 12
- Fine-Tuning: 8
- Frameworks: 8
- Ethics: 10
- Production: 7
- New Papers: 5
- Other: 8
```

---

## ✅ Update Workflow Checklist

### Discovery Phase
- [ ] Run weekly searches
- [ ] Check Google Scholar alerts
- [ ] Review conference proceedings
- [ ] Check citations to key papers
- [ ] Screen abstracts
- [ ] Download promising papers

### Review Phase  
- [ ] Read selected papers
- [ ] Take notes on contributions
- [ ] Identify integration points
- [ ] Check quality/credibility
- [ ] Create BibTeX entries
- [ ] Update paper tracker

### Integration Phase
- [ ] Prepare integration text
- [ ] Add to references.bib
- [ ] Edit paper.tex
- [ ] Build and check (make)
- [ ] Review PDF output
- [ ] Update documentation

### Quality Check
- [ ] All citations correct
- [ ] No LaTeX errors
- [ ] Section flow maintained
- [ ] Cross-references work
- [ ] Page count reasonable
- [ ] Professional appearance

### Documentation
- [ ] Update PAPERS_SUMMARY.md
- [ ] Update INTEGRATION_GUIDE.md
- [ ] Update PAPER_TRACKER.md
- [ ] Update REFERENCE_STATS.md
- [ ] Commit with clear message
- [ ] Deploy documentation

---

## 🎓 Best Practices

### Citation Etiquette
1. **Primary sources**: Cite original work, not secondary
2. **Recent work**: Cite most recent relevant paper
3. **Balance**: Mix seminal and recent papers
4. **Credit**: Properly attribute ideas
5. **Verify**: Check papers before citing

### Writing Style
1. **Clear attribution**: "Smith et al. \cite{smith2025} demonstrate..."
2. **Critical analysis**: Don't just describe, evaluate
3. **Connections**: Link to other sections
4. **Concise**: Value over word count
5. **Academic tone**: Professional and objective

### Common Pitfalls to Avoid
- ❌ Citing papers you haven't read
- ❌ Over-citing from single source
- ❌ Ignoring contradictory findings
- ❌ Using outdated papers when recent exist
- ❌ Copy-pasting from papers
- ❌ Orphaned citations (in bib but not cited)
- ❌ Missing page numbers or DOIs

---

## 📧 Review Process

### Self-Review Questions
1. Does this paper add value?
2. Is it properly integrated (not just listed)?
3. Are citations accurate?
4. Does it fit the narrative?
5. Is writing quality maintained?
6. Are claims properly supported?

### Peer Review (Optional)
- Share draft with colleagues
- Request feedback on new sections
- Verify technical accuracy
- Check readability

---

**Last Updated**: November 15, 2025  
**Current References**: 104  
**Next Quarterly Review**: February 2026  
**Maintained By**: Majid Memari (mmemari@uvu.edu)

