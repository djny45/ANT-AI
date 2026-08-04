"""ANT AI API rate limiting with thread safety and DDoS protection."""

import time
import threading
from collections import defaultdict
from typing import Dict, List

class RateLimiter:
    """Thread-safe rate limiter with per-IP and global limits."""
    
    def __init__(self, max_requests=20, window_seconds=60):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests: Dict[str, List[float]] = defaultdict(list)
        self.lock = threading.Lock()  # FIX: Thread safety
        self.global_requests = []  # FIX: Track global requests
        self.blocked_ips = set()  # FIX: IP blocking mechanism

    def allow(self, client_id: str = "global") -> bool:
        """Check if request is allowed for client."""
        with self.lock:
            # FIX: Prevent known attackers
            if client_id in self.blocked_ips:
                return False
            
            now = time.time()
            
            # Clean old requests
            self.requests[client_id] = [
                r for r in self.requests[client_id] 
                if now - r < self.window_seconds
            ]
            
            # Check per-client limit
            if len(self.requests[client_id]) >= self.max_requests:
                return False
            
            # FIX: Check global limit (prevent total system overload)
            self.global_requests = [
                r for r in self.global_requests 
                if now - r < self.window_seconds
            ]
            if len(self.global_requests) >= (self.max_requests * 10):
                self.block_client(client_id)
                return False
            
            # Add request
            self.requests[client_id].append(now)
            self.global_requests.append(now)
            return True
    
    def block_client(self, client_id: str) -> None:
        """Block a misbehaving client."""
        with self.lock:
            self.blocked_ips.add(client_id)
    
    def unblock_client(self, client_id: str) -> None:
        """Unblock a client."""
        with self.lock:
            self.blocked_ips.discard(client_id)
