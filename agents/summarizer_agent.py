from typing import List, Dict
import re

class SummarizerAgent:
    """
    Summarizer Agent that analyzes and summarizes research findings.
    Uses multiple strategies for text summarization.
    """
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key
    
    def summarize(self, search_results: List[Dict], length: str = "Medium") -> str:
        """
        Summarize search results into a coherent summary.
        
        Args:
            search_results: List of search results with title, url, and snippet
            length: Summary length - "Short", "Medium", or "Detailed"
            
        Returns:
            A coherent summary of the research findings
        """
        if not search_results:
            return "No results found to summarize."
        
        # Extract all snippets
        snippets = [result.get('snippet', '') for result in search_results]
        titles = [result.get('title', '') for result in search_results]
        
        # Combine information
        combined_text = " ".join(snippets)
        
        # If OpenAI API key is provided, use it for better summarization
        if self.api_key:
            return self._summarize_with_ai(combined_text, titles, length)
        
        # Otherwise use extractive summarization
        return self._extractive_summarize(combined_text, titles, length)
    
    def _summarize_with_ai(self, text: str, titles: List[str], length: str) -> str:
        """Use OpenAI to generate summary"""
        try:
            import openai
            openai.api_key = self.api_key
            
            # Determine max tokens based on length
            max_tokens = {
                "Short": 150,
                "Medium": 300,
                "Detailed": 500
            }.get(length, 300)
            
            prompt = f"Summarize the following research findings:\n\n{text[:3000]}\n\nProvide a {length.lower()} summary."
            
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a research analyst. Provide clear, concise summaries."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=max_tokens,
                temperature=0.7
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            print(f"AI summarization error: {e}")
            return self._extractive_summarize(text, titles, length)
    
    def _extractive_summarize(self, text: str, titles: List[str], length: str) -> str:
        """Create summary using extractive methods"""
        
        # Clean text
        text = self._clean_text(text)
        
        # Split into sentences
        sentences = self._split_sentences(text)
        
        # Determine number of sentences based on length
        num_sentences = {
            "Short": 3,
            "Medium": 5,
            "Detailed": 8
        }.get(length, 5)
        
        # Score sentences
        scored_sentences = self._score_sentences(sentences, titles)
        
        # Select top sentences
        top_sentences = sorted(scored_sentences, key=lambda x: x[1], reverse=True)[:num_sentences]
        
        # Sort by original order
        top_sentences.sort(key=lambda x: x[2])
        
        # Combine sentences
        summary = " ".join([sent[0] for sent in top_sentences])
        
        if not summary:
            # Fallback: use beginning of text
            summary = " ".join(sentences[:num_sentences])
        
        return summary.strip() or "Unable to generate summary from the available information."
    
    def _clean_text(self, text: str) -> str:
        """Clean and normalize text"""
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        # Remove special characters but keep punctuation
        text = re.sub(r'[^\w\s.,!?;:\-]', '', text)
        return text.strip()
    
    def _split_sentences(self, text: str) -> List[str]:
        """Split text into sentences"""
        # Simple sentence splitting
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if len(s.strip()) > 20]
        return sentences
    
    def _score_sentences(self, sentences: List[str], titles: List[str]) -> List[tuple]:
        """Score sentences based on relevance"""
        scored = []
        
        # Extract keywords from titles
        keywords = set()
        for title in titles:
            words = re.findall(r'\b\w+\b', title.lower())
            keywords.update([w for w in words if len(w) > 4])
        
        for idx, sentence in enumerate(sentences):
            score = 0
            sentence_lower = sentence.lower()
            
            # Score based on keyword presence
            for keyword in keywords:
                if keyword in sentence_lower:
                    score += 2
            
            # Score based on sentence length (prefer medium length)
            word_count = len(sentence.split())
            if 10 <= word_count <= 25:
                score += 1
            
            # Score based on position (earlier sentences often more important)
            if idx < len(sentences) * 0.3:
                score += 1
            
            # Check for important phrases
            important_phrases = ['research shows', 'study found', 'according to', 'important', 'significant']
            for phrase in important_phrases:
                if phrase in sentence_lower:
                    score += 1
            
            scored.append((sentence, score, idx))
        
        return scored
    
    def extract_key_points(self, search_results: List[Dict]) -> List[str]:
        """Extract key points from search results"""
        key_points = []
        
        for result in search_results[:5]:  # Top 5 results
            snippet = result.get('snippet', '')
            if snippet:
                # Extract first sentence or key information
                sentences = self._split_sentences(snippet)
                if sentences:
                    key_points.append(f"• {sentences[0]}")
        
        return key_points
