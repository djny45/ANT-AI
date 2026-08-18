"""
ANT AI LangGraph authenticated chat integration.

Bridge between API sessions and graph execution.
Keeps user identity, permissions, memory context and audit metadata
attached to every graph run.
"""

from dataclasses import dataclass, field
from typing import Any, Dict


@dataclass
class GraphChatRequest:
    user_id: str
    message: str
    conversation_id: str | None = None
    metadata: Dict[str, Any] = field(default_factory=dict)


class AuthenticatedGraphRunner:
    """Execution boundary for authenticated user requests."""

    def __init__(self, graph_runtime=None, memory=None, audit=None):
        self.graph_runtime = graph_runtime
        self.memory = memory
        self.audit = audit

    async def execute(self, request: GraphChatRequest):
        context = {
            "user_id": request.user_id,
            "conversation_id": request.conversation_id,
            "permissions": request.metadata.get("permissions", []),
        }

        if self.audit:
            await self.audit.log({
                "event": "graph_request_started",
                "user_id": request.user_id,
            })

        if self.memory:
            context["memory"] = await self.memory.retrieve(request.user_id)

        result = await self.graph_runtime.run(
            user_input=request.message,
            context=context,
        )

        if self.memory:
            await self.memory.save(
                request.user_id,
                request.message,
                result,
            )

        if self.audit:
            await self.audit.log({
                "event": "graph_request_completed",
                "user_id": request.user_id,
            })

        return result
