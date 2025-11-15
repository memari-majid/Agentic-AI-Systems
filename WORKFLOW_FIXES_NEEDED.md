# ⚠️ Workflow Dependency Fixes - Manual Update Required

**Issue**: GitHub OAuth restrictions prevent automatic workflow file updates  
**Status**: Fixes prepared locally, need manual application

---

## ✅ Issue Verified and Fixed Locally

### Problem Found

1. **weekly-paper-update.yml** (line 69):
   ```yaml
   # BEFORE (incorrect):
   pip install mkdocs-material
   mkdocs gh-deploy --force
   ```
   
   **Issues**:
   - ❌ Only installs `mkdocs-material`
   - ❌ Missing `mkdocs` base package
   - ❌ Missing `mkdocs-minify-plugin`
   - ❌ Missing `mkdocs-git-revision-date-localized-plugin`
   - ❌ No version consistency from `requirements.txt`

2. **deploy-docs.yml** (if it exists):
   - Same issues as above

---

## ✅ Fixes Applied Locally

### 1. Fixed weekly-paper-update.yml

**Location**: `.github/workflows/weekly-paper-update.yml`  
**Line**: 66-71

**Change Required**:
```yaml
# AFTER (correct):
- name: Deploy updated documentation
  if: steps.changes.outputs.has_changes == 'true'
  run: |
    pip install --upgrade pip
    pip install -r requirements.txt
    mkdocs gh-deploy --force
```

### 2. Created deploy-docs.yml

**Location**: `.github/workflows/deploy-docs.yml`  
**Status**: Needs manual creation

**Complete File Content**:
```yaml
name: Deploy Documentation

on:
  push:
    branches:
      - main
    paths:
      - 'docs/**'
      - 'mkdocs.yml'
      - 'requirements.txt'
  workflow_dispatch:

permissions:
  contents: write

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
          cache: 'pip'
      
      - name: Install dependencies
        run: |
          pip install --upgrade pip
          pip install -r requirements.txt
      
      - name: Deploy to GitHub Pages
        run: |
          git config user.name "github-actions[bot]"
          git config user.email "github-actions[bot]@users.noreply.github.com"
          mkdocs gh-deploy --force
```

### 3. Updated requirements.txt

**Added**: `mkdocs-minify-plugin>=0.7.0` ✅ (already pushed)

**Complete MkDocs dependencies**:
```txt
mkdocs>=1.5.3
mkdocs-material>=9.5.3
mkdocs-minify-plugin>=0.7.0
mkdocs-git-revision-date-localized-plugin>=1.2.0
```

---

## 📋 Manual Update Instructions

### Step 1: Update weekly-paper-update.yml

1. Go to: https://github.com/memari-majid/Agentic-AI-Systems
2. Navigate to: `.github/workflows/weekly-paper-update.yml`
3. Click "Edit" (pencil icon)
4. Find lines 66-71 (Deploy updated documentation step)
5. Replace with:
   ```yaml
   - name: Deploy updated documentation
     if: steps.changes.outputs.has_changes == 'true'
     run: |
       pip install --upgrade pip
       pip install -r requirements.txt
       mkdocs gh-deploy --force
   ```
6. Commit changes

### Step 2: Create deploy-docs.yml

1. Go to: https://github.com/memari-majid/Agentic-AI-Systems
2. Click "Add file" → "Create new file"
3. Path: `.github/workflows/deploy-docs.yml`
4. Copy the complete file content from above
5. Commit directly to `main` branch

---

## ✅ Verification

After manual updates, verify:

1. ✅ `weekly-paper-update.yml` uses `pip install -r requirements.txt`
2. ✅ `deploy-docs.yml` exists and uses `pip install -r requirements.txt`
3. ✅ `requirements.txt` includes all plugins

---

## 📊 What Gets Installed

After fix, all workflows will install:

- ✅ `mkdocs>=1.5.3` (base package)
- ✅ `mkdocs-material>=9.5.3` (theme)
- ✅ `mkdocs-minify-plugin>=0.7.0` (HTML minification)
- ✅ `mkdocs-git-revision-date-localized-plugin>=1.2.0` (dates)

All from `requirements.txt` - single source of truth!

---

## 🎯 Benefits

1. **Version Consistency**: All workflows use same versions
2. **Complete Dependencies**: All plugins automatically included
3. **Easier Maintenance**: Update once in requirements.txt
4. **Best Practices**: Consistent with standard workflow patterns

---

**Status**: Fixes ready, awaiting manual workflow file updates

