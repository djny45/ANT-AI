package com.antclaw.core

/**
 * ANT CLAW Omni Router foundation.
 * Routes requests to the best available agent.
 */
class OmniRouter {

    fun route(input: String): String {
        return when {
            input.contains("code", ignoreCase = true) -> "CodeAgent"
            input.contains("research", ignoreCase = true) -> "ResearchAgent"
            input.contains("write", ignoreCase = true) -> "WriterAgent"
            else -> "GeneralAgent"
        }
    }
}
