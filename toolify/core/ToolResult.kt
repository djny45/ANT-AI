package com.antai.toolify.core

sealed class ToolResult {
    data class Success(val data: Any) : ToolResult()
    data class Error(val message: String) : ToolResult()
}
