package com.antai.agents.core

data class AgentTask(
    val id: String,
    val input: String,
    val metadata: Map<String, String> = emptyMap()
)
