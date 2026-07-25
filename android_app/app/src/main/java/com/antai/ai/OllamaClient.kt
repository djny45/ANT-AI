package com.antai.ai

import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.flow
import kotlinx.coroutines.delay

class OllamaClient(
    private val endpoint: String = "http://localhost:11434",
    private val model: String = "llama3"
) {
    fun streamResponse(prompt: String): Flow<String> = flow {
        // Ollama /api/chat streaming pipeline
        // HTTP implementation hook ready for OkHttp integration.
        val response = "Ollama($model): response stream for $prompt"

        response.split(" ").forEach { token ->
            emit("$token ")
            delay(60)
        }
    }
}
