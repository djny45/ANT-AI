package com.antai.ai

import kotlinx.coroutines.flow.Flow

interface ModelProvider {
    suspend fun chat(request: AIRequest): Flow<String>
}
