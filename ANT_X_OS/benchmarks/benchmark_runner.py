import time

class BenchmarkRunner:
    def run(self, task):
        start = time.time()
        result = task()
        return {
            "duration": time.time() - start,
            "success": True,
            "result": result
        }
