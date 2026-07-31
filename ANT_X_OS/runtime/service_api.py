class ANTService:
    def __init__(self, runtime):
        self.runtime = runtime

    def build_app(self, request):
        return self.runtime.execute(request)
