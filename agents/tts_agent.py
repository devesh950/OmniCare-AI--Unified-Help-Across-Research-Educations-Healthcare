"""
Text-to-Speech Agent - Converts research reports to natural speech
Helps visually impaired users access research content
"""

import re
from typing import Dict, List

class TextToSpeechAgent:
    """
    Text-to-Speech Agent that converts text to speech-ready format
    Optimizes content for natural audio playback
    """
    
    def __init__(self):
        self.speech_rate = "medium"  # slow, medium, fast
        self.voice_type = "neutral"
    
    def prepare_for_speech(self, text: str, speech_type: str = "report") -> Dict:
        """
        Prepare text for text-to-speech conversion
        
        Args:
            text: Text content to convert
            speech_type: Type of content (report, summary, results)
            
        Returns:
            Speech-ready content with SSML markup
        """
        # Clean text for speech
        cleaned_text = self._clean_for_speech(text)
        
        # Add pauses and emphasis
        speech_text = self._add_speech_markers(cleaned_text, speech_type)
        
        # Generate SSML (Speech Synthesis Markup Language)
        ssml = self._generate_ssml(speech_text)
        
        # Break into manageable chunks
        chunks = self._chunk_for_speech(speech_text)
        
        return {
            'text': cleaned_text,
            'speech_text': speech_text,
            'ssml': ssml,
            'chunks': chunks,
            'estimated_duration': self._estimate_duration(cleaned_text),
            'word_count': len(cleaned_text.split()),
            'recommended_breaks': self._identify_break_points(cleaned_text)
        }
    
    def _clean_for_speech(self, text: str) -> str:
        """Clean text for natural speech"""
        if not text:
            return ""
        
        # Remove markdown symbols
        text = re.sub(r'\*\*([^*]+)\*\*', r'\1', text)  # Bold
        text = re.sub(r'\*([^*]+)\*', r'\1', text)  # Italic
        text = re.sub(r'`([^`]+)`', r'\1', text)  # Code
        
        # Convert headers to natural speech
        text = re.sub(r'^#{1,6}\s+', '', text, flags=re.MULTILINE)
        
        # Replace special characters with words
        replacements = {
            '&': 'and',
            '@': 'at',
            '#': 'number',
            '$': 'dollars',
            '%': 'percent',
            '+': 'plus',
            '=': 'equals',
            '<': 'less than',
            '>': 'greater than',
            '→': 'leads to',
            '←': 'comes from',
            '↑': 'increases',
            '↓': 'decreases',
            '✓': 'check',
            '✗': 'cross',
            '•': '',  # Remove bullets, they're implicit in lists
            '◦': '',
            '▪': '',
        }
        
        for symbol, word in replacements.items():
            text = text.replace(symbol, word)
        
        # Fix spacing
        text = re.sub(r'\s+', ' ', text)
        
        # Spell out abbreviations
        text = self._expand_abbreviations(text)
        
        return text.strip()
    
    def _expand_abbreviations(self, text: str) -> str:
        """Expand common abbreviations for speech"""
        abbreviations = {
            'e.g.': 'for example',
            'i.e.': 'that is',
            'etc.': 'et cetera',
            'vs.': 'versus',
            'Dr.': 'Doctor',
            'Mr.': 'Mister',
            'Mrs.': 'Missus',
            'Ms.': 'Miss',
            'Prof.': 'Professor',
            'URL': 'U R L',
            'API': 'A P I',
            'AI': 'A I',
            'FAQ': 'F A Q',
            'CEO': 'C E O',
            'USA': 'U S A',
            'UK': 'U K',
        }
        
        for abbr, expansion in abbreviations.items():
            text = text.replace(abbr, expansion)
        
        return text
    
    def _add_speech_markers(self, text: str, speech_type: str) -> str:
        """Add natural pauses and emphasis markers"""
        
        # Add pause after sentences
        text = re.sub(r'([.!?])\s+', r'\1 <break time="500ms"/> ', text)
        
        # Add pause after section headers (double newline)
        text = re.sub(r'\n\n+', '\n<break time="1s"/>\n', text)
        
        # Add emphasis to important phrases
        important_phrases = [
            'important', 'critical', 'essential', 'key finding',
            'conclusion', 'summary', 'recommendation', 'note that'
        ]
        
        for phrase in important_phrases:
            pattern = re.compile(f'({phrase})', re.IGNORECASE)
            text = pattern.sub(r'<emphasis level="strong">\1</emphasis>', text)
        
        # Add pause before lists
        text = re.sub(r'\n(\d+\.)', r'\n<break time="300ms"/>\1', text)
        
        return text
    
    def _generate_ssml(self, text: str) -> str:
        """Generate SSML (Speech Synthesis Markup Language) markup"""
        
        ssml = f'''<speak version="1.1" xmlns="http://www.w3.org/2001/10/synthesis">
    <voice name="en-US-Neural">
        <prosody rate="{self.speech_rate}" pitch="medium">
            {text}
        </prosody>
    </voice>
</speak>'''
        
        return ssml
    
    def _chunk_for_speech(self, text: str, chunk_size: int = 500) -> List[Dict]:
        """Break text into manageable speech chunks"""
        
        # Split by sentences
        sentences = re.split(r'([.!?]+\s+)', text)
        
        chunks = []
        current_chunk = ""
        chunk_number = 1
        
        for i in range(0, len(sentences), 2):
            sentence = sentences[i]
            punctuation = sentences[i + 1] if i + 1 < len(sentences) else ""
            full_sentence = sentence + punctuation
            
            # If adding this sentence exceeds chunk size, save current chunk
            if len(current_chunk) + len(full_sentence) > chunk_size and current_chunk:
                chunks.append({
                    'number': chunk_number,
                    'text': current_chunk.strip(),
                    'duration': self._estimate_duration(current_chunk)
                })
                current_chunk = full_sentence
                chunk_number += 1
            else:
                current_chunk += full_sentence
        
        # Add last chunk
        if current_chunk:
            chunks.append({
                'number': chunk_number,
                'text': current_chunk.strip(),
                'duration': self._estimate_duration(current_chunk)
            })
        
        return chunks
    
    def _estimate_duration(self, text: str) -> str:
        """Estimate audio duration"""
        if not text:
            return "0 seconds"
        
        # Average speech rate: 150 words per minute
        words = len(text.split())
        seconds = (words / 150) * 60
        
        if seconds < 60:
            return f"{int(seconds)} seconds"
        
        minutes = int(seconds / 60)
        remaining_seconds = int(seconds % 60)
        
        if remaining_seconds > 0:
            return f"{minutes} minutes {remaining_seconds} seconds"
        return f"{minutes} minutes"
    
    def _identify_break_points(self, text: str) -> List[Dict]:
        """Identify natural break points for long content"""
        break_points = []
        
        # Break at major sections
        lines = text.split('\n')
        char_position = 0
        
        for i, line in enumerate(lines):
            # Detect section headers (usually shorter, capitalized lines)
            if line.strip() and len(line) < 100:
                # Check if it looks like a header
                if line.strip().isupper() or line.strip().endswith(':'):
                    break_points.append({
                        'position': char_position,
                        'line_number': i + 1,
                        'type': 'section_break',
                        'text': line.strip()
                    })
            
            char_position += len(line) + 1
        
        # Add breaks every ~5 minutes of content
        words = len(text.split())
        words_per_break = 750  # 5 minutes worth
        
        if words > words_per_break:
            num_breaks = words // words_per_break
            for i in range(1, num_breaks + 1):
                break_points.append({
                    'position': None,
                    'line_number': None,
                    'type': 'time_break',
                    'text': f"Natural break point {i} (approximately {i * 5} minutes in)"
                })
        
        return break_points
    
    def generate_audio_navigation(self, content: Dict) -> Dict:
        """Generate audio navigation menu"""
        
        sections = []
        
        # Extract sections from report
        if 'report' in content:
            report = content['report']
            section_pattern = r'^##\s+(.+)$'
            matches = re.finditer(section_pattern, report, re.MULTILINE)
            
            for i, match in enumerate(matches, 1):
                sections.append({
                    'number': i,
                    'title': match.group(1).strip(),
                    'audio_label': f"Section {i}: {match.group(1).strip()}"
                })
        
        navigation = {
            'introduction': "Use voice commands or number keys to navigate sections",
            'sections': sections,
            'total_sections': len(sections),
            'commands': [
                "Say 'next section' to move forward",
                "Say 'previous section' to go back",
                "Say 'repeat' to hear the current section again",
                "Say 'pause' to pause playback",
                "Say 'menu' to return to section navigation"
            ]
        }
        
        return navigation
    
    def create_audio_summary(self, summary: str) -> str:
        """Create a brief audio-optimized summary"""
        
        # Limit to key points
        sentences = re.split(r'[.!?]+', summary)
        key_sentences = sentences[:3]  # First 3 sentences
        
        audio_summary = "Quick summary. " + '. '.join(s.strip() for s in key_sentences if s.strip()) + '.'
        
        # Add listening time
        duration = self._estimate_duration(audio_summary)
        audio_summary = f"Listening time: {duration}. " + audio_summary
        
        return audio_summary
