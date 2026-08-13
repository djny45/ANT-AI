"""ANT AI runtime kernel."""

import asyncio
from core_state.sqlite_state import SQLiteState
from llm.ollama_client import OllamaClient


class AntKernel:
    def __init__(self, db_path="ant_state.db"):
        self.loop = None
        self.state = SQLiteState(db_path)
        self.llm = OllamaClient()

    async def initialize(self):
        self.state.initialize()
        await self.llm.health_check()
        return {"kernel": "ANT", "status": "initialized"}

    def start(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        return self.loop.run_until_complete(self.initialize())
