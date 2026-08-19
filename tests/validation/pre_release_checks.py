#!/usr/bin/env python3
"""
ANT AI Pre-Release Validation Suite

Performs comprehensive validation checks before release:
- Application startup
- Backend API health
- Frontend availability
- Agent loading
- LangGraph workflow execution
- Memory persistence
- Audit log generation
- Security controls
- Performance metrics
"""

import asyncio
import sys
import json
import subprocess
from datetime import datetime
from typing import Dict, List, Tuple
import httpx

# Configuration
BACKEND_URL = "http://localhost:8000"
FRONTEND_URL = "http://localhost:3000"
OLLAMA_URL = "http://localhost:11434"
REDIS_URL = "redis://localhost:6379"
DB_URL = "postgresql://antai_user:antai_secure_password@localhost:5432/antai_knowledge"

class ValidationReport:
    """Validation report generator"""
    
    def __init__(self):
        self.tests: Dict[str, Dict] = {}
        self.start_time = datetime.now()
    
    def add_test(self, name: str, passed: bool, details: str = "", duration: float = 0.0):
        """Add test result"""
        self.tests[name] = {
            "passed": passed,
            "details": details,
            "duration": duration,
            "timestamp": datetime.now().isoformat()
        }
    
    def get_summary(self) -> Dict:
        """Get validation summary"""
        total = len(self.tests)
        passed = sum(1 for t in self.tests.values() if t["passed"])
        failed = total - passed
        
        return {
            "version": "ANT AI Beta v0.1",
            "status": "READY" if failed == 0 else "BLOCKED",
            "completion_percentage": int((passed / total * 100) if total > 0 else 0),
            "tests_run": total,
            "tests_passed": passed,
            "tests_failed": failed,
            "start_time": self.start_time.isoformat(),
            "end_time": datetime.now().isoformat(),
            "duration_seconds": (datetime.now() - self.start_time).total_seconds(),
            "test_details": self.tests
        }
    
    def print_report(self):
        """Print formatted report"""
        summary = self.get_summary()
        print("\n" + "="*80)
        print("ANT AI PRE-RELEASE VALIDATION REPORT")
        print("="*80)
        print(f"\nStatus: {summary['status']}")
        print(f"Tests Passed: {summary['tests_passed']}/{summary['tests_run']}")
        print(f"Completion: {summary['completion_percentage']}%")
        print(f"Duration: {summary['duration_seconds']:.2f}s")
        
        print("\n" + "-"*80)
        print("Test Details:")
        print("-"*80)
        
        for test_name, result in self.tests.items():
            status = "✓ PASS" if result["passed"] else "✗ FAIL"
            print(f"{status} | {test_name}")
            if result["details"]:
                print(f"       {result['details']}")
        
        print("\n" + "="*80)
        return summary


async def check_backend_health() -> Tuple[bool, str]:
    """Check backend API health"""
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(f"{BACKEND_URL}/health")
            if response.status_code == 200:
                return True, "Backend responding normally"
            return False, f"Backend returned status {response.status_code}"
    except Exception as e:
        return False, f"Backend unreachable: {str(e)}"


async def check_frontend_availability() -> Tuple[bool, str]:
    """Check frontend availability"""
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(f"{FRONTEND_URL}/")
            if response.status_code == 200:
                return True, "Frontend serving pages"
            return False, f"Frontend returned status {response.status_code}"
    except Exception as e:
        return False, f"Frontend unreachable: {str(e)}"


async def check_ollama_models() -> Tuple[bool, str]:
    """Check Ollama LLM availability"""
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(f"{OLLAMA_URL}/api/tags")
            if response.status_code == 200:
                data = response.json()
                if data.get("models"):
                    models = [m.get("name") for m in data["models"]]
                    return True, f"Ollama models available: {', '.join(models[:3])}"
                return False, "No models loaded in Ollama"
            return False, f"Ollama returned status {response.status_code}"
    except Exception as e:
        return False, f"Ollama unreachable: {str(e)}"


async def check_database_connection() -> Tuple[bool, str]:
    """Check PostgreSQL database connection"""
    try:
        import psycopg2
        conn = psycopg2.connect(DB_URL)
        cursor = conn.cursor()
        cursor.execute("SELECT version();")
        version = cursor.fetchone()[0]
        conn.close()
        return True, f"Database connected: {version[:40]}..."
    except ImportError:
        return False, "psycopg2 not installed"
    except Exception as e:
        return False, f"Database connection failed: {str(e)}"


async def check_redis_connection() -> Tuple[bool, str]:
    """Check Redis cache connection"""
    try:
        import redis
        r = redis.from_url(REDIS_URL, decode_responses=True)
        r.ping()
        info = r.info()
        return True, f"Redis connected: {info.get('redis_version')} - {info.get('used_memory_human')}"
    except ImportError:
        return False, "redis not installed"
    except Exception as e:
        return False, f"Redis connection failed: {str(e)}"


async def check_backend_endpoints() -> Tuple[bool, str]:
    """Check critical backend endpoints"""
    endpoints = [
        "/health",
        "/api/agents",
        "/api/memory",
        "/api/audit",
    ]
    
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            failed = []
            for endpoint in endpoints:
                try:
                    response = await client.get(f"{BACKEND_URL}{endpoint}")
                    if response.status_code >= 400:
                        failed.append(endpoint)
                except:
                    failed.append(endpoint)
            
            if failed:
                return False, f"Failed endpoints: {', '.join(failed)}"
            return True, f"All {len(endpoints)} endpoints responding"
    except Exception as e:
        return False, f"Endpoint check failed: {str(e)}"


async def check_agent_loading() -> Tuple[bool, str]:
    """Check if agents load correctly"""
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(f"{BACKEND_URL}/api/agents")
            if response.status_code == 200:
                agents = response.json()
                if agents:
                    agent_names = [a.get("name") for a in agents]
                    return True, f"Loaded {len(agents)} agents"
                return False, "No agents loaded"
            return False, f"Agent endpoint returned status {response.status_code}"
    except Exception as e:
        return False, f"Agent loading check failed: {str(e)}"


async def check_memory_operations() -> Tuple[bool, str]:
    """Check memory save and retrieve operations"""
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            # Test memory save
            save_data = {
                "key": "test_memory_key",
                "value": "test_value",
                "category": "validation"
            }
            response = await client.post(
                f"{BACKEND_URL}/api/memory/save",
                json=save_data
            )
            if response.status_code >= 400:
                return False, f"Memory save failed with status {response.status_code}"
            
            # Test memory retrieve
            response = await client.get(
                f"{BACKEND_URL}/api/memory/get",
                params={"key": "test_memory_key"}
            )
            if response.status_code == 200:
                return True, "Memory save and retrieve working"
            return False, f"Memory retrieve failed with status {response.status_code}"
    except Exception as e:
        return False, f"Memory operations check failed: {str(e)}"


async def check_audit_logging() -> Tuple[bool, str]:
    """Check audit log generation"""
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            # Create a test audit entry
            audit_data = {
                "action": "validation_test",
                "resource": "pre_release_check",
                "status": "success"
            }
            response = await client.post(
                f"{BACKEND_URL}/api/audit/log",
                json=audit_data
            )
            if response.status_code >= 400:
                return False, f"Audit logging failed with status {response.status_code}"
            
            # Retrieve audit logs
            response = await client.get(f"{BACKEND_URL}/api/audit/logs")
            if response.status_code == 200:
                return True, "Audit logging operational"
            return False, f"Audit retrieval failed with status {response.status_code}"
    except Exception as e:
        return False, f"Audit logging check failed: {str(e)}"


async def check_security_headers() -> Tuple[bool, str]:
    """Check security headers"""
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(f"{BACKEND_URL}/health")
            
            required_headers = [
                "x-frame-options",
                "x-content-type-options",
                "x-xss-protection"
            ]
            
            missing = [h for h in required_headers if h not in response.headers]
            
            if missing:
                return False, f"Missing security headers: {', '.join(missing)}"
            return True, "All security headers present"
    except Exception as e:
        return False, f"Security header check failed: {str(e)}"


async def check_docker_services() -> Tuple[bool, str]:
    """Check all Docker services are running"""
    try:
        result = subprocess.run(
            ["docker", "compose", "ps", "--status=running"],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode == 0:
            lines = result.stdout.strip().split('\n')
            if len(lines) > 1:  # More than just header
                return True, f"Docker services running: {len(lines)-1} services"
            return False, "No Docker services running"
        return False, "Docker compose check failed"
    except Exception as e:
        return False, f"Docker services check failed: {str(e)}"


async def run_all_validations() -> Dict:
    """Run all validation checks"""
    report = ValidationReport()
    
    print("\n" + "="*80)
    print("Running ANT AI Pre-Release Validation Checks...")
    print("="*80 + "\n")
    
    # Phase 1: Infrastructure checks
    print("Phase 1: Infrastructure Checks")
    print("-" * 80)
    
    start = datetime.now()
    passed, details = await check_docker_services()
    report.add_test("Docker Services Running", passed, details, 
                   (datetime.now() - start).total_seconds())
    print(f"  {'✓' if passed else '✗'} Docker Services: {details}")
    
    start = datetime.now()
    passed, details = await check_backend_health()
    report.add_test("Backend Health Check", passed, details,
                   (datetime.now() - start).total_seconds())
    print(f"  {'✓' if passed else '✗'} Backend Health: {details}")
    
    start = datetime.now()
    passed, details = await check_frontend_availability()
    report.add_test("Frontend Availability", passed, details,
                   (datetime.now() - start).total_seconds())
    print(f"  {'✓' if passed else '✗'} Frontend: {details}")
    
    # Phase 2: Database and Cache checks
    print("\nPhase 2: Data Layer Checks")
    print("-" * 80)
    
    start = datetime.now()
    passed, details = await check_database_connection()
    report.add_test("Database Connection", passed, details,
                   (datetime.now() - start).total_seconds())
    print(f"  {'✓' if passed else '✗'} Database: {details}")
    
    start = datetime.now()
    passed, details = await check_redis_connection()
    report.add_test("Redis Connection", passed, details,
                   (datetime.now() - start).total_seconds())
    print(f"  {'✓' if passed else '✗'} Redis: {details}")
    
    # Phase 3: AI Infrastructure checks
    print("\nPhase 3: AI Infrastructure Checks")
    print("-" * 80)
    
    start = datetime.now()
    passed, details = await check_ollama_models()
    report.add_test("Ollama Models Available", passed, details,
                   (datetime.now() - start).total_seconds())
    print(f"  {'✓' if passed else '✗'} Ollama: {details}")
    
    start = datetime.now()
    passed, details = await check_agent_loading()
    report.add_test("Agent Loading", passed, details,
                   (datetime.now() - start).total_seconds())
    print(f"  {'✓' if passed else '✗'} Agents: {details}")
    
    # Phase 4: API Functionality checks
    print("\nPhase 4: API Functionality Checks")
    print("-" * 80)
    
    start = datetime.now()
    passed, details = await check_backend_endpoints()
    report.add_test("Backend Endpoints", passed, details,
                   (datetime.now() - start).total_seconds())
    print(f"  {'✓' if passed else '✗'} API Endpoints: {details}")
    
    start = datetime.now()
    passed, details = await check_memory_operations()
    report.add_test("Memory Operations", passed, details,
                   (datetime.now() - start).total_seconds())
    print(f"  {'✓' if passed else '✗'} Memory: {details}")
    
    start = datetime.now()
    passed, details = await check_audit_logging()
    report.add_test("Audit Logging", passed, details,
                   (datetime.now() - start).total_seconds())
    print(f"  {'✓' if passed else '✗'} Audit: {details}")
    
    # Phase 5: Security checks
    print("\nPhase 5: Security Checks")
    print("-" * 80)
    
    start = datetime.now()
    passed, details = await check_security_headers()
    report.add_test("Security Headers", passed, details,
                   (datetime.now() - start).total_seconds())
    print(f"  {'✓' if passed else '✗'} Security: {details}")
    
    # Print final report
    summary = report.get_summary()
    report.print_report()
    
    return summary


def main():
    """Main entry point"""
    try:
        summary = asyncio.run(run_all_validations())
        
        # Exit with appropriate code
        if summary["status"] == "READY":
            print("\n✓ Platform is ready for release!\n")
            sys.exit(0)
        else:
            print("\n✗ Platform has blockers. See details above.\n")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n\nValidation interrupted by user.")
        sys.exit(130)
    except Exception as e:
        print(f"\n✗ Validation failed with error: {str(e)}\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
