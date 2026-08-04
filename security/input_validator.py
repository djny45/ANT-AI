"""Input validation and sanitization for ANT AI."""

import re
from typing import Any, Dict, List
import html

class InputValidator:
    """Validates and sanitizes user input to prevent injection attacks."""
    
    # FIX: XSS prevention patterns
    DANGEROUS_PATTERNS = [
        r'<script[^>]*>.*?</script>',
        r'javascript:',
        r'on\w+\s*=',  # Event handlers
        r'<iframe',
        r'<object',
        r'<embed',
    ]
    
    # FIX: SQL injection patterns
    SQL_INJECTION_PATTERNS = [
        r'(\bOR\b|\bAND\b|\bUNION\b)\s+\d+\s*=\s*\d+',
        r'(DROP|DELETE|INSERT|UPDATE)\s+(TABLE|DATABASE)',
        r'--\s*$',  # SQL comments
    ]
    
    def __init__(self):
        self.compiled_dangerous = [re.compile(p, re.IGNORECASE) for p in self.DANGEROUS_PATTERNS]
        self.compiled_sql = [re.compile(p, re.IGNORECASE) for p in self.SQL_INJECTION_PATTERNS]
    
    def validate_string(self, value: str, max_length: int = 10000) -> bool:
        """Validate string input."""
        if not isinstance(value, str):
            return False
        
        # FIX: Length check to prevent DoS
        if len(value) > max_length:
            return False
        
        # Check for XSS
        if self._has_xss(value):
            return False
        
        # Check for SQL injection
        if self._has_sql_injection(value):
            return False
        
        return True
    
    def sanitize_string(self, value: str) -> str:
        """Sanitize string by escaping HTML."""
        return html.escape(value)
    
    def validate_input(self, data: Dict[str, Any]) -> bool:
        """Validate user input dictionary."""
        for key, value in data.items():
            if isinstance(value, str) and not self.validate_string(value):
                return False
            elif isinstance(value, dict) and not self.validate_input(value):
                return False
            elif isinstance(value, list):
                for item in value:
                    if isinstance(item, str) and not self.validate_string(item):
                        return False
                    elif isinstance(item, dict) and not self.validate_input(item):
                        return False
        return True
    
    def _has_xss(self, value: str) -> bool:
        """Check for XSS patterns."""
        return any(pattern.search(value) for pattern in self.compiled_dangerous)
    
    def _has_sql_injection(self, value: str) -> bool:
        """Check for SQL injection patterns."""
        return any(pattern.search(value) for pattern in self.compiled_sql)
