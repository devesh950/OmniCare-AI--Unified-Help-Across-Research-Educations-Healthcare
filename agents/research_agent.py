import requests
from bs4 import BeautifulSoup
import json
from typing import List, Dict
import time
from urllib.parse import quote_plus

class ResearchAgent:
    """
    Research Agent that searches the web for information on given topics.
    Uses multiple search strategies and sources.
    """
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
    
    def search(self, query: str, max_results: int = 5) -> List[Dict]:
        """
        Search for information on the given query.
        
        Args:
            query: The search query
            max_results: Maximum number of results to return
            
        Returns:
            List of search results with title, url, and snippet
        """
        results = []
        
        try:
            # Method 1: Use DuckDuckGo HTML search (no API key needed)
            ddg_results = self._search_duckduckgo(query, max_results)
            results.extend(ddg_results)
            
            # Method 2: Search Wikipedia for additional context
            wiki_results = self._search_wikipedia(query)
            results.extend(wiki_results)
            
            # Method 3: If OpenAI API key provided, use it for enhanced search
            if self.api_key:
                enhanced_results = self._enhance_with_ai(query, results)
                return enhanced_results[:max_results]
            
            return results[:max_results]
            
        except Exception as e:
            print(f"Search error: {e}")
            # Return fallback results
            return self._generate_fallback_results(query, max_results)
    
    def _search_duckduckgo(self, query: str, max_results: int) -> List[Dict]:
        """Search using DuckDuckGo HTML"""
        results = []
        try:
            url = f"https://html.duckduckgo.com/html/?q={quote_plus(query)}"
            response = requests.get(url, headers=self.headers, timeout=10)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                search_results = soup.find_all('div', class_='result')
                
                for result in search_results[:max_results]:
                    try:
                        title_elem = result.find('a', class_='result__a')
                        snippet_elem = result.find('a', class_='result__snippet')
                        
                        if title_elem and snippet_elem:
                            title = title_elem.get_text(strip=True)
                            url = title_elem.get('href', '')
                            snippet = snippet_elem.get_text(strip=True)
                            
                            results.append({
                                'title': title,
                                'url': url,
                                'snippet': snippet,
                                'source': 'DuckDuckGo'
                            })
                    except:
                        continue
        except Exception as e:
            print(f"DuckDuckGo search error: {e}")
        
        return results
    
    def _search_wikipedia(self, query: str) -> List[Dict]:
        """Search Wikipedia for relevant articles"""
        results = []
        try:
            # Wikipedia API search
            search_url = f"https://en.wikipedia.org/w/api.php"
            params = {
                'action': 'opensearch',
                'search': query,
                'limit': 2,
                'format': 'json'
            }
            
            response = requests.get(search_url, params=params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                titles = data[1]
                descriptions = data[2]
                urls = data[3]
                
                for i in range(len(titles)):
                    results.append({
                        'title': f"{titles[i]} (Wikipedia)",
                        'url': urls[i],
                        'snippet': descriptions[i] if i < len(descriptions) else "Wikipedia article",
                        'source': 'Wikipedia'
                    })
        except Exception as e:
            print(f"Wikipedia search error: {e}")
        
        return results
    
    def _enhance_with_ai(self, query: str, results: List[Dict]) -> List[Dict]:
        """Use OpenAI to enhance and rank search results"""
        try:
            import openai
            openai.api_key = self.api_key
            
            # Create a summary of results for AI ranking
            results_text = "\n".join([
                f"{i+1}. {r['title']}: {r['snippet'][:100]}"
                for i, r in enumerate(results)
            ])
            
            # Ask AI to rank and enhance
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a research assistant. Rank these search results by relevance."},
                    {"role": "user", "content": f"Query: {query}\n\nResults:\n{results_text}\n\nReturn the numbers of the most relevant results in order."}
                ],
                max_tokens=100
            )
            
            # Parse AI response and reorder results
            # For simplicity, return original results
            return results
            
        except Exception as e:
            print(f"AI enhancement error: {e}")
            return results
    
    def _generate_fallback_results(self, query: str, max_results: int) -> List[Dict]:
        """Generate fallback results when search fails"""
        return [
            {
                'title': f"Research on: {query}",
                'url': f"https://www.google.com/search?q={quote_plus(query)}",
                'snippet': f"Information about {query}. This is a fallback result as the main search encountered issues. Please try refining your query or check your internet connection.",
                'source': 'Fallback'
            },
            {
                'title': f"{query} - Overview",
                'url': f"https://en.wikipedia.org/wiki/{query.replace(' ', '_')}",
                'snippet': f"General information and overview of {query}. For best results, ensure you have an active internet connection.",
                'source': 'Fallback'
            },
            {
                'title': f"Latest news about {query}",
                'url': f"https://news.google.com/search?q={quote_plus(query)}",
                'snippet': f"Recent news and updates related to {query}. This is a generated result.",
                'source': 'Fallback'
            }
        ][:max_results]
    
    def fetch_content(self, url: str) -> str:
        """Fetch and extract text content from a URL"""
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Remove script and style elements
                for script in soup(["script", "style"]):
                    script.decompose()
                
                # Get text
                text = soup.get_text()
                
                # Clean up text
                lines = (line.strip() for line in text.splitlines())
                chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
                text = ' '.join(chunk for chunk in chunks if chunk)
                
                return text[:5000]  # Return first 5000 characters
        except Exception as e:
            print(f"Content fetch error for {url}: {e}")
            return ""
