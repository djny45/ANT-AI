package com.antai.ai

import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.flow

class OllamaHttpClient {
    fun chatStream(prompt: String): Flow<String> = flow {
        // OkHttp streaming integration hook.
        emit(prompt)
    }
}
