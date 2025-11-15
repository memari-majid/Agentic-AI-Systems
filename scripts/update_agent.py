#!/usr/bin/env python3
"""
Automated Update Agent for Agentic AI Systems Review
Uses OpenAI API to search for and analyze updates to the review content.
"""

import os
import json
import asyncio
import aiohttp
from datetime import datetime, timedelta
from typing import List, Dict, Any
from openai import OpenAI
import requests
from pathlib import Path

class UpdateAgent:
    """Agent to automatically check for updates to the Agentic AI Systems review."""
    
    def __init__(self):
        self.api_key = os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY environment variable is required")
        
        self.client = OpenAI(api_key=self.api_key)
        self.github_token = os.getenv('GITHUB_TOKEN')
        self.repo = os.getenv('GITHUB_REPOSITORY', 'memari-majid/Agentic-AI-Systems')
        
        # Load search prompts
        self.search_prompts = self.load_search_prompts()
        
        # Results storage
        self.findings = {
            'new_papers': [],
            'framework_updates': [],
            'broken_links': [],
            'content_suggestions': [],
            'timestamp': datetime.now().isoformat()
        }
    
    def load_search_prompts(self) -> List[str]:
        """Load search prompts from the SEARCH-PROMPTS-FOR-IMPROVEMENT.md file."""
        prompts_file = Path('arxiv-paper/SEARCH-PROMPTS-FOR-IMPROVEMENT.md')
        
        if not prompts_file.exists():
            print("⚠️  Search prompts file not found, using default prompts")
            return self.get_default_prompts()
        
        prompts = []
        with open(prompts_file, 'r') as f:
            content = f.read()
            # Extract prompts (lines starting with **Prompt**:)
            lines = content.split('\n')
            for line in lines:
                if line.strip().startswith('**Prompt**:'):
                    prompt = line.split('**Prompt**:')[1].strip().strip('"')
                    prompts.append(prompt)
        
        return prompts[:15]  # Limit to first 15 prompts to avoid API costs
    
    def get_default_prompts(self) -> List[str]:
        """Default search prompts if file is not available."""
        return [
            "Survey of Large Language Model based Autonomous Agents 2024 2025 arXiv",
            "Comprehensive review agentic AI systems LLM agents 2024",
            "Tree of Thoughts Graph of Thoughts reasoning LLM 2024",
            "MemGPT long-term memory systems LLM agents",
            "ReAct ReWOO tool use planning agents 2024",
            "LangChain LangGraph Pydantic AI framework updates 2024",
            "Multi-agent coordination GPT Swarm CAMEL 2024",
            "Self-RAG CRAG Corrective RAG active retrieval 2024",
            "AgentBench WebArena agent evaluation benchmark",
            "GPT-4V multimodal agents vision-language reasoning 2024"
        ]
    
    async def search_arxiv(self, query: str, max_results: int = 5) -> List[Dict[str, Any]]:
        """Search arXiv for recent papers."""
        # Calculate date 6 months ago
        six_months_ago = (datetime.now() - timedelta(days=180)).strftime('%Y%m%d')
        
        url = 'http://export.arxiv.org/api/query'
        params = {
            'search_query': f'all:{query}',
            'start': 0,
            'max_results': max_results,
            'sortBy': 'lastUpdatedDate',
            'sortOrder': 'descending'
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, params=params) as response:
                    if response.status == 200:
                        text = await response.text()
                        return self.parse_arxiv_response(text)
        except Exception as e:
            print(f"⚠️  Error searching arXiv: {e}")
        
        return []
    
    def parse_arxiv_response(self, xml_text: str) -> List[Dict[str, Any]]:
        """Parse arXiv API XML response."""
        # Simple XML parsing (in production, use xml.etree.ElementTree)
        papers = []
        entries = xml_text.split('<entry>')
        
        for entry in entries[1:]:  # Skip first split (header)
            if '</entry>' not in entry:
                continue
            
            paper = {}
            
            # Extract title
            if '<title>' in entry:
                title = entry.split('<title>')[1].split('</title>')[0].strip()
                paper['title'] = ' '.join(title.split())  # Normalize whitespace
            
            # Extract id/link
            if '<id>' in entry:
                paper['url'] = entry.split('<id>')[1].split('</id>')[0].strip()
            
            # Extract published date
            if '<published>' in entry:
                paper['published'] = entry.split('<published>')[1].split('</published>')[0].strip()
            
            # Extract authors
            authors = []
            author_entries = entry.split('<author>')
            for author_entry in author_entries[1:]:
                if '<name>' in author_entry:
                    name = author_entry.split('<name>')[1].split('</name>')[0].strip()
                    authors.append(name)
            paper['authors'] = authors
            
            # Extract summary
            if '<summary>' in entry:
                summary = entry.split('<summary>')[1].split('</summary>')[0].strip()
                paper['summary'] = ' '.join(summary.split())[:300]  # First 300 chars
            
            papers.append(paper)
        
        return papers
    
    async def analyze_paper_relevance(self, paper: Dict[str, Any]) -> Dict[str, Any]:
        """Use OpenAI to analyze if a paper is relevant to the review."""
        try:
            prompt = f"""Analyze if this research paper is relevant to a comprehensive review on Agentic AI Systems.
            
Paper Title: {paper.get('title', 'Unknown')}
Summary: {paper.get('summary', 'No summary available')}

Consider:
1. Is it about AI agents, LLM-based agents, or autonomous systems?
2. Does it introduce new techniques, frameworks, or insights?
3. Would it add value to a comprehensive review paper?

Respond with JSON:
{{
    "relevant": true/false,
    "relevance_score": 0-10,
    "reason": "brief explanation",
    "suggested_section": "which section of the paper this belongs to"
}}"""
            
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",  # Using cheaper model for analysis
                messages=[
                    {"role": "system", "content": "You are an expert in AI agent systems and academic paper review."},
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"},
                temperature=0.3
            )
            
            analysis = json.loads(response.choices[0].message.content)
            paper['analysis'] = analysis
            return paper
            
        except Exception as e:
            print(f"⚠️  Error analyzing paper: {e}")
            return paper
    
    async def check_framework_updates(self) -> List[Dict[str, Any]]:
        """Check for updates to major frameworks mentioned in the review."""
        frameworks = [
            {'name': 'LangChain', 'pypi': 'langchain', 'github': 'langchain-ai/langchain'},
            {'name': 'LangGraph', 'pypi': 'langgraph', 'github': 'langchain-ai/langgraph'},
            {'name': 'Pydantic AI', 'pypi': 'pydantic-ai', 'github': 'pydantic/pydantic-ai'},
            {'name': 'DSPy', 'pypi': 'dspy-ai', 'github': 'stanfordnlp/dspy'},
            {'name': 'AutoGPT', 'github': 'Significant-Gravitas/AutoGPT'},
            {'name': 'CrewAI', 'pypi': 'crewai', 'github': 'joaomdmoura/crewAI'},
        ]
        
        updates = []
        
        for framework in frameworks:
            try:
                # Check PyPI version if available
                if 'pypi' in framework:
                    url = f"https://pypi.org/pypi/{framework['pypi']}/json"
                    async with aiohttp.ClientSession() as session:
                        async with session.get(url) as response:
                            if response.status == 200:
                                data = await response.json()
                                latest_version = data['info']['version']
                                release_date = list(data['releases'][latest_version])[0]['upload_time']
                                
                                updates.append({
                                    'framework': framework['name'],
                                    'version': latest_version,
                                    'release_date': release_date,
                                    'url': data['info']['project_urls'].get('Homepage', '')
                                })
                
                # Add small delay to avoid rate limiting
                await asyncio.sleep(0.5)
                
            except Exception as e:
                print(f"⚠️  Error checking {framework['name']}: {e}")
        
        return updates
    
    def verify_links_in_file(self, filepath: Path) -> List[Dict[str, Any]]:
        """Verify links in a markdown file."""
        broken_links = []
        
        if not filepath.exists():
            return broken_links
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Simple markdown link extraction: [text](url)
            import re
            links = re.findall(r'\[([^\]]+)\]\(([^\)]+)\)', content)
            
            for text, url in links[:20]:  # Limit to first 20 links
                # Skip anchors and relative paths
                if url.startswith('#') or url.startswith('/') or not url.startswith('http'):
                    continue
                
                try:
                    response = requests.head(url, timeout=5, allow_redirects=True)
                    if response.status_code >= 400:
                        broken_links.append({
                            'file': str(filepath),
                            'text': text,
                            'url': url,
                            'status': response.status_code
                        })
                except Exception as e:
                    broken_links.append({
                        'file': str(filepath),
                        'text': text,
                        'url': url,
                        'error': str(e)
                    })
                
                # Rate limiting
                import time
                time.sleep(0.3)
        
        except Exception as e:
            print(f"⚠️  Error verifying links in {filepath}: {e}")
        
        return broken_links
    
    async def generate_content_suggestions(self) -> List[str]:
        """Use OpenAI to generate suggestions for content improvements."""
        try:
            # Read current paper content
            paper_file = Path('arxiv-paper/paper.tex')
            readme_file = Path('README.md')
            
            context = ""
            if paper_file.exists():
                with open(paper_file, 'r') as f:
                    # Read first 5000 characters
                    context += f"Paper excerpt:\n{f.read(5000)}\n\n"
            
            if readme_file.exists():
                with open(readme_file, 'r') as f:
                    context += f"README:\n{f.read()}\n\n"
            
            prompt = f"""Based on this Agentic AI Systems review content, suggest 5 specific improvements or topics that should be added to keep it up-to-date with the latest developments in 2025.

{context}

Focus on:
1. Missing recent frameworks or tools
2. Emerging research directions
3. New benchmark or evaluation methods
4. Production deployment best practices
5. Recent breakthrough papers

Provide specific, actionable suggestions."""
            
            response = self.client.chat.completions.create(
                model="gpt-4o",  # Using advanced model for strategic suggestions
                messages=[
                    {"role": "system", "content": "You are an expert in AI agent systems and stay current with the latest research and developments."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1000
            )
            
            suggestions_text = response.choices[0].message.content
            
            # Parse suggestions (assuming numbered list)
            suggestions = [s.strip() for s in suggestions_text.split('\n') if s.strip() and (s.strip()[0].isdigit() or s.strip().startswith('-'))]
            
            return suggestions
            
        except Exception as e:
            print(f"⚠️  Error generating suggestions: {e}")
            return []
    
    async def run(self):
        """Run the complete update check process."""
        print("🤖 Starting Agentic AI Systems Update Agent...")
        print(f"📅 Timestamp: {datetime.now().isoformat()}")
        print(f"🔍 Loaded {len(self.search_prompts)} search prompts\n")
        
        # 1. Search for new papers
        print("📚 Searching for new research papers...")
        relevant_papers = []
        
        for i, prompt in enumerate(self.search_prompts[:10], 1):  # Limit to 10 searches
            print(f"  [{i}/10] Searching: {prompt[:60]}...")
            papers = await self.search_arxiv(prompt, max_results=3)
            
            for paper in papers:
                analyzed = await self.analyze_paper_relevance(paper)
                if analyzed.get('analysis', {}).get('relevant', False):
                    relevant_papers.append(analyzed)
            
            # Rate limiting
            await asyncio.sleep(1)
        
        # Remove duplicates by URL
        seen_urls = set()
        unique_papers = []
        for paper in relevant_papers:
            url = paper.get('url', '')
            if url and url not in seen_urls:
                seen_urls.add(url)
                unique_papers.append(paper)
        
        self.findings['new_papers'] = sorted(
            unique_papers, 
            key=lambda x: x.get('analysis', {}).get('relevance_score', 0),
            reverse=True
        )[:15]  # Top 15 papers
        
        print(f"✅ Found {len(self.findings['new_papers'])} relevant papers\n")
        
        # 2. Check framework updates
        print("🔧 Checking framework updates...")
        self.findings['framework_updates'] = await self.check_framework_updates()
        print(f"✅ Checked {len(self.findings['framework_updates'])} frameworks\n")
        
        # 3. Verify links (sample)
        print("🔗 Verifying links...")
        key_files = [
            Path('README.md'),
            Path('arxiv-paper/paper.tex')
        ]
        
        for file in key_files:
            if file.exists():
                broken = self.verify_links_in_file(file)
                self.findings['broken_links'].extend(broken)
        
        print(f"✅ Found {len(self.findings['broken_links'])} broken links\n")
        
        # 4. Generate content suggestions
        print("💡 Generating content suggestions...")
        self.findings['content_suggestions'] = await self.generate_content_suggestions()
        print(f"✅ Generated {len(self.findings['content_suggestions'])} suggestions\n")
        
        # 5. Generate report
        self.generate_report()
        
        print("✨ Update check complete!")
    
    def generate_report(self):
        """Generate a markdown report of findings."""
        report = f"""# Agentic AI Systems - Automated Update Report

**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}

## 📊 Summary

- **New Papers Found**: {len(self.findings['new_papers'])}
- **Framework Updates**: {len(self.findings['framework_updates'])}
- **Broken Links**: {len(self.findings['broken_links'])}
- **Content Suggestions**: {len(self.findings['content_suggestions'])}

---

## 📚 New Relevant Papers

"""
        
        if self.findings['new_papers']:
            for i, paper in enumerate(self.findings['new_papers'][:10], 1):
                analysis = paper.get('analysis', {})
                report += f"""### {i}. {paper.get('title', 'Unknown Title')}

- **Authors**: {', '.join(paper.get('authors', [])[:3])}
- **Published**: {paper.get('published', 'Unknown')[:10]}
- **Relevance Score**: {analysis.get('relevance_score', 0)}/10
- **Reason**: {analysis.get('reason', 'N/A')}
- **Suggested Section**: {analysis.get('suggested_section', 'N/A')}
- **URL**: {paper.get('url', 'N/A')}

"""
        else:
            report += "*No new highly relevant papers found in this update cycle.*\n\n"
        
        report += "---\n\n## 🔧 Framework Updates\n\n"
        
        if self.findings['framework_updates']:
            for update in self.findings['framework_updates']:
                report += f"- **{update['framework']}**: v{update['version']} (released {update['release_date'][:10]})\n"
        else:
            report += "*No framework updates detected.*\n"
        
        report += "\n---\n\n## 🔗 Broken Links\n\n"
        
        if self.findings['broken_links']:
            for link in self.findings['broken_links'][:10]:
                status = link.get('status', link.get('error', 'Unknown'))
                report += f"- **File**: `{link['file']}`\n  - Text: {link['text']}\n  - URL: {link['url']}\n  - Status: {status}\n\n"
        else:
            report += "*No broken links detected.*\n"
        
        report += "\n---\n\n## 💡 Content Improvement Suggestions\n\n"
        
        if self.findings['content_suggestions']:
            for i, suggestion in enumerate(self.findings['content_suggestions'], 1):
                report += f"{i}. {suggestion}\n"
        else:
            report += "*No specific suggestions generated.*\n"
        
        report += f"\n---\n\n## 🎯 Action Items\n\n"
        
        if self.findings['new_papers']:
            report += f"1. **Review Top Papers**: Evaluate the {min(5, len(self.findings['new_papers']))} highest-scoring papers for inclusion\n"
        
        if self.findings['framework_updates']:
            report += f"2. **Update Framework Versions**: Review and update framework version references\n"
        
        if self.findings['broken_links']:
            report += f"3. **Fix Broken Links**: Update or remove {len(self.findings['broken_links'])} broken links\n"
        
        if self.findings['content_suggestions']:
            report += f"4. **Consider Suggestions**: Review and implement relevant content improvements\n"
        
        if not any([self.findings['new_papers'], self.findings['framework_updates'], 
                   self.findings['broken_links'], self.findings['content_suggestions']]):
            report += "*No significant updates found. The review appears to be current.*\n"
        
        report += "\n---\n\n*This report was automatically generated by the Agentic AI Systems Update Agent.*\n"
        
        # Save report
        with open('update_report.md', 'w') as f:
            f.write(report)
        
        # Save JSON findings
        with open('update_suggestions.json', 'w') as f:
            json.dump(self.findings, f, indent=2)
        
        print(f"📝 Report saved to update_report.md")
        print(f"💾 Findings saved to update_suggestions.json")


async def main():
    """Main entry point."""
    try:
        agent = UpdateAgent()
        await agent.run()
    except Exception as e:
        print(f"❌ Error running update agent: {e}")
        raise


if __name__ == '__main__':
    asyncio.run(main())

