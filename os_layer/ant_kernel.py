"""ANT AI runtime kernel.

Model providers are selected by the unified API runtime; this legacy kernel
only owns local state initialization and never starts a provider-specific model.
"""

import asyncio
from core_state.sqlite_state import SQLiteState


class AntKernel:
    def __init__(self, db_path="ant_state.db"):
        self.loop = None
        self.state = SQLiteState(db_path)

    async def initialize(self):
        self.state.initialize()
        return {"kernel": "ANT", "status": "initialized"}

    def start(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        return self.loop.run_until_complete(self.initialize())
