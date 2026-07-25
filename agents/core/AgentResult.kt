package com.antai.agents.core

data class AgentResult(
    val success: Boolean,
    val output: String,
    val error: String? = null
)
