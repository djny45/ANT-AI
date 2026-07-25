package com.antai.integrations.omniroute

interface RouteStrategy {
    fun selectProvider(
        providers: List<ProviderAdapter>,
        task: String
    ): ProviderAdapter?
}
