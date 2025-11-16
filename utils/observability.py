"""
Observability Module: Logging, Tracing, and Metrics
Provides comprehensive monitoring for the multi-agent system
"""

import logging
import json
import time
from datetime import datetime
from typing import Dict, List, Optional
import os
from functools import wraps

class AgentLogger:
    """
    Advanced logging system for agent activities
    """
    
    def __init__(self, log_dir: str = "logs"):
        self.log_dir = log_dir
        os.makedirs(log_dir, exist_ok=True)
        
        # Setup main logger
        self.logger = logging.getLogger("ResearchAssistant")
        self.logger.setLevel(logging.DEBUG)
        
        # File handler
        log_file = os.path.join(log_dir, f"agent_{datetime.now().strftime('%Y%m%d')}.log")
        fh = logging.FileHandler(log_file)
        fh.setLevel(logging.DEBUG)
        
        # Console handler
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        
        # Formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)
        
        self.logger.addHandler(fh)
        self.logger.addHandler(ch)
    
    def log_agent_start(self, agent_name: str, task: str):
        """Log agent start"""
        self.logger.info(f"🤖 Agent [{agent_name}] started task: {task}")
    
    def log_agent_complete(self, agent_name: str, task: str, duration: float):
        """Log agent completion"""
        self.logger.info(f"✅ Agent [{agent_name}] completed task: {task} in {duration:.2f}s")
    
    def log_agent_error(self, agent_name: str, error: str):
        """Log agent error"""
        self.logger.error(f"❌ Agent [{agent_name}] error: {error}")
    
    def log_tool_usage(self, tool_name: str, params: Dict):
        """Log tool usage"""
        self.logger.debug(f"🔧 Tool [{tool_name}] called with params: {json.dumps(params)}")
    
    def log_search_results(self, query: str, num_results: int):
        """Log search results"""
        self.logger.info(f"🔍 Search for '{query}' returned {num_results} results")
    
    def info(self, message: str):
        """Log info message"""
        self.logger.info(message)
    
    def error(self, message: str):
        """Log error message"""
        self.logger.error(message)
    
    def warning(self, message: str):
        """Log warning message"""
        self.logger.warning(message)
    
    def debug(self, message: str):
        """Log debug message"""
        self.logger.debug(message)
    
    def get_logger(self):
        """Get underlying logger"""
        return self.logger


class AgentTracer:
    """
    Distributed tracing for agent execution flow
    """
    
    def __init__(self, trace_dir: str = "traces"):
        self.trace_dir = trace_dir
        self.traces = []
        self.current_trace_id = None
        
        os.makedirs(trace_dir, exist_ok=True)
    
    def start_trace(self, operation: str, metadata: Dict = None) -> str:
        """Start a new trace"""
        trace_id = f"trace_{int(time.time() * 1000)}"
        
        trace = {
            'trace_id': trace_id,
            'operation': operation,
            'start_time': datetime.now().isoformat(),
            'metadata': metadata or {},
            'spans': [],
            'status': 'in_progress'
        }
        
        self.traces.append(trace)
        self.current_trace_id = trace_id
        
        return trace_id
    
    def add_span(self, trace_id: str, agent_name: str, action: str, duration: float, status: str = "success"):
        """Add a span (sub-operation) to a trace"""
        for trace in self.traces:
            if trace['trace_id'] == trace_id:
                span = {
                    'agent': agent_name,
                    'action': action,
                    'duration': duration,
                    'status': status,
                    'timestamp': datetime.now().isoformat()
                }
                trace['spans'].append(span)
                break
    
    def end_trace(self, trace_id: str, status: str = "success"):
        """End a trace"""
        for trace in self.traces:
            if trace['trace_id'] == trace_id:
                trace['end_time'] = datetime.now().isoformat()
                trace['status'] = status
                
                # Calculate total duration
                start = datetime.fromisoformat(trace['start_time'])
                end = datetime.fromisoformat(trace['end_time'])
                trace['total_duration'] = (end - start).total_seconds()
                
                # Save trace to file
                self._save_trace(trace)
                break
    
    def get_trace(self, trace_id: str) -> Optional[Dict]:
        """Get a specific trace"""
        for trace in self.traces:
            if trace['trace_id'] == trace_id:
                return trace
        return None
    
    def get_recent_traces(self, limit: int = 10) -> List[Dict]:
        """Get recent traces"""
        return self.traces[-limit:]
    
    def _save_trace(self, trace: Dict):
        """Save trace to file"""
        filename = os.path.join(self.trace_dir, f"{trace['trace_id']}.json")
        with open(filename, 'w') as f:
            json.dump(trace, f, indent=2)


class MetricsCollector:
    """
    Collect and aggregate metrics for agent performance
    """
    
    def __init__(self):
        self.metrics = {
            'agent_calls': {},
            'tool_calls': {},
            'response_times': [],
            'errors': [],
            'success_rate': {'success': 0, 'failure': 0}
        }
    
    def record_agent_call(self, agent_name: str, duration: float, success: bool):
        """Record agent call metrics"""
        if agent_name not in self.metrics['agent_calls']:
            self.metrics['agent_calls'][agent_name] = {
                'count': 0,
                'total_duration': 0,
                'avg_duration': 0,
                'success': 0,
                'failure': 0
            }
        
        self.metrics['agent_calls'][agent_name]['count'] += 1
        self.metrics['agent_calls'][agent_name]['total_duration'] += duration
        self.metrics['agent_calls'][agent_name]['avg_duration'] = \
            self.metrics['agent_calls'][agent_name]['total_duration'] / \
            self.metrics['agent_calls'][agent_name]['count']
        
        if success:
            self.metrics['agent_calls'][agent_name]['success'] += 1
            self.metrics['success_rate']['success'] += 1
        else:
            self.metrics['agent_calls'][agent_name]['failure'] += 1
            self.metrics['success_rate']['failure'] += 1
        
        self.metrics['response_times'].append(duration)
    
    def record_tool_call(self, tool_name: str):
        """Record tool usage"""
        if tool_name not in self.metrics['tool_calls']:
            self.metrics['tool_calls'][tool_name] = 0
        self.metrics['tool_calls'][tool_name] += 1
    
    def record_metric(self, metric_name: str, value: float, tags: Dict = None):
        """Record a custom metric with optional tags"""
        if 'custom_metrics' not in self.metrics:
            self.metrics['custom_metrics'] = []
        
        self.metrics['custom_metrics'].append({
            'name': metric_name,
            'value': value,
            'tags': tags or {},
            'timestamp': datetime.now().isoformat()
        })
    
    def record_error(self, error_type: str, error_message: str):
        """Record error"""
        self.metrics['errors'].append({
            'type': error_type,
            'message': error_message,
            'timestamp': datetime.now().isoformat()
        })
    
    def get_metrics_summary(self) -> Dict:
        """Get summary of all metrics"""
        total_calls = sum(m['count'] for m in self.metrics['agent_calls'].values())
        avg_response_time = sum(self.metrics['response_times']) / len(self.metrics['response_times']) \
            if self.metrics['response_times'] else 0
        
        total_attempts = self.metrics['success_rate']['success'] + self.metrics['success_rate']['failure']
        success_rate = (self.metrics['success_rate']['success'] / total_attempts * 100) \
            if total_attempts > 0 else 0
        
        return {
            'total_agent_calls': total_calls,
            'avg_response_time': avg_response_time,
            'success_rate': success_rate,
            'total_errors': len(self.metrics['errors']),
            'agent_breakdown': self.metrics['agent_calls'],
            'tool_usage': self.metrics['tool_calls']
        }
    
    def export_metrics(self, filepath: str):
        """Export metrics to JSON file"""
        with open(filepath, 'w') as f:
            json.dump(self.metrics, f, indent=2)


def trace_agent_execution(agent_name: str):
    """
    Decorator to automatically trace agent execution
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            
            try:
                result = func(*args, **kwargs)
                duration = time.time() - start_time
                
                # Log success
                if hasattr(args[0], 'logger'):
                    args[0].logger.log_agent_complete(agent_name, func.__name__, duration)
                
                return result
                
            except Exception as e:
                duration = time.time() - start_time
                
                # Log error
                if hasattr(args[0], 'logger'):
                    args[0].logger.log_agent_error(agent_name, str(e))
                
                raise
        
        return wrapper
    return decorator


# Global instances
logger = AgentLogger()
tracer = AgentTracer()
metrics = MetricsCollector()
