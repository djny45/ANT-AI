package com.antai.integrations.omniroute

class FallbackManager(
    private val providers: List<ProviderAdapter>
) {
    suspend fun execute(
        model: String,
        prompt: String
    ): String {
        var lastError: Exception? = null

        for (provider in providers) {
            try {
                return provider.complete(model, prompt)
            } catch (error: Exception) {
                lastError = error
            }
        }

        throw lastError ?: IllegalStateException("No providers available")
    }
}
