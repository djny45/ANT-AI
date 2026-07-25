package com.antai.ai

import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.flow

class OllamaClient(
    private val endpoint: String = "http://localhost:11434"
) {
    fun streamResponse(prompt: String): Flow<String> = flow {
        // TODO: Connect HTTP streaming endpoint /api/chat
        // Each emitted value represents a streamed token.
        emit("Ollama connection ready: ")
        emit(prompt)
    }
}
