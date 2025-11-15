#!/usr/bin/env python3
"""
Update paper version and last modified date in both LaTeX and HTML versions
"""

import os
import re
from datetime import datetime
from pathlib import Path

def get_version_info():
    """Get current version and date"""
    now = datetime.now()
    date_str = now.strftime('%B %d, %Y')
    date_iso = now.strftime('%Y-%m-%d')
    version = now.strftime('%Y.%m.%d')
    return {
        'date': date_str,
        'date_iso': date_iso,
        'version': version,
        'year': now.year,
        'month': now.month,
        'day': now.day
    }

def update_latex_version(paper_tex_path, version_info):
    """Update version in LaTeX paper"""
    if not os.path.exists(paper_tex_path):
        print(f"LaTeX file not found: {paper_tex_path}")
        return False
    
    with open(paper_tex_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Update date in LaTeX - use lambda to avoid escape issues
    def replace_date(match):
        return f"\\date{{{version_info['date']}}}"
    
    content = re.sub(r'\\date\{[^}]+\}', replace_date, content)
    
    # Add version command if not exists
    if '\\newcommand{\\paperversion}' not in content:
        # Add after documentclass
        def add_version(match):
            return f"{match.group(1)}\n\\newcommand{{\\paperversion}}{{{version_info['version']}}}\n\\newcommand{{\\lastupdated}}{{{version_info['date']}}}"
        content = re.sub(r'(\\documentclass\[12pt\]\{article\})', add_version, content)
    else:
        # Update existing version command
        def update_version(match):
            return f"\\newcommand{{\\paperversion}}{{{version_info['version']}}}"
        def update_date(match):
            return f"\\newcommand{{\\lastupdated}}{{{version_info['date']}}}"
        content = re.sub(r'\\newcommand\{\\paperversion\}\{[^}]+\}', update_version, content)
        content = re.sub(r'\\newcommand\{\\lastupdated\}\{[^}]+\}', update_date, content)
    
    with open(paper_tex_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ Updated LaTeX version to {version_info['version']}")
    return True

def update_html_version(paper_dir, version_info):
    """Update version in HTML paper pages"""
    paper_dir = Path(paper_dir)
    
    if not paper_dir.exists():
        print(f"Paper directory not found: {paper_dir}")
        return False
    
    # Files to update
    files_to_update = [
        'index.md',
        '01-introduction.md',
        '02-related-work.md',
        '03-foundations.md',
        '04-implementation.md',
        '05-knowledge-integration.md',
        '06-organizational.md',
        '07-conclusion.md',
        '08-references.md'
    ]
    
    updated_count = 0
    
    for filename in files_to_update:
        filepath = paper_dir / filename
        if not filepath.exists():
            continue
        
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Add or update version info at the top
        version_block = f"""---
version: {version_info['version']}
last_updated: {version_info['date_iso']}
last_updated_display: {version_info['date']}
---

"""
        
        # Remove existing version block if present
        content = re.sub(r'^---\nversion:.*?\n---\n\n', '', content, flags=re.MULTILINE | re.DOTALL)
        
        # Add new version block at the beginning
        if not content.startswith('---'):
            content = version_block + content
        else:
            # If there's already frontmatter, update it
            frontmatter_pattern = r'^---\n(.*?)\n---\n\n'
            match = re.match(frontmatter_pattern, content, re.DOTALL)
            if match:
                # Update existing frontmatter
                existing = match.group(1)
                if 'version:' not in existing:
                    existing += f"\nversion: {version_info['version']}"
                else:
                    existing = re.sub(r'version:.*', f"version: {version_info['version']}", existing)
                
                if 'last_updated:' not in existing:
                    existing += f"\nlast_updated: {version_info['date_iso']}"
                    existing += f"\nlast_updated_display: {version_info['date']}"
                else:
                    existing = re.sub(r'last_updated:.*', f"last_updated: {version_info['date_iso']}", existing)
                    existing = re.sub(r'last_updated_display:.*', f"last_updated_display: {version_info['date']}", existing)
                
                content = f"---\n{existing}\n---\n\n" + content[match.end():]
            else:
                content = version_block + content
        
        # Also update any "Last Updated" text in the content
        content = re.sub(
            r'\*\*Last Updated\*\*:.*',
            f"**Last Updated**: {version_info['date']}",
            content
        )
        
        # Add version badge if not present in index.md
        if filename == 'index.md' and 'version:' not in content[:500]:
            # Find a good place to insert version info
            if '!!! info' in content:
                # Add after first info box
                content = re.sub(
                    r'(!!! info "Paper Information"[^\n]*\n[^\n]*\n[^\n]*\n[^\n]*\n[^\n]*\n[^\n]*\n)',
                    r'\1\n!!! success "Version Information"\n    **Version**: ' + version_info['version'] + '\n    **Last Updated**: ' + version_info['date'] + '\n    **Status**: Automatically updated weekly\n\n',
                    content
                )
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        updated_count += 1
    
    print(f"✅ Updated {updated_count} HTML paper pages")
    return updated_count > 0

def main():
    """Main function"""
    repo_root = Path(__file__).parent.parent
    version_info = get_version_info()
    
    print(f"📝 Updating paper version to {version_info['version']}")
    print(f"📅 Date: {version_info['date']}")
    
    # Update LaTeX version
    latex_path = repo_root / 'arxiv-paper' / 'paper.tex'
    update_latex_version(latex_path, version_info)
    
    # Update HTML versions
    html_dir = repo_root / 'docs' / 'paper'
    update_html_version(html_dir, version_info)
    
    print(f"\n✅ Version update complete!")
    print(f"   Version: {version_info['version']}")
    print(f"   Date: {version_info['date']}")

if __name__ == '__main__':
    main()

