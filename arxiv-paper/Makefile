# Makefile for arXiv paper compilation

# Main paper file (without extension)
PAPER = paper

# LaTeX compiler
LATEX = pdflatex
BIBTEX = bibtex

# Compiler flags
LATEX_FLAGS = -interaction=nonstopmode -halt-on-error

.PHONY: all clean distclean view

# Default target: build the paper
all: $(PAPER).pdf

# Build the PDF (full compilation with bibliography)
$(PAPER).pdf: $(PAPER).tex
	@echo "First LaTeX pass..."
	$(LATEX) $(LATEX_FLAGS) $(PAPER).tex
	@echo "Running BibTeX..."
	-$(BIBTEX) $(PAPER)
	@echo "Second LaTeX pass..."
	$(LATEX) $(LATEX_FLAGS) $(PAPER).tex
	@echo "Third LaTeX pass..."
	$(LATEX) $(LATEX_FLAGS) $(PAPER).tex
	@echo "✓ Paper compiled successfully!"

# Quick build (single pass, for testing)
quick: $(PAPER).tex
	@echo "Quick compilation (single pass)..."
	$(LATEX) $(LATEX_FLAGS) $(PAPER).tex

# Clean auxiliary files
clean:
	@echo "Cleaning auxiliary files..."
	rm -f $(PAPER).aux $(PAPER).log $(PAPER).out $(PAPER).toc
	rm -f $(PAPER).bbl $(PAPER).blg $(PAPER).synctex.gz
	rm -f $(PAPER).fdb_latexmk $(PAPER).fls
	rm -f *.aux *.log *.out *.toc *.bbl *.blg
	@echo "✓ Cleaned auxiliary files"

# Remove all generated files including PDF
distclean: clean
	@echo "Removing PDF..."
	rm -f $(PAPER).pdf
	@echo "✓ Full clean complete"

# View the PDF (macOS)
view: $(PAPER).pdf
	@if [ `uname` = "Darwin" ]; then \
		open $(PAPER).pdf; \
	elif [ `uname` = "Linux" ]; then \
		xdg-open $(PAPER).pdf 2>/dev/null || evince $(PAPER).pdf; \
	else \
		echo "Please open $(PAPER).pdf manually"; \
	fi

# Check for common LaTeX errors
check:
	@echo "Checking LaTeX syntax..."
	@chktex -q $(PAPER).tex || echo "Consider installing chktex for style checking"

# Count words (approximate, excludes LaTeX commands)
wordcount:
	@echo "Word count (approximate):"
	@detex $(PAPER).tex | wc -w || echo "Install detex for accurate word count"

# Display help
help:
	@echo "Available targets:"
	@echo "  make          - Build the paper (default)"
	@echo "  make quick    - Quick single-pass compilation"
	@echo "  make clean    - Remove auxiliary files"
	@echo "  make distclean- Remove all generated files"
	@echo "  make view     - Open the PDF"
	@echo "  make check    - Check for LaTeX errors"
	@echo "  make wordcount- Count words in paper"
	@echo "  make help     - Show this help message"

