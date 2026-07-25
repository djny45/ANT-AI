"""ANT AI APK build cache manager."""

class BuildCache:
    def store(self, project, result):
        return {"project": project, "cached": True, "result": result}
