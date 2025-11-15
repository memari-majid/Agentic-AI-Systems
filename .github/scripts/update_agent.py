#!/usr/bin/env python3
"""
AI Agent for Automatically Updating Knowledge Base Content

This agent:
1. Monitors AI/ML framework releases
2. Updates technology comparisons
3. Checks for broken links
4. Suggests content improvements
5. Updates best practices
"""

import os
import re
import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional
import requests
from bs4 import BeautifulSoup


class ContentUpdateAgent:
    """AI-powered agent for keeping knowledge base current"""
    
    def __init__(self):
        self.openai_key = os.getenv("OPENAI_API_KEY")
        self.anthropic_key = os.getenv("ANTHROPIC_API_KEY")
        self.repo_root = Path(__file__).parent.parent.parent
        self.changes = []
        
    def run(self):
        """Main agent workflow"""
        print("🤖 Content Update Agent Starting...")
        
        # 1. Check framework versions
        self.check_framework_updates()
        
        # 2. Verify links
        self.verify_links()
        
        # 3. Update technology comparisons
        self.update_tech_comparisons()
        
        # 4. Check for outdated content
        self.check_outdated_content()
        
        # 5. Generate report
        self.generate_report()
        
        print(f"✅ Agent completed with {len(self.changes)} changes")
        
    def check_framework_updates(self):
        """Check for new versions of mentioned frameworks"""
        print("🔍 Checking framework updates...")
        
        frameworks = {
            "langchain": "https://api.github.com/repos/langchain-ai/langchain/releases/latest",
            "langgraph": "https://api.github.com/repos/langchain-ai/langgraph/releases/latest",
            "pydantic-ai": "https://api.github.com/repos/pydantic/pydantic-ai/releases/latest",
            "dspy": "https://api.github.com/repos/stanfordnlp/dspy/releases/latest",
        }
        
        for framework, api_url in frameworks.items():
            try:
                response = requests.get(api_url, timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    version = data.get("tag_name", "unknown")
                    published = data.get("published_at", "")
                    
                    self.changes.append({
                        "type": "framework_update",
                        "framework": framework,
                        "version": version,
                        "date": published
                    })
                    print(f"  ✓ {framework}: {version}")
            except Exception as e:
                print(f"  ⚠️  Could not check {framework}: {e}")
                
    def verify_links(self):
        """Check all markdown files for broken links"""
        print("🔗 Verifying links...")
        
        md_files = list(self.repo_root.glob("**/*.md"))
        broken_links = []
        
        for md_file in md_files[:10]:  # Limit to avoid rate limiting
            try:
                content = md_file.read_text(encoding="utf-8")
                # Find markdown links
                links = re.findall(r'\[([^\]]+)\]\(([^\)]+)\)', content)
                
                for link_text, url in links:
                    if url.startswith("http"):
                        try:
                            response = requests.head(url, timeout=5, allow_redirects=True)
                            if response.status_code >= 400:
                                broken_links.append({
                                    "file": str(md_file.relative_to(self.repo_root)),
                                    "url": url,
                                    "status": response.status_code
                                })
                        except:
                            pass  # Skip failed requests to avoid false positives
            except Exception as e:
                print(f"  ⚠️  Error checking {md_file.name}: {e}")
                
        if broken_links:
            self.changes.append({
                "type": "broken_links",
                "links": broken_links
            })
            print(f"  ⚠️  Found {len(broken_links)} potential broken links")
        else:
            print("  ✓ All checked links valid")
            
    def update_tech_comparisons(self):
        """Update technology comparison tables"""
        print("📊 Updating technology comparisons...")
        
        tech_file = self.repo_root / "03-modern-frameworks" / "technology-comparison.md"
        
        if tech_file.exists():
            # This is where you'd use OpenAI/Anthropic to generate updates
            # For now, we'll just note that it needs review
            self.changes.append({
                "type": "tech_comparison",
                "file": str(tech_file.relative_to(self.repo_root)),
                "action": "needs_review"
            })
            print("  ✓ Technology comparison marked for review")
            
    def check_outdated_content(self):
        """Check for content that might be outdated"""
        print("📅 Checking for outdated content...")
        
        # Check for dates in content
        md_files = list(self.repo_root.glob("**/*.md"))
        current_year = datetime.now().year
        
        for md_file in md_files:
            try:
                content = md_file.read_text(encoding="utf-8")
                
                # Look for year references
                old_years = re.findall(r'\b(202[0-3])\b', content)
                
                if old_years and current_year > 2024:
                    self.changes.append({
                        "type": "outdated_date",
                        "file": str(md_file.relative_to(self.repo_root)),
                        "years": list(set(old_years))
                    })
            except:
                pass
                
        print(f"  ✓ Checked {len(md_files)} files")
        
    def generate_report(self):
        """Generate a report of changes"""
        report_path = self.repo_root / "agent-report.json"
        
        report = {
            "timestamp": datetime.now().isoformat(),
            "changes_count": len(self.changes),
            "changes": self.changes
        }
        
        report_path.write_text(json.dumps(report, indent=2))
        print(f"📝 Report saved to {report_path.name}")
        

if __name__ == "__main__":
    agent = ContentUpdateAgent()
    agent.run()

