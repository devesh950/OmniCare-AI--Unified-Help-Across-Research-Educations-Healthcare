"""
Session and Memory Management for Research Assistant
Implements state management and long-term memory for research history
"""

import json
import os
from datetime import datetime
from typing import List, Dict, Optional
import hashlib

class SessionService:
    """
    In-Memory Session Service for managing research sessions and state
    """
    
    def __init__(self, storage_path: str = "sessions"):
        self.storage_path = storage_path
        self.current_session = None
        self.sessions = {}
        
        try:
            # Create storage directory if it doesn't exist
            os.makedirs(storage_path, exist_ok=True)
            # Load existing sessions
            self._load_sessions()
        except Exception as e:
            # If file operations fail, continue with in-memory only
            print(f"Warning: Could not access session storage: {e}")
    
    def create_session(self, user_id: str = "default") -> str:
        """Create a new session"""
        session_id = self._generate_session_id()
        session = {
            'id': session_id,
            'user_id': user_id,
            'created_at': datetime.now().isoformat(),
            'state': {},
            'research_history': [],
            'context': []
        }
        
        self.sessions[session_id] = session
        self.current_session = session_id
        self._save_session(session_id)
        
        return session_id
    
    def get_session(self, session_id: str) -> Optional[Dict]:
        """Get session by ID"""
        return self.sessions.get(session_id)
    
    def update_session_state(self, session_id: str, key: str, value: any):
        """Update session state"""
        if session_id in self.sessions:
            self.sessions[session_id]['state'][key] = value
            self._save_session(session_id)
    
    def add_to_history(self, session_id: str, research_data: Dict):
        """Add research to session history"""
        if session_id in self.sessions:
            self.sessions[session_id]['research_history'].append(research_data)
            self._save_session(session_id)
    
    def get_session_history(self, session_id: str) -> List[Dict]:
        """Get research history for a session"""
        session = self.sessions.get(session_id)
        return session['research_history'] if session else []
    
    def add_context(self, session_id: str, context_item: str):
        """Add context to session for context engineering"""
        if session_id in self.sessions:
            self.sessions[session_id]['context'].append({
                'content': context_item,
                'timestamp': datetime.now().isoformat()
            })
            
            # Context compaction: Keep only last 10 items
            if len(self.sessions[session_id]['context']) > 10:
                self.sessions[session_id]['context'] = \
                    self.sessions[session_id]['context'][-10:]
            
            self._save_session(session_id)
    
    def get_session_context(self, session_id: str) -> List[Dict]:
        """Get compressed context for session"""
        session = self.sessions.get(session_id)
        return session['context'] if session else []
    
    def _generate_session_id(self) -> str:
        """Generate unique session ID"""
        timestamp = datetime.now().isoformat()
        hash_input = f"{timestamp}_{os.urandom(8).hex()}"
        return hashlib.md5(hash_input.encode()).hexdigest()[:16]
    
    def _save_session(self, session_id: str):
        """Save session to disk"""
        try:
            session = self.sessions.get(session_id)
            if session:
                # Ensure directory exists
                os.makedirs(self.storage_path, exist_ok=True)
                filepath = os.path.join(self.storage_path, f"{session_id}.json")
                with open(filepath, 'w') as f:
                    json.dump(session, f, indent=2)
        except Exception as e:
            # Log error but continue (in-memory session still works)
            print(f"Warning: Could not save session file: {e}")
    
    def _load_sessions(self):
        """Load all sessions from disk"""
        if not os.path.exists(self.storage_path):
            return
        
        for filename in os.listdir(self.storage_path):
            if filename.endswith('.json'):
                filepath = os.path.join(self.storage_path, filename)
                try:
                    with open(filepath, 'r') as f:
                        session = json.load(f)
                        self.sessions[session['id']] = session
                except:
                    pass


class MemoryBank:
    """
    Long-term memory storage for research insights and patterns
    """
    
    def __init__(self, storage_path: str = "memory_bank"):
        self.storage_path = storage_path
        self.memories = {}
        
        os.makedirs(storage_path, exist_ok=True)
        self._load_memories()
    
    def store_memory(self, topic: str, insights: Dict, metadata: Dict = None):
        """Store long-term memory of research insights"""
        memory_id = hashlib.md5(topic.encode()).hexdigest()[:16]
        
        memory = {
            'id': memory_id,
            'topic': topic,
            'insights': insights,
            'metadata': metadata or {},
            'timestamp': datetime.now().isoformat(),
            'access_count': 0
        }
        
        # Update existing or create new
        if memory_id in self.memories:
            memory['access_count'] = self.memories[memory_id]['access_count'] + 1
        
        self.memories[memory_id] = memory
        self._save_memory(memory_id)
    
    def retrieve_memory(self, topic: str) -> Optional[Dict]:
        """Retrieve memory by topic"""
        memory_id = hashlib.md5(topic.encode()).hexdigest()[:16]
        
        if memory_id in self.memories:
            self.memories[memory_id]['access_count'] += 1
            self._save_memory(memory_id)
            return self.memories[memory_id]
        
        return None
    
    def search_memories(self, query: str, limit: int = 5) -> List[Dict]:
        """Search memories by query string"""
        results = []
        query_lower = query.lower()
        
        for memory in self.memories.values():
            topic_lower = memory['topic'].lower()
            if query_lower in topic_lower:
                results.append(memory)
        
        # Sort by access count and recency
        results.sort(key=lambda x: (x['access_count'], x['timestamp']), reverse=True)
        
        return results[:limit]
    
    def get_recent_memories(self, limit: int = 10) -> List[Dict]:
        """Get most recent memories"""
        sorted_memories = sorted(
            self.memories.values(),
            key=lambda x: x['timestamp'],
            reverse=True
        )
        return sorted_memories[:limit]
    
    def get_popular_topics(self, limit: int = 5) -> List[Dict]:
        """Get most accessed topics"""
        sorted_memories = sorted(
            self.memories.values(),
            key=lambda x: x['access_count'],
            reverse=True
        )
        return sorted_memories[:limit]
    
    def _save_memory(self, memory_id: str):
        """Save memory to disk"""
        memory = self.memories.get(memory_id)
        if memory:
            filepath = os.path.join(self.storage_path, f"{memory_id}.json")
            with open(filepath, 'w') as f:
                json.dump(memory, f, indent=2)
    
    def _load_memories(self):
        """Load all memories from disk"""
        if not os.path.exists(self.storage_path):
            return
        
        for filename in os.listdir(self.storage_path):
            if filename.endswith('.json'):
                filepath = os.path.join(self.storage_path, filename)
                try:
                    with open(filepath, 'r') as f:
                        memory = json.load(f)
                        self.memories[memory['id']] = memory
                except:
                    pass


def compact_context(context_list: List[str], max_length: int = 1000) -> str:
    """
    Context compaction: Reduce context size while maintaining key information
    """
    if not context_list:
        return ""
    
    # Join all context
    full_context = " ".join(context_list)
    
    # If within limit, return as-is
    if len(full_context) <= max_length:
        return full_context
    
    # Simple compaction: Take first and last portions
    half = max_length // 2
    compacted = full_context[:half] + " ... " + full_context[-half:]
    
    return compacted
