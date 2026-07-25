package com.antai.ai

import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.flow

class OllamaStreamService(
    private val client: OllamaClient = OllamaClient()
) {
    fun chat(prompt: String): Flow<String> {
        return client.streamResponse(prompt)
    }
}
