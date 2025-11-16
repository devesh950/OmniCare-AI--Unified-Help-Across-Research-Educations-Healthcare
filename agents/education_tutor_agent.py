"""
Education Tutor Agent - Personalized Learning Assistant
Provides adaptive tutoring, explains concepts, generates practice problems
"""

import json
import re
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from utils.observability import AgentLogger, AgentTracer, MetricsCollector
from utils.gemini_client import get_gemini_client

logger = AgentLogger("EducationTutorAgent")
tracer = AgentTracer()
metrics = MetricsCollector()


class EducationTutorAgent:
    """
    AI Tutor that adapts to student's learning level and provides:
    - Concept explanations at appropriate difficulty
    - Step-by-step problem solving
    - Practice exercises with solutions
    - Learning path recommendations
    """
    
    def __init__(self, api_key: Optional[str] = None):
        self.name = "Education Tutor"
        self.api_key = api_key
        self.gemini_client = None
        
        # Try to initialize Gemini client
        if api_key:
            self.gemini_client = get_gemini_client(api_key)
            if self.gemini_client:
                logger.info("Gemini API integration enabled for Education Tutor")
        
        self.subjects = {
            "math": ["algebra", "geometry", "calculus", "statistics", "arithmetic"],
            "science": ["physics", "chemistry", "biology", "earth science"],
            "language": ["grammar", "writing", "reading comprehension", "vocabulary"],
            "computer science": ["programming", "algorithms", "data structures"],
            "history": ["world history", "us history", "geography"],
            "programming": [
                "python", "javascript", "java", "c++", "c#", "c", 
                "html", "css", "sql", "r", "php", "swift", "kotlin",
                "typescript", "go", "rust", "ruby", "perl", "scala",
                "react", "angular", "vue", "node.js", "django", "flask",
                "spring boot", "asp.net", ".net", "express.js"
            ],
            "web development": [
                "html", "css", "javascript", "responsive design",
                "frontend", "backend", "full stack", "rest api",
                "graphql", "web security", "web performance"
            ],
            "data science": [
                "python for data science", "pandas", "numpy", "matplotlib",
                "machine learning", "deep learning", "tensorflow", "pytorch",
                "scikit-learn", "data visualization", "statistics",
                "sql for data analysis", "jupyter notebooks"
            ],
            "mobile development": [
                "android", "ios", "react native", "flutter",
                "swift", "kotlin", "mobile ui/ux", "app development"
            ],
            "devops": [
                "git", "docker", "kubernetes", "ci/cd",
                "linux", "bash", "cloud computing", "aws", "azure"
            ]
        }
        self.difficulty_levels = ["elementary", "middle school", "high school", "college", "advanced"]
        
    def tutor(self, 
              query: str, 
              subject: Optional[str] = None,
              difficulty: str = "high school",
              learning_style: str = "visual",
              trace_id: Optional[str] = None) -> Dict:
        """
        Main tutoring function - analyzes query and provides educational support
        
        Args:
            query: Student's question or topic
            subject: Subject area (auto-detected if None)
            difficulty: Learning level
            learning_style: visual, auditory, kinesthetic, reading/writing
            trace_id: Tracing ID for observability
            
        Returns:
            Dict with explanation, examples, practice problems, resources
        """
        start_time = datetime.now()
        trace_id = trace_id or tracer.generate_trace_id()
        
        logger.info(f"[{trace_id}] Starting tutoring session for: {query[:50]}...")
        
        try:
            # Detect subject if not provided
            if not subject:
                subject = self._detect_subject(query)
                logger.info(f"[{trace_id}] Auto-detected subject: {subject}")
            
            # Analyze the query type
            query_type = self._analyze_query_type(query)
            logger.info(f"[{trace_id}] Query type: {query_type}")
            
            # Generate response based on query type
            if query_type == "concept_explanation":
                response = self._explain_concept(query, subject, difficulty, learning_style)
            elif query_type == "problem_solving":
                response = self._solve_problem(query, subject, difficulty)
            elif query_type == "practice_request":
                response = self._generate_practice(query, subject, difficulty)
            else:
                response = self._general_tutoring(query, subject, difficulty, learning_style)
            
            # Add learning recommendations
            response["recommendations"] = self._generate_recommendations(query, subject, difficulty)
            response["resources"] = self._find_resources(query, subject)
            
            # Add metadata
            duration = (datetime.now() - start_time).total_seconds()
            response["metadata"] = {
                "subject": subject,
                "difficulty": difficulty,
                "learning_style": learning_style,
                "query_type": query_type,
                "duration_seconds": round(duration, 2),
                "timestamp": datetime.now().isoformat()
            }
            
            metrics.record_metric("education_tutor_query", duration, {"subject": subject, "type": query_type})
            logger.info(f"[{trace_id}] Tutoring session completed in {duration:.2f}s")
            
            return response
            
        except Exception as e:
            logger.error(f"[{trace_id}] Error in tutoring: {str(e)}")
            return {
                "error": str(e),
                "explanation": "I encountered an error. Please rephrase your question or try a different topic.",
                "metadata": {"subject": subject, "difficulty": difficulty}
            }
    
    def _detect_subject(self, query: str) -> str:
        """Auto-detect subject from query keywords"""
        query_lower = query.lower()
        
        # Math keywords
        if any(word in query_lower for word in ["equation", "solve", "calculate", "algebra", "geometry", 
                                                  "derivative", "integral", "probability", "factor", "multiply"]):
            return "math"
        
        # Science keywords
        if any(word in query_lower for word in ["atom", "cell", "energy", "force", "chemical", "organism",
                                                  "molecule", "physics", "biology", "chemistry", "reaction"]):
            return "science"
        
        # Programming keywords
        if any(word in query_lower for word in ["code", "program", "function", "algorithm", "python", 
                                                  "javascript", "loop", "variable", "array", "class"]):
            return "computer science"
        
        # Language keywords
        if any(word in query_lower for word in ["grammar", "sentence", "verb", "noun", "essay", "write",
                                                  "paragraph", "punctuation", "spelling"]):
            return "language"
        
        # History keywords
        if any(word in query_lower for word in ["war", "revolution", "president", "ancient", "civilization",
                                                  "empire", "treaty", "constitution"]):
            return "history"
        
        return "general"
    
    def _analyze_query_type(self, query: str) -> str:
        """Determine what type of help the student needs"""
        query_lower = query.lower()
        
        if any(phrase in query_lower for phrase in ["what is", "explain", "define", "how does", "why"]):
            return "concept_explanation"
        
        if any(phrase in query_lower for phrase in ["solve", "calculate", "find the", "what is the answer"]):
            return "problem_solving"
        
        if any(phrase in query_lower for phrase in ["practice", "exercises", "quiz", "test me", "problems"]):
            return "practice_request"
        
        return "general_help"
    
    def _explain_concept(self, query: str, subject: str, difficulty: str, learning_style: str) -> Dict:
        """Provide detailed concept explanation adapted to learning level and style"""
        
        # Extract the core concept from query
        concept = query.replace("what is", "").replace("explain", "").replace("?", "").strip()
        
        # Generate summary and intro for concept explanations too
        summary = self._generate_topic_summary(concept, subject, difficulty)
        introduction = self._generate_basic_intro(concept, subject, difficulty)
        
        explanation = {
            "concept": concept,
            "quick_summary": summary,
            "introduction": introduction,
            "explanation": self._generate_explanation(concept, subject, difficulty),
            "visual_aids": self._suggest_visual_aids(concept, subject) if learning_style == "visual" else [],
            "examples": self._generate_examples(concept, subject, difficulty),
            "key_points": self._extract_key_points(concept, subject),
            "common_mistakes": self._identify_common_mistakes(concept, subject),
        }
        
        return explanation
    
    def _generate_explanation(self, concept: str, subject: str, difficulty: str) -> str:
        """Generate explanation text adapted to difficulty level"""
        
        # Try using Gemini API if available
        if self.gemini_client:
            try:
                gemini_explanation = self.gemini_client.generate_educational_content(
                    topic=f"{concept} in {subject}",
                    difficulty=difficulty,
                    content_type="explanation"
                )
                if gemini_explanation and not gemini_explanation.startswith("Error"):
                    logger.info(f"Generated explanation using Gemini API for: {concept}")
                    return gemini_explanation
            except Exception as e:
                logger.warning(f"Gemini API failed, falling back to template: {e}")
        
        # Fallback to template-based approach
        explanations = {
            "math": {
                "elementary": f"Let me explain {concept} in a simple way. {concept} is a mathematical idea that helps us understand numbers and patterns.",
                "high school": f"{concept} is an important mathematical concept. It involves understanding relationships and applying rules to solve problems.",
                "college": f"{concept} is a fundamental principle in mathematics with applications across multiple domains."
            },
            "science": {
                "elementary": f"{concept} is something we can observe in nature. Let me break it down into simple parts.",
                "high school": f"{concept} is a scientific principle that explains how things work in our world.",
                "college": f"{concept} represents a key scientific theory with empirical evidence and practical applications."
            }
        }
        
        subject_key = subject if subject in explanations else "math"
        difficulty_key = difficulty if difficulty in explanations[subject_key] else "high school"
        
        base_explanation = explanations[subject_key][difficulty_key]
        
        # Add structure
        return f"""
{base_explanation}

📚 **Core Definition:**
The concept of '{concept}' can be understood as a foundational idea in {subject}. It builds upon prerequisite knowledge and serves as a building block for more advanced topics.

🔍 **Why It Matters:**
Understanding {concept} is important because it helps you solve real-world problems and prepares you for more advanced learning in {subject}.

💡 **Think of it this way:**
Imagine {concept} like a tool in your learning toolkit. The more you practice and understand it, the more powerful it becomes for solving challenges.
"""
    
    def _generate_examples(self, concept: str, subject: str, difficulty: str) -> List[Dict]:
        """Generate practical examples"""
        return [
            {
                "title": "Basic Example",
                "description": f"Let's look at a simple case of {concept}",
                "solution_steps": [
                    "Step 1: Identify what we know",
                    "Step 2: Apply the concept",
                    "Step 3: Verify the result"
                ]
            },
            {
                "title": "Real-World Application",
                "description": f"How {concept} appears in everyday life",
                "context": "This helps you see why learning this matters"
            }
        ]
    
    def _extract_key_points(self, concept: str, subject: str) -> List[str]:
        """Extract key learning points"""
        return [
            f"✓ {concept} is a core concept in {subject}",
            f"✓ Practice regularly to master {concept}",
            f"✓ Connect {concept} to real-world situations",
            f"✓ Build on this knowledge for advanced topics"
        ]
    
    def _identify_common_mistakes(self, concept: str, subject: str) -> List[str]:
        """Identify common errors students make"""
        return [
            "⚠️ Rushing without understanding the fundamentals",
            "⚠️ Not checking your work",
            "⚠️ Memorizing without understanding the 'why'",
            "⚠️ Skipping practice problems"
        ]
    
    def _suggest_visual_aids(self, concept: str, subject: str) -> List[str]:
        """Suggest visual learning aids"""
        return [
            f"📊 Diagram showing {concept} structure",
            f"📈 Graph illustrating {concept} relationships",
            f"🎨 Color-coded concept map",
            f"🎬 Khan Academy video on {concept}",
            f"🖼️ Interactive visualization"
        ]
    
    def _solve_problem(self, query: str, subject: str, difficulty: str) -> Dict:
        """Help solve a specific problem with step-by-step guidance"""
        return {
            "problem": query,
            "approach": "Let's break this problem down into manageable steps",
            "steps": [
                {
                    "number": 1,
                    "title": "Understand the problem",
                    "description": "Read carefully and identify what's being asked",
                    "tips": ["Highlight key information", "Draw a diagram if helpful"]
                },
                {
                    "number": 2,
                    "title": "Plan your approach",
                    "description": "Decide which concepts and formulas to use",
                    "tips": ["Think about similar problems you've solved", "Write down what you know"]
                },
                {
                    "number": 3,
                    "title": "Execute the solution",
                    "description": "Work through the problem step by step",
                    "tips": ["Show all your work", "Check each step as you go"]
                },
                {
                    "number": 4,
                    "title": "Verify the answer",
                    "description": "Make sure your solution makes sense",
                    "tips": ["Plug answer back into original problem", "Check units and reasonableness"]
                }
            ],
            "hints": [
                "💡 Start with what you know",
                "💡 Don't be afraid to try different approaches",
                "💡 Practice similar problems to build confidence"
            ],
            "solution_strategy": f"For {subject} problems at the {difficulty} level, focus on understanding the underlying concepts rather than just memorizing steps."
        }
    
    def _generate_practice(self, query: str, subject: str, difficulty: str) -> Dict:
        """Generate practice problems"""
        return {
            "practice_set": f"Practice Problems: {subject} ({difficulty} level)",
            "problems": [
                {
                    "number": 1,
                    "difficulty": "easy",
                    "problem": f"Warm-up problem for {subject}",
                    "hint": "Start with the basics you just learned",
                    "estimated_time": "2-3 minutes"
                },
                {
                    "number": 2,
                    "difficulty": "medium",
                    "problem": f"Intermediate problem applying {subject} concepts",
                    "hint": "This builds on problem 1",
                    "estimated_time": "5-7 minutes"
                },
                {
                    "number": 3,
                    "difficulty": "challenging",
                    "problem": f"Advanced problem combining multiple concepts",
                    "hint": "Break this into smaller steps",
                    "estimated_time": "10-15 minutes"
                }
            ],
            "practice_tips": [
                "🎯 Do problems without looking at solutions first",
                "🎯 Time yourself to build speed",
                "🎯 Review mistakes carefully - they're learning opportunities",
                "🎯 Redo problems you got wrong after studying"
            ],
            "answer_key_note": "Solutions are available after you attempt all problems. Learning happens through struggle!"
        }
    
    def _general_tutoring(self, query: str, subject: str, difficulty: str, learning_style: str) -> Dict:
        """General tutoring support with summary and introduction"""
        
        # Generate concise summary and introduction
        summary = self._generate_topic_summary(query, subject, difficulty)
        introduction = self._generate_basic_intro(query, subject, difficulty)
        
        return {
            "topic": query,
            "quick_summary": summary,
            "introduction": introduction,
            "guidance": f"Let's explore {query} together in {subject}",
            "learning_path": [
                f"1️⃣ Start with the fundamentals of {query}",
                f"2️⃣ Work through guided examples",
                f"3️⃣ Practice independently with feedback",
                f"4️⃣ Apply knowledge to real scenarios"
            ],
            "study_tips": self._get_study_tips(learning_style),
            "encouragement": "Remember: Every expert was once a beginner. You're making progress with every question you ask! 🌟"
        }
    
    def _get_study_tips(self, learning_style: str) -> List[str]:
        """Personalized study tips based on learning style"""
        tips = {
            "visual": [
                "📊 Create colorful mind maps and diagrams",
                "📝 Use highlighters to color-code concepts",
                "🎨 Watch educational videos and animations",
                "🖼️ Draw pictures to represent ideas"
            ],
            "auditory": [
                "🎧 Listen to educational podcasts",
                "💬 Explain concepts out loud to yourself",
                "👥 Join study groups for discussions",
                "🎵 Create mnemonics and rhymes"
            ],
            "kinesthetic": [
                "✋ Use hands-on activities and experiments",
                "🚶 Walk around while studying",
                "🎯 Build models and demonstrations",
                "⚡ Take frequent breaks with movement"
            ],
            "reading": [
                "📖 Read textbooks and articles thoroughly",
                "📝 Take detailed written notes",
                "📄 Create written summaries",
                "✍️ Write practice essays and explanations"
            ]
        }
        return tips.get(learning_style, tips["visual"])
    
    def _generate_topic_summary(self, query: str, subject: str, difficulty: str) -> str:
        """Generate a concise 2-3 sentence summary of the topic"""
        
        # Clean up the query
        topic = query.lower().strip()
        
        # Generate summary based on difficulty level
        if difficulty in ["elementary", "middle school"]:
            return f"""**Quick Summary:** {query.title()} is an important concept in {subject} that helps you understand how things work. It's a building block that you'll use in many different situations, and once you master it, learning related topics becomes much easier."""
        elif difficulty == "high school":
            return f"""**Quick Summary:** {query.title()} is a fundamental concept in {subject} that connects basic principles to advanced applications. Understanding this topic will help you solve complex problems and prepares you for higher-level coursework."""
        else:  # college/advanced
            return f"""**Quick Summary:** {query.title()} represents a key theoretical and practical framework in {subject}. It synthesizes multiple concepts and has widespread applications across various domains, making it essential for advanced study and professional work."""
    
    def _generate_basic_intro(self, query: str, subject: str, difficulty: str) -> str:
        """Generate a basic introduction to ease into the topic"""
        
        topic = query.strip()
        
        # Create engaging introductions based on subject
        subject_intros = {
            "math": f"""
🧮 **Introduction to {topic}**

Welcome! Let's start our journey into {topic}. Mathematics might seem challenging at first, but every concept has a logical foundation. 

**What you'll discover:**
- The core idea behind {topic} and why it matters
- How it connects to what you already know
- Real-world situations where this is useful

Think of learning math like building with blocks - each new concept adds to your foundation, making you stronger at problem-solving. Let's build your understanding step by step!
""",
            "science": f"""
🔬 **Introduction to {topic}**

Science is all about understanding the world around us, and {topic} is a fascinating piece of that puzzle!

**What you'll learn:**
- The basic principles of {topic}
- How scientists discovered or developed this idea
- Why this matters in our daily lives

Science isn't just facts to memorize - it's a way of thinking and exploring. Let's explore {topic} together through curiosity and discovery!
""",
            "computer science": f"""
💻 **Introduction to {topic}**

Welcome to the world of {topic}! Computer science combines logical thinking with creative problem-solving.

**What we'll cover:**
- The fundamental concepts behind {topic}
- How this is used in real applications
- Practical skills you'll develop

Don't worry if it seems complex at first - every programmer started as a beginner. Let's break it down into manageable pieces!
""",
            "programming": f"""
👨‍💻 **Introduction to {topic}**

Ready to dive into {topic}? Programming is like learning a new language - it might feel unfamiliar at first, but with practice, it becomes second nature!

**What you'll master:**
- Core syntax and programming concepts
- Best practices and coding standards
- Hands-on examples and real projects
- Problem-solving with code

Every expert programmer started exactly where you are. Let's write some code and bring your ideas to life! 🚀
""",
            "web development": f"""
🌐 **Introduction to {topic}**

Welcome to web development! You're about to learn how websites and web applications come to life.

**What you'll build:**
- Understanding of {topic} fundamentals
- Practical skills for creating web content
- Modern development techniques
- Real-world project experience

The web is your canvas, and code is your paintbrush. Let's create something amazing together!
""",
            "data science": f"""
📊 **Introduction to {topic}**

Data science is where math, statistics, and programming meet to unlock insights from data. {topic} is your gateway to this exciting field!

**What you'll learn:**
- Data analysis and visualization techniques
- Statistical thinking and machine learning basics
- Working with real datasets
- Tools used by professional data scientists

Data is everywhere, and you're about to learn how to make it speak. Let's turn raw data into actionable insights!
""",
            "mobile development": f"""
📱 **Introduction to {topic}**

Mobile apps are in everyone's pocket! Learn {topic} and build applications used by millions.

**What you'll create:**
- Understanding of mobile app architecture
- UI/UX design for mobile platforms
- Native or cross-platform development skills
- Real app projects for your portfolio

Your app ideas can change the world. Let's turn them into reality, one screen at a time!
""",
            "devops": f"""
⚙️ **Introduction to {topic}**

DevOps bridges development and operations, making software delivery faster and more reliable. {topic} is essential in modern tech!

**What you'll master:**
- Automation and deployment pipelines
- Infrastructure management
- Monitoring and troubleshooting
- Industry-standard tools and practices

DevOps engineers are in high demand. Let's build your skills and make deployments smooth and stress-free!
""",
            "language": f"""
📝 **Introduction to {topic}**

Language is how we express ideas, tell stories, and connect with others. {topic} is an essential tool in your communication toolkit!

**What you'll explore:**
- The basics of {topic} and why it matters
- How to apply this in your writing and speaking
- Tips to improve your skills

Good communication is a superpower in any career. Let's develop your abilities together!
""",
            "history": f"""
🌍 **Introduction to {topic}**

History helps us understand how we got to where we are today. {topic} is a window into the past that shapes our present!

**What you'll discover:**
- Key events and people related to {topic}
- Why this period/event was significant
- How it influences our world today

History isn't just dates and names - it's stories of real people and pivotal moments. Let's explore {topic} together!
"""
        }
        
        # Get introduction for subject, with fallback
        subject_key = subject.lower()
        for key in subject_intros:
            if key in subject_key:
                return subject_intros[key]
        
        # Default introduction
        return f"""
📚 **Introduction to {topic}**

Welcome! You're about to learn something valuable about {topic} in {subject}.

**What you'll discover:**
- The fundamental concepts of {topic}
- Why this topic is important
- How to apply what you learn

Learning is a journey, not a race. Let's take this step by step and build your confidence along the way!
"""

    
    def _generate_recommendations(self, query: str, subject: str, difficulty: str) -> List[str]:
        """Recommend next learning steps"""
        return [
            f"📚 Continue exploring {subject} at the {difficulty} level",
            f"🎯 Practice 3-5 problems daily on this topic",
            f"🔍 Connect this to related concepts you've learned",
            f"👥 Teach this concept to someone else to deepen understanding",
            f"📈 Track your progress and celebrate small wins"
        ]
    
    def _find_resources(self, query: str, subject: str) -> List[Dict]:
        """Suggest external learning resources"""
        return [
            {
                "name": "Khan Academy",
                "url": f"https://www.khanacademy.org",
                "description": "Free video lessons and practice",
                "type": "video"
            },
            {
                "name": "Wikipedia",
                "url": f"https://en.wikipedia.org/wiki/{query.replace(' ', '_')}",
                "description": "Detailed background information",
                "type": "reference"
            },
            {
                "name": "YouTube Educational Channels",
                "url": "https://www.youtube.com",
                "description": f"Search for '{query} tutorial'",
                "type": "video"
            },
            {
                "name": "Practice Problems",
                "url": "https://www.wolframalpha.com",
                "description": "Step-by-step problem solving",
                "type": "interactive"
            }
        ]


# Example usage
if __name__ == "__main__":
    tutor = EducationTutorAgent()
    
    # Test 1: Concept explanation
    result = tutor.tutor(
        query="What is the Pythagorean theorem?",
        difficulty="high school",
        learning_style="visual"
    )
    print(json.dumps(result, indent=2))
    
    # Test 2: Problem solving
    result = tutor.tutor(
        query="How do I solve quadratic equations?",
        subject="math",
        difficulty="high school"
    )
    print(json.dumps(result, indent=2))
