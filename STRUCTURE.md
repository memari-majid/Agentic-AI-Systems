# Repository Structure

Clean and organized knowledge base - easy to access and navigate.

## Directory Layout

```
Agentic-AI-Systems/
│
├── 01-foundations/              # 🧠 Theoretical Foundations
│   ├── README.md               # Section guide
│   ├── 01-generative-ai-fundamentals.md
│   ├── 02-agentic-system-principles.md
│   ├── 03-intelligent-agent-components.md
│   ├── 04-reflection-introspection.md
│   ├── 05-tool-use-planning.md
│   ├── 06-multi-agent-coordination.md
│   ├── 07-system-design-techniques.md
│   ├── 08-building-trust-safety.md
│   ├── 09-ethics-considerations.md
│   ├── 10-use-cases-applications.md
│   └── 11-future-outlook.md
│
├── 02-implementation/           # ⚡ Practical Development
│   ├── README.md
│   ├── 01-introduction.md
│   ├── 02-langchain-foundations.md
│   ├── 03-langgraph-workflows.md
│   ├── 04-combined-approach.md
│   ├── 05-dspy-optimization.md
│   ├── 06-state-management.md
│   ├── 07-debugging-monitoring.md
│   ├── 08-unstructured-data.md
│   ├── 09-best-practices.md
│   └── 10-references.md
│
├── 03-modern-frameworks/        # 🚀 Latest Technologies
│   ├── README.md
│   ├── pydantic-ai.md
│   ├── model-context-protocol.md
│   ├── autonomous-agents.md
│   ├── multi-agent-systems.md
│   ├── communication-protocols.md
│   ├── orchestration-frameworks.md
│   ├── security-observability.md
│   ├── enterprise-platforms.md
│   ├── technology-comparison.md
│   └── agentic-ai-2025.md
│
├── 04-strategy/                 # 📈 Leadership & Strategy
│   ├── README.md
│   ├── 01-strategic-planning.md
│   ├── 02-team-building.md
│   ├── 03-technology-selection.md
│   ├── 04-implementation-roadmap.md
│   ├── 05-change-management.md
│   ├── 06-risk-assessment.md
│   ├── 07-performance-metrics.md
│   ├── 08-stakeholder-alignment.md
│   ├── 09-budget-resources.md
│   ├── 10-governance-ethics.md
│   ├── 11-scaling-strategies.md
│   ├── 12-future-planning.md
│   ├── 13-case-studies.md
│   ├── 14-industry-applications.md
│   ├── 15-roi-measurement.md
│   ├── 16-continuous-improvement.md
│   └── 17-advanced-topics.md
│
├── 05-research/                 # 🔬 Frontier Research
│   ├── README.md
│   └── leveraging-unstructured-data-llms.md
│
├── 06-labs/                     # 🧪 Hands-On Labs
│   ├── README.md
│   ├── 01-hello-graph.md
│   ├── 01-hello-graph.py
│   ├── 02-travel-booking-graph.md
│   ├── 02-travel-booking-graph.py
│   ├── 03-parallel-scoring.md
│   ├── 03-parallel-scoring.py
│   ├── 04-reflection-loops.md
│   ├── 04-reflection-loops.py
│   ├── 05-parallel-planning.md
│   ├── 05-parallel-planning.py
│   ├── 06-nested-graphs.md
│   ├── 06-nested-graphs.py
│   ├── 07-memory-feedback.md
│   ├── 07-memory-feedback.py
│   ├── 08-tool-protocols.md
│   ├── 08-tool-protocols.py
│   ├── 09-guardrails.md
│   ├── 09-guardrails.py
│   ├── 10-dspy-optimization.md
│   ├── 10-dspy-optimization.py
│   ├── 11-agent-finetuning.md
│   ├── 11-agent-finetuning.py
│   ├── 12-multi-agent-systems.md
│   ├── 12-multi-agent-systems.py
│   ├── 13-document-rag-agents.md
│   └── 13-document-rag-pipeline.md
│
├── assets/                      # 🖼️ Images & Resources
│   ├── logo.png
│   └── banner.png
│
└── README.md                    # 📖 Main Documentation
```

## File Count

- **70 Markdown files** (.md)
- **12 Python files** (.py)
- **7 README guides** (navigation)
- **2 image assets**

## Navigation

Each section has a `README.md` that provides:
- Overview of content
- Chapter descriptions
- Learning objectives
- Prerequisites
- Estimated reading time

## File Naming Convention

- `##-descriptive-name.md` - Numbered chapters (sequential reading)
- `descriptive-name.md` - Standalone documents
- `##-name.py` - Code files corresponding to labs

## Access Patterns

**By Section:**
```bash
ls 01-foundations/
ls 02-implementation/
ls 06-labs/
```

**By Topic:**
```bash
grep -r "multi-agent" .
grep -r "RAG" .
```

**Sequential Reading:**
```bash
cd 01-foundations
cat 01-generative-ai-fundamentals.md
cat 02-agentic-system-principles.md
# ... continue
```

## Content Organization

### Theory → Practice → Advanced
1. **Foundations** - Core concepts
2. **Implementation** - Practical skills
3. **Modern Frameworks** - Latest tools
4. **Strategy** - Leadership
5. **Research** - Frontier topics
6. **Labs** - Hands-on code

## No Website, No Build System

Just plain Markdown files you can:
- Read in terminal (`cat`, `less`, `more`)
- Open in any editor (VS Code, Vim, Emacs)
- View in any IDE (IntelliJ, PyCharm)
- Browse on GitHub
- Search with grep or IDE search

Simple. Clean. Organized. 🎯
