package com.antai.agents.core

interface Agent {
    val name: String
    val description: String

    suspend fun execute(task: AgentTask): AgentResult
}
