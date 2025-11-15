#!/usr/bin/env python3
"""
Simple Content Update Agent

Run this to automatically check and update your knowledge base.

Usage:
    python update-agent.py

Requirements:
    pip install openai requests
    export OPENAI_API_KEY="your-key"
"""

import os
import sys
from pathlib import Path
from datetime import datetime


def check_environment():
    """Verify environment is set up"""
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ OPENAI_API_KEY not set")
        print("   Run: export OPENAI_API_KEY='your-key'")
        return False
    return True


def scan_knowledge_base():
    """Scan the knowledge base structure"""
    print("🔍 Scanning knowledge base...\n")
    
    sections = {
        "01-foundations": "Foundations",
        "02-implementation": "Implementation",
        "03-modern-frameworks": "Modern Frameworks",
        "04-strategy": "Strategy",
        "05-research": "Research",
        "06-labs": "Labs"
    }
    
    repo_root = Path(__file__).parent
    
    for dir_name, display_name in sections.items():
        section_path = repo_root / dir_name
        
        if section_path.exists():
            md_files = list(section_path.glob("*.md"))
            py_files = list(section_path.glob("*.py"))
            
            print(f"📁 {display_name}:")
            print(f"   Markdown files: {len(md_files)}")
            if py_files:
                print(f"   Python files: {len(py_files)}")
            print()
        else:
            print(f"⚠️  {display_name}: Directory not found")
            print()
            

def check_framework_versions():
    """Check for framework updates"""
    print("🔄 Checking framework versions...\n")
    
    frameworks = {
        "LangChain": "https://api.github.com/repos/langchain-ai/langchain/releases/latest",
        "LangGraph": "https://api.github.com/repos/langchain-ai/langgraph/releases/latest",
        "Pydantic AI": "https://api.github.com/repos/pydantic/pydantic-ai/releases/latest",
        "DSPy": "https://api.github.com/repos/stanfordnlp/dspy/releases/latest",
    }
    
    try:
        import requests
        
        for name, url in frameworks.items():
            try:
                response = requests.get(url, timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    version = data.get("tag_name", "unknown")
                    date = data.get("published_at", "")[:10]
                    print(f"✅ {name}: {version} (released {date})")
                else:
                    print(f"⚠️  {name}: Could not fetch version")
            except Exception as e:
                print(f"⚠️  {name}: {e}")
                
    except ImportError:
        print("⚠️  'requests' not installed. Run: pip install requests")
        return
        
    print()


def verify_internal_links():
    """Check internal links between files"""
    print("🔗 Verifying internal links...\n")
    
    repo_root = Path(__file__).parent
    md_files = list(repo_root.glob("**/*.md"))
    
    broken_links = []
    
    for md_file in md_files:
        try:
            content = md_file.read_text(encoding="utf-8")
            
            # Find relative markdown links
            import re
            links = re.findall(r'\[([^\]]+)\]\(([^\)]+\.md)\)', content)
            
            for link_text, link_path in links:
                # Resolve relative path
                if not link_path.startswith("http"):
                    target = (md_file.parent / link_path).resolve()
                    
                    if not target.exists():
                        broken_links.append({
                            "file": str(md_file.relative_to(repo_root)),
                            "link": link_path,
                            "target": str(target)
                        })
                        
        except Exception as e:
            print(f"⚠️  Error checking {md_file.name}: {e}")
            
    if broken_links:
        print(f"⚠️  Found {len(broken_links)} broken internal links:")
        for link in broken_links[:5]:  # Show first 5
            print(f"   {link['file']} → {link['link']}")
        if len(broken_links) > 5:
            print(f"   ... and {len(broken_links) - 5} more")
    else:
        print("✅ All internal links valid")
        
    print()


def suggest_updates():
    """Suggest potential content updates using AI"""
    print("💡 Suggesting content updates...\n")
    
    if not os.getenv("OPENAI_API_KEY"):
        print("⚠️  OpenAI API key not set, skipping AI suggestions")
        return
        
    print("🤖 AI-powered suggestions:")
    print("   - Check for new framework features")
    print("   - Update technology comparisons")
    print("   - Refresh best practices")
    print("   - Add recent case studies")
    print("   - Update industry trends")
    print()
    
    # Here you would integrate OpenAI API
    # For now, we provide manual checklist
    

def generate_maintenance_report():
    """Generate maintenance recommendations"""
    print("📋 Maintenance Recommendations:\n")
    
    recommendations = [
        "✅ Review framework updates monthly",
        "✅ Check links quarterly",
        "✅ Update technology comparisons with each major release",
        "✅ Add new research papers as they're published",
        "✅ Refresh case studies annually",
        "✅ Update best practices based on community feedback"
    ]
    
    for rec in recommendations:
        print(f"   {rec}")
        
    print()


def main():
    """Main agent workflow"""
    print("=" * 60)
    print("🤖 AGENTIC AI SYSTEMS - CONTENT UPDATE AGENT")
    print("=" * 60)
    print()
    
    # Check environment
    if not check_environment():
        print("\n⚠️  Environment not ready. Set OPENAI_API_KEY to continue.\n")
    
    # Run checks
    scan_knowledge_base()
    check_framework_versions()
    verify_internal_links()
    suggest_updates()
    generate_maintenance_report()
    
    print("=" * 60)
    print(f"✅ Agent completed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    print()
    
    print("Next steps:")
    print("  1. Review findings above")
    print("  2. Update content as needed")
    print("  3. Run again weekly or monthly")
    print("  4. Consider automating with GitHub Actions")
    print()


if __name__ == "__main__":
    main()

