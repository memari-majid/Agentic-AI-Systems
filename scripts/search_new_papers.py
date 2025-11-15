#!/usr/bin/env python3
"""
Automated Paper Discovery for Agentic AI Review
Searches multiple sources for relevant new papers
"""

import requests
import json
from datetime import datetime, timedelta
from typing import List, Dict
import argparse
import sys

class PaperSearcher:
    """Search for academic papers from multiple sources"""
    
    def __init__(self, days_back=7):
        self.days_back = days_back
        self.cutoff_date = datetime.now() - timedelta(days=days_back)
        self.papers = []
        
    def search_arxiv(self, query: str, max_results=20) -> List[Dict]:
        """Search arXiv for recent papers"""
        print(f"Searching arXiv for: {query}")
        
        base_url = "http://export.arxiv.org/api/query"
        params = {
            'search_query': f'all:{query}',
            'start': 0,
            'max_results': max_results,
            'sortBy': 'submittedDate',
            'sortOrder': 'descending'
        }
        
        try:
            response = requests.get(base_url, params=params)
            response.raise_for_status()
            
            # Parse XML response (simplified - would need proper XML parsing)
            papers = self._parse_arxiv_response(response.text)
            return papers
        except Exception as e:
            print(f"Error searching arXiv: {e}")
            return []
    
    def _parse_arxiv_response(self, xml_text: str) -> List[Dict]:
        """Parse arXiv API XML response (simplified)"""
        import xml.etree.ElementTree as ET
        
        papers = []
        try:
            root = ET.fromstring(xml_text)
            ns = {'atom': 'http://www.w3.org/2005/Atom'}
            
            for entry in root.findall('atom:entry', ns):
                title = entry.find('atom:title', ns)
                published = entry.find('atom:published', ns)
                summary = entry.find('atom:summary', ns)
                
                authors = []
                for author in entry.findall('atom:author', ns):
                    name = author.find('atom:name', ns)
                    if name is not None:
                        authors.append(name.text)
                
                links = entry.findall('atom:link', ns)
                pdf_url = None
                for link in links:
                    if link.get('title') == 'pdf':
                        pdf_url = link.get('href')
                        break
                
                if title is not None and published is not None:
                    paper = {
                        'title': title.text.strip(),
                        'authors': authors,
                        'published': published.text,
                        'summary': summary.text.strip() if summary is not None else '',
                        'pdf_url': pdf_url or '',
                        'source': 'arXiv'
                    }
                    papers.append(paper)
        except Exception as e:
            print(f"Error parsing arXiv response: {e}")
        
        return papers
    
    def search_semantic_scholar(self, query: str, limit=20) -> List[Dict]:
        """Search Semantic Scholar API"""
        print(f"Searching Semantic Scholar for: {query}")
        
        base_url = "https://api.semanticscholar.org/graph/v1/paper/search"
        params = {
            'query': query,
            'limit': limit,
            'fields': 'title,authors,year,abstract,url,citationCount,publicationDate'
        }
        
        try:
            response = requests.get(base_url, params=params)
            response.raise_for_status()
            data = response.json()
            
            papers = []
            for item in data.get('data', []):
                # Filter by date
                if 'publicationDate' in item:
                    pub_date = datetime.strptime(item['publicationDate'], '%Y-%m-%d')
                    if pub_date < self.cutoff_date:
                        continue
                
                authors = [a.get('name', '') for a in item.get('authors', [])]
                paper = {
                    'title': item.get('title', ''),
                    'authors': authors,
                    'published': item.get('publicationDate', ''),
                    'summary': item.get('abstract', '')[:300] if item.get('abstract') else '',
                    'citations': item.get('citationCount', 0),
                    'url': item.get('url', ''),
                    'source': 'Semantic Scholar'
                }
                papers.append(paper)
            
            return papers
        except Exception as e:
            print(f"Error searching Semantic Scholar: {e}")
            return []
    
    def search_all_sources(self, queries: List[str]) -> List[Dict]:
        """Search all sources with given queries"""
        all_papers = []
        
        for query in queries:
            # Search arXiv
            arxiv_papers = self.search_arxiv(query, max_results=10)
            all_papers.extend(arxiv_papers)
            
            # Search Semantic Scholar
            ss_papers = self.search_semantic_scholar(query, limit=10)
            all_papers.extend(ss_papers)
        
        # Remove duplicates based on title
        unique_papers = {}
        for paper in all_papers:
            title = paper['title'].lower().strip()
            if title not in unique_papers:
                unique_papers[title] = paper
        
        return list(unique_papers.values())
    
    def filter_by_quality(self, papers: List[Dict]) -> List[Dict]:
        """Filter papers by quality criteria"""
        filtered = []
        
        for paper in papers:
            # Skip if too old
            if paper.get('published'):
                try:
                    pub_date = datetime.fromisoformat(paper['published'].split('T')[0])
                    if pub_date < self.cutoff_date:
                        continue
                except:
                    pass
            
            # Skip if title doesn't seem relevant
            title_lower = paper['title'].lower()
            relevant_terms = ['agent', 'agentic', 'autonomous', 'llm', 'language model', 
                            'multi-agent', 'reasoning', 'planning', 'tool']
            if not any(term in title_lower for term in relevant_terms):
                continue
            
            filtered.append(paper)
        
        return filtered
    
    def generate_report(self, papers: List[Dict], output_file='new_papers.md') -> str:
        """Generate markdown report"""
        report = f"# Weekly Paper Review - {datetime.now().date()}\n\n"
        report += f"**Search Date**: {datetime.now().strftime('%Y-%m-%d')}\n"
        report += f"**Papers Found**: {len(papers)}\n"
        report += f"**Time Window**: Last {self.days_back} days\n\n"
        report += "---\n\n"
        
        if not papers:
            report += "No new papers found matching criteria.\n"
            return report
        
        # Sort by publication date (most recent first)
        sorted_papers = sorted(papers, key=lambda x: x.get('published', ''), reverse=True)
        
        for i, paper in enumerate(sorted_papers, 1):
            report += f"## {i}. {paper['title']}\n\n"
            
            # Authors
            authors = paper.get('authors', [])
            if authors:
                author_str = ', '.join(authors[:3])
                if len(authors) > 3:
                    author_str += f" et al. ({len(authors)} authors)"
                report += f"**Authors**: {author_str}\n\n"
            
            # Publication info
            if paper.get('published'):
                report += f"**Published**: {paper['published'].split('T')[0]}\n\n"
            
            report += f"**Source**: {paper['source']}\n\n"
            
            # Citations (if available)
            if paper.get('citations'):
                report += f"**Citations**: {paper['citations']}\n\n"
            
            # Summary
            summary = paper.get('summary', '')
            if summary:
                # Clean up summary
                summary = ' '.join(summary.split())[:400]
                report += f"**Summary**: {summary}...\n\n"
            
            # Link
            url = paper.get('pdf_url') or paper.get('url', '')
            if url:
                report += f"**Link**: [{url}]({url})\n\n"
            
            # Quick assessment section
            report += "**Quick Assessment**:\n"
            report += "- [ ] Relevant to review scope\n"
            report += "- [ ] Peer-reviewed/quality venue\n"
            report += "- [ ] Adds new insights\n"
            report += "- [ ] Integration priority: [ ] High / [ ] Medium / [ ] Low\n\n"
            
            report += "**Potential Sections**: \n\n"
            report += "**Notes**: \n\n"
            report += "---\n\n"
        
        # Save report
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"\nReport saved to: {output_file}")
        return report

def main():
    parser = argparse.ArgumentParser(description='Search for new papers on Agentic AI')
    parser.add_argument('--days', type=int, default=7, help='Days to look back (default: 7)')
    parser.add_argument('--output', type=str, default='new_papers.md', help='Output file')
    parser.add_argument('--verbose', action='store_true', help='Verbose output')
    
    args = parser.parse_args()
    
    # Search queries
    queries = [
        "agentic AI",
        "autonomous agents large language models",
        "multi-agent systems LLM",
        "tool use language models",
        "ReAct reasoning acting",
        "AI agent planning",
        "agent memory systems",
        "LLM agent coordination"
    ]
    
    print("="*60)
    print("Agentic AI Paper Discovery System")
    print("="*60)
    print(f"Searching for papers from the last {args.days} days...")
    print()
    
    searcher = PaperSearcher(days_back=args.days)
    
    # Search all sources
    papers = searcher.search_all_sources(queries)
    print(f"\nTotal papers found: {len(papers)}")
    
    # Filter by quality
    filtered_papers = searcher.filter_by_quality(papers)
    print(f"After filtering: {len(filtered_papers)} papers")
    
    # Generate report
    if filtered_papers:
        report = searcher.generate_report(filtered_papers, args.output)
        print("\n" + "="*60)
        print("SUMMARY")
        print("="*60)
        print(f"Papers to review: {len(filtered_papers)}")
        print(f"Report: {args.output}")
        print("\nNext steps:")
        print("1. Review papers in the report")
        print("2. Assess quality and relevance")
        print("3. Integrate high-priority papers")
        print("4. Update references.bib")
    else:
        print("\nNo papers found matching criteria.")
        print("Try:")
        print("- Expanding the time window (--days 14)")
        print("- Checking search queries")
        print("- Running again in a few days")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nSearch interrupted by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\nError: {e}")
        sys.exit(1)

