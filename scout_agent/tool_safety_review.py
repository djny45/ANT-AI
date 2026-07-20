"""ANT AI tool safety review."""

class ToolSafetyReview:
    def review(self, tool):
        return {
            "tool": tool,
            "checked": True,
            "approved": False,
            "needs_validation": True
        }
