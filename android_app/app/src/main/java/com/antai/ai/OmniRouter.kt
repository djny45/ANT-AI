package com.antai.ai

import kotlinx.coroutines.flow.Flow

class OmniRouter(
    private val providers: List<ModelProvider> = emptyList()
) {
    suspend fun chat(request: AIRequest): Flow<String> {
        val provider = providers.firstOrNull()
            ?: error("No AI provider configured")
        return provider.chat(request)
    }
}
