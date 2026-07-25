package com.antai.integrations.omniroute

interface ProviderAdapter {
    val providerName: String
    val models: List<String>

    suspend fun complete(
        model: String,
        prompt: String
    ): String
}
