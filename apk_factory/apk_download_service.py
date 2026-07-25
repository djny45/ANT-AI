"""ANT AI APK artifact delivery service."""

class APKDownloadService:
    def create_link(self, artifact):
        return {"artifact": artifact, "status": "download_ready"}
