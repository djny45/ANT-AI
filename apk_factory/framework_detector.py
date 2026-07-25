"""Detect project framework before APK generation."""

class FrameworkDetector:
    def detect(self, project):
        return {
            "project": project,
            "framework": "unknown",
            "status": "analysis_required"
        }
