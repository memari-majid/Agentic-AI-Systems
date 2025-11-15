# GitHub Pages Deployment Guide

This guide will help you deploy your Agentic AI Systems knowledge base to GitHub Pages using MkDocs Material.

## ✅ What's Already Done

All configuration files have been created:
- ✅ `mkdocs.yml` - Site configuration
- ✅ `.github/workflows/deploy.yml` - Auto-deployment workflow
- ✅ `CITATION.cff` - Citation metadata
- ✅ `requirements.txt` - Python dependencies
- ✅ `.gitignore` - Ignore build files
- ✅ `index.md` - Homepage

## 🚀 Quick Start

### Option 1: Automatic Deployment (Recommended)

Just push to GitHub and it deploys automatically!

```bash
# Add and commit all files
git add .
git commit -m "Add MkDocs Material configuration and GitHub Pages deployment"

# Push to GitHub
git push origin main
```

The GitHub Action will automatically:
1. Build your MkDocs site
2. Deploy it to GitHub Pages
3. Make it live at: https://memari-majid.github.io/Agentic-AI-Systems/

### Option 2: Test Locally First

Test the site on your computer before deploying:

```bash
# Install dependencies
pip install -r requirements.txt

# Serve the site locally
mkdocs serve
```

Then open your browser to: http://127.0.0.1:8000

## 📋 GitHub Pages Setup (First Time Only)

After your first push, you need to enable GitHub Pages:

1. Go to your repository on GitHub: `https://github.com/memari-majid/Agentic-AI-Systems`
2. Click **Settings** (top menu)
3. Click **Pages** (left sidebar)
4. Under **Source**, select:
   - Source: `Deploy from a branch`
   - Branch: `gh-pages`
   - Folder: `/ (root)`
5. Click **Save**

Your site will be live in 1-2 minutes at:
**https://memari-majid.github.io/Agentic-AI-Systems/**

## 🔧 Customization

### Change Colors

Edit `mkdocs.yml`:

```yaml
theme:
  palette:
    primary: indigo  # Change to: blue, teal, green, etc.
    accent: indigo   # Change to: blue, teal, green, etc.
```

### Add Google Analytics

1. Get your Google Analytics ID (format: `G-XXXXXXXXXX`)
2. Edit `mkdocs.yml`:

```yaml
extra:
  analytics:
    provider: google
    property: G-XXXXXXXXXX  # Replace with your ID
```

### Update Author Info

Edit `CITATION.cff`:

```yaml
authors:
  - family-names: "Memari"
    given-names: "Majid"
    email: your.email@example.com  # Update your email
```

## 📊 Features Included

- ✅ Beautiful Material Design theme
- ✅ Dark/Light mode toggle
- ✅ Built-in search
- ✅ Navigation tabs and sections
- ✅ Mobile responsive
- ✅ Code syntax highlighting
- ✅ Automatic deployment
- ✅ Edit button on each page
- ✅ Citation metadata
- ✅ Social media links

## 🐛 Troubleshooting

### Site not deploying?

1. Check the **Actions** tab on GitHub for error messages
2. Make sure you enabled GitHub Pages (see setup above)
3. Verify the `gh-pages` branch exists

### Local preview not working?

```bash
# Reinstall dependencies
pip install --upgrade -r requirements.txt

# Clear cache and rebuild
mkdocs build --clean
mkdocs serve
```

### 404 errors on links?

- Check that all file paths in `mkdocs.yml` match your actual files
- Ensure all `.md` files exist in their directories

## 📝 Making Updates

Every time you push to `main`, the site automatically rebuilds:

```bash
# Make your changes to .md files
git add .
git commit -m "Update content"
git push origin main
```

Wait 1-2 minutes and your changes are live!

## 🌟 Next Steps

1. **Push to GitHub** - Deploy your site
2. **Enable GitHub Pages** - Configure in repository settings
3. **Share your URL** - https://memari-majid.github.io/Agentic-AI-Systems/
4. **Add Zenodo DOI** - For permanent citation
5. **Submit to arXiv** - For academic citations
6. **Share on social media** - LinkedIn, Twitter, Reddit

## 🔗 Useful Links

- [MkDocs Documentation](https://www.mkdocs.org/)
- [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/)
- [GitHub Pages Docs](https://docs.github.com/en/pages)
- [Citation File Format](https://citation-file-format.github.io/)

## 🎉 You're Done!

Your knowledge base is now ready for the world to see and cite! 🚀

