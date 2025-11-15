# GitHub Pages Setup & Deployment Guide

Complete guide for running and maintaining the GitHub Pages site for the Agentic AI Systems review paper.

## 🚀 Quick Start

### Prerequisites
```bash
# Install Python dependencies
pip install -r requirements.txt

# Verify MkDocs installation
mkdocs --version  # Should show mkdocs, version 1.5.0 or higher
```

## 📖 Running Locally

### 1. Development Server

```bash
# Navigate to repository root
cd /home/majid/Downloads/Agentic-AI-Systems

# Start local development server
mkdocs serve

# Output will show:
# INFO     -  Building documentation...
# INFO     -  Cleaning site directory
# INFO     -  Documentation built in 0.52 seconds
# INFO     -  [09:00:00] Serving on http://127.0.0.1:8000/
```

**Access**: Open browser to `http://127.0.0.1:8000/`

### 2. Live Reload

The development server includes live reload:
- Edit any `.md` file in `docs/`
- Save the file
- Browser automatically refreshes
- See changes immediately

### 3. Build Static Site

```bash
# Build production-ready site
mkdocs build

# Output in site/ directory
# Files are optimized for deployment
```

## 🌐 GitHub Pages Deployment

### Option 1: Automatic Deployment (Recommended)

#### Step 1: Enable GitHub Pages

1. Go to your repository on GitHub
2. Click **Settings** → **Pages**
3. Under **Source**, select:
   - Branch: `gh-pages`
   - Folder: `/ (root)`
4. Click **Save**

#### Step 2: Deploy with MkDocs

```bash
# Single command deployment
mkdocs gh-deploy

# This will:
# 1. Build the site
# 2. Create/update gh-pages branch
# 3. Push to GitHub
# 4. Trigger GitHub Pages deployment
```

#### Step 3: Verify Deployment

- Wait 1-2 minutes for GitHub Pages to build
- Visit: `https://YOUR-USERNAME.github.io/Agentic-AI-Systems/`
- Your site is live!

### Option 2: Manual Deployment

```bash
# Build the site
mkdocs build

# Switch to gh-pages branch
git checkout gh-pages

# Copy built files
cp -r site/* .

# Commit and push
git add .
git commit -m "Update GitHub Pages"
git push origin gh-pages

# Switch back to main
git checkout main
```

### Option 3: GitHub Actions (Automated)

Create `.github/workflows/deploy-docs.yml`:

```yaml
name: Deploy Documentation

on:
  push:
    branches:
      - main
    paths:
      - 'docs/**'
      - 'mkdocs.yml'

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.x'
      
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
      
      - name: Deploy to GitHub Pages
        run: |
          git config user.name "github-actions[bot]"
          git config user.email "github-actions[bot]@users.noreply.github.com"
          mkdocs gh-deploy --force
```

**Benefits**:
- Automatic deployment on every push to main
- No manual commands needed
- Always up-to-date

## 📝 Updating Documentation

### Add New Page

1. **Create Markdown File**
```bash
# Example: Add new framework
nano docs/frameworks/new-framework.md
```

2. **Add Content**
```markdown
# New Framework

## Overview
Description of the framework...

## Features
- Feature 1
- Feature 2

## Example
\`\`\`python
# Code example
\`\`\`
```

3. **Update Navigation** (mkdocs.yml)
```yaml
nav:
  - Home: index.md
  - Frameworks:
    - Overview: frameworks/index.md
    - New Framework: frameworks/new-framework.md  # Add this
```

4. **Preview Locally**
```bash
mkdocs serve
```

5. **Deploy**
```bash
mkdocs gh-deploy
```

### Update Existing Page

1. Edit the `.md` file in `docs/`
2. Save changes
3. Preview with `mkdocs serve`
4. Deploy with `mkdocs gh-deploy`

### Update Paper on Site

When you update `arxiv-paper/paper.pdf`:

```bash
# Copy updated PDF to docs
cp arxiv-paper/paper.pdf docs/

# Deploy
mkdocs gh-deploy
```

## 🔧 Configuration

### MkDocs Configuration (mkdocs.yml)

```yaml
site_name: Agentic AI Systems
site_url: https://YOUR-USERNAME.github.io/Agentic-AI-Systems/
site_description: Comprehensive framework for building autonomous intelligent agents

theme:
  name: material
  features:
    - navigation.tabs
    - navigation.sections
    - toc.integrate
    - search.suggest
    - search.highlight
  palette:
    - scheme: default
      primary: indigo
      accent: indigo

plugins:
  - search
  - minify:
      minify_html: true

extra_javascript:
  - javascripts/mathjax.js
  - https://polyfill.io/v3/polyfill.min.js?features=es6
  - https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js

extra_css:
  - stylesheets/extra.css

markdown_extensions:
  - pymdownx.arithmatex:
      generic: true
  - pymdownx.highlight
  - pymdownx.superfences
  - admonition
  - toc:
      permalink: true
```

## 🎨 Customization

### Custom CSS

Edit `docs/stylesheets/extra.css`:

```css
/* Custom styles for paper */
.paper-section {
  margin: 2em 0;
  padding: 1em;
  background: #f5f5f5;
}

/* Citation styling */
.citation {
  font-style: italic;
  color: #666;
}
```

### Custom JavaScript

Edit `docs/javascripts/mathjax.js` for math rendering:

```javascript
window.MathJax = {
  tex: {
    inlineMath: [["\\(", "\\)"]],
    displayMath: [["\\[", "\\]"]],
    processEscapes: true,
    processEnvironments: true
  },
  options: {
    ignoreHtmlClass: ".*|",
    processHtmlClass: "arithmatex"
  }
};
```

## 📊 Site Structure

```
docs/
├── index.md                    # Home page
├── arxiv-paper/                # Paper documentation
│   ├── index.md
│   ├── overview.md
│   └── citation.md
├── paper.pdf                   # Actual paper PDF
├── javascripts/
│   └── mathjax.js             # Math rendering
└── stylesheets/
    └── extra.css              # Custom styles

site/ (generated)
├── index.html                  # Built home page
├── arxiv-paper/
│   ├── index.html
│   ├── overview/
│   └── citation/
├── paper.pdf
├── assets/
├── search/
└── sitemap.xml
```

## 🔍 Testing

### Before Deployment

```bash
# 1. Clean previous build
rm -rf site/

# 2. Fresh build
mkdocs build

# 3. Check for errors
# Look for warnings in output

# 4. Test locally
mkdocs serve

# 5. Test all links work
# Click through navigation

# 6. Test search functionality

# 7. Test on mobile (responsive design)
```

### After Deployment

1. **Visit live site**
2. **Check all pages load**
3. **Test navigation**
4. **Test search**
5. **Verify PDF downloads**
6. **Check mobile responsiveness**

## 🐛 Troubleshooting

### Issue: Site not updating

```bash
# Clear GitHub Pages cache
mkdocs gh-deploy --force

# Or manually clear gh-pages branch
git push origin --delete gh-pages
mkdocs gh-deploy
```

### Issue: 404 errors

Check `mkdocs.yml`:
```yaml
# Ensure site_url is correct
site_url: https://YOUR-USERNAME.github.io/Agentic-AI-Systems/

# Not:
# site_url: https://YOUR-USERNAME.github.io/Agentic-AI-Systems
```

### Issue: Math not rendering

1. Check `docs/javascripts/mathjax.js` exists
2. Verify in `mkdocs.yml`:
```yaml
extra_javascript:
  - javascripts/mathjax.js
  - https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js
```

### Issue: Build fails

```bash
# Check Python dependencies
pip install -r requirements.txt --upgrade

# Verify MkDocs version
mkdocs --version

# Check for syntax errors
mkdocs build --strict
```

## 📈 Maintenance

### Regular Updates

**Weekly**:
- Check for broken links
- Update paper if revised
- Review GitHub Pages status

**Monthly**:
- Update dependencies: `pip install -r requirements.txt --upgrade`
- Review analytics (if configured)
- Check for MkDocs updates

**As Needed**:
- Add new research papers
- Update documentation
- Fix reported issues

### Monitoring

```bash
# Check deployment status
git log gh-pages --oneline -5

# View site build logs
# Go to: https://github.com/YOUR-USERNAME/Agentic-AI-Systems/actions
```

## 🔒 Security

### HTTPS

GitHub Pages automatically provides HTTPS:
- `https://YOUR-USERNAME.github.io/Agentic-AI-Systems/`
- Certificate managed by GitHub

### Custom Domain (Optional)

1. Add `CNAME` file to `docs/`:
```bash
echo "yourdomain.com" > docs/CNAME
```

2. Configure DNS:
```
Type: CNAME
Name: www (or subdomain)
Value: YOUR-USERNAME.github.io
```

3. Enable in GitHub Settings → Pages → Custom domain

## 📚 Resources

### Documentation
- **MkDocs**: https://www.mkdocs.org/
- **Material Theme**: https://squidfunk.github.io/mkdocs-material/
- **GitHub Pages**: https://docs.github.com/en/pages

### Commands Reference

```bash
# Development
mkdocs serve          # Start dev server
mkdocs serve -a 0.0.0.0:8000  # Listen on all interfaces

# Building
mkdocs build          # Build site
mkdocs build --strict # Build with warnings as errors
mkdocs build --clean  # Clean before building

# Deployment
mkdocs gh-deploy      # Deploy to GitHub Pages
mkdocs gh-deploy --force  # Force deployment
mkdocs gh-deploy -m "Custom commit message"  # With message

# Utilities
mkdocs --version      # Show version
mkdocs -h             # Show help
```

## ✅ Checklist

### Initial Setup
- [ ] Install dependencies
- [ ] Test local build
- [ ] Configure mkdocs.yml
- [ ] Enable GitHub Pages
- [ ] Deploy site
- [ ] Verify live site

### Regular Workflow
- [ ] Edit documentation
- [ ] Preview locally (`mkdocs serve`)
- [ ] Test all links
- [ ] Deploy (`mkdocs gh-deploy`)
- [ ] Verify on live site

---

**Last Updated**: November 15, 2025  
**MkDocs Version**: 1.5.0+  
**Status**: Production Ready

