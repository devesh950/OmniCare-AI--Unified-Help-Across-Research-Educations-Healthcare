"""
Google Gemini API Client
Provides text generation using Gemini Pro model.
"""

import os
import google.generativeai as genai
from typing import Optional, Dict, Any
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class GeminiClient:
    """Client for Google Gemini API integration."""
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize Gemini client with API key from environment or parameter."""
        # Use provided key or get from environment
        self.api_key = api_key or os.getenv('GEMINI_API_KEY')
        
        if not self.api_key:
            raise ValueError(
                "GEMINI_API_KEY not found. "
                "Please provide API key or set GEMINI_API_KEY environment variable."
            )
        
        # Configure Gemini API
        genai.configure(api_key=self.api_key)
        
        # Initialize model
        self.model = genai.GenerativeModel('gemini-pro')
        
        # Default generation config
        self.default_config = {
            'temperature': 0.7,
            'top_p': 0.9,
            'top_k': 40,
            'max_output_tokens': 2048,
        }
    
    def generate_text(
        self,
        prompt: str,
        temperature: float = 0.7,
        max_tokens: int = 2048,
        stop_sequences: Optional[list] = None
    ) -> str:
        """
        Generate text using Gemini Pro model.
        
        Args:
            prompt: Input prompt for generation
            temperature: Controls randomness (0.0-1.0)
            max_tokens: Maximum tokens to generate
            stop_sequences: Optional sequences to stop generation
        
        Returns:
            Generated text string
        """
        try:
            # Configure generation parameters
            generation_config = genai.types.GenerationConfig(
                temperature=temperature,
                max_output_tokens=max_tokens,
                top_p=self.default_config['top_p'],
                top_k=self.default_config['top_k'],
            )
            
            # Generate content
            response = self.model.generate_content(
                prompt,
                generation_config=generation_config,
            )
            
            # Extract text from response
            if response.parts:
                return response.text
            else:
                return "No response generated."
                
        except Exception as e:
            print(f"Gemini generation error: {e}")
            return f"Error generating content: {str(e)}"
    
    def generate_educational_content(
        self,
        topic: str,
        difficulty: str = "intermediate",
        content_type: str = "explanation"
    ) -> str:
        """
        Generate educational content optimized for learning.
        
        Args:
            topic: Subject topic to generate content for
            difficulty: Difficulty level (elementary/intermediate/advanced)
            content_type: Type of content (explanation/summary/practice/quiz)
        
        Returns:
            Generated educational content
        """
        # Build specialized prompt based on content type
        prompts = {
            'explanation': f"""
Explain {topic} for a {difficulty} level student.

Requirements:
- Clear, concise explanation
- Use simple language
- Include 2-3 real-world examples
- Add helpful analogies
- Structure with subheadings
- Keep it engaging and practical

Explanation:
""",
            'summary': f"""
Create a comprehensive summary of {topic} for {difficulty} level.

Requirements:
- 2-3 paragraphs maximum
- Key concepts highlighted
- Important terms defined
- Practical applications mentioned
- Easy to understand

Summary:
""",
            'practice': f"""
Generate 5 practice problems for {topic} at {difficulty} level.

For each problem:
1. Clear problem statement
2. Step-by-step solution
3. Learning objective

Problems:
""",
            'quiz': f"""
Create a 5-question quiz on {topic} for {difficulty} level.

For each question:
1. Multiple choice with 4 options
2. Indicate correct answer
3. Brief explanation of why it's correct

Quiz:
"""
        }
        
        prompt = prompts.get(content_type, prompts['explanation'])
        return self.generate_text(prompt, temperature=0.7, max_tokens=2048)
    
    def generate_health_information(
        self,
        symptoms: str,
        context: str = ""
    ) -> str:
        """
        Generate health information (educational purposes only).
        
        Args:
            symptoms: Symptom description
            context: Additional context
        
        Returns:
            Generated health information with disclaimer
        """
        prompt = f"""
Based on these symptoms: {symptoms}
{f"Context: {context}" if context else ""}

Provide educational health information:
1. Possible common causes (general information only)
2. When to seek medical attention
3. General wellness advice
4. Prevention tips

IMPORTANT DISCLAIMER: This is educational information only, not medical diagnosis.
Always consult a qualified healthcare professional for medical advice.

Information:
"""
        return self.generate_text(prompt, temperature=0.5, max_tokens=1500)


def get_gemini_client(api_key: Optional[str] = None) -> Optional[GeminiClient]:
    """
    Factory function to get Gemini client instance.
    Returns None if API key not available.
    """
    try:
        return GeminiClient(api_key)
    except ValueError as e:
        print(f"Gemini client initialization failed: {e}")
        return None
