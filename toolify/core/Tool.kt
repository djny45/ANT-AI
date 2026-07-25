package com.antai.toolify.core

interface Tool {
    val name: String
    val description: String

    suspend fun execute(input: Map<String, Any>): ToolResult
}
