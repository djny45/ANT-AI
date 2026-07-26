package com.antai.ai

import kotlinx.coroutines.flow.Flow

class RouterChatService(
    private val router: OmniRouter
) {
    suspend fun send(message: String): Flow<String> {
        return router.chat(
            AIRequest(
                message = message,
                model = "auto"
            )
        )
    }
}
