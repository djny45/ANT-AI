package com.antai.core

class ANTBridge {
    fun executeTask(task: String): String {
        val normalized = task.trim().lowercase()
        if (normalized.isBlank()) return "Tell me what you want ANT to do."

        val route = when {
            normalized.hasAny("apk", "android", "build", "release") -> TaskRoute(
                agent = "APK Factory + Coding Ant",
                action = "Build inspection, Gradle validation, APK packaging, checksum generation",
                result = "I will treat this as a mobile release task and check build safety before packaging."
            )
            normalized.hasAny("security", "scan", "audit", "secret") -> TaskRoute(
                agent = "Security Ant",
                action = "Threat review, secret hygiene, permissions audit, release gate",
                result = "I will run this through the security gate before any release step."
            )
            normalized.hasAny("research", "find", "web", "github") -> TaskRoute(
                agent = "Research Ant",
                action = "Source discovery, issue review, release note extraction, summary",
                result = "I will collect relevant repository signals and return the strongest next move."
            )
            normalized.hasAny("code", "fix", "feature", "ui", "interface") -> TaskRoute(
                agent = "Coding Ant",
                action = "Codebase mapping, implementation plan, patch, build verification",
                result = "I will make the app usable first, then polish the experience."
            )
            else -> TaskRoute(
                agent = "Commander Ant",
                action = "Intent classification, swarm routing, execution checklist",
                result = "I will break this into an executable swarm plan."
            )
        }

        return buildString {
            appendLine(route.result)
            appendLine()
            appendLine("Agent: ${route.agent}")
            appendLine("Action: ${route.action}")
            appendLine("Status: Ready for execution")
            appendLine()
            append("Task: $task")
        }
    }

    fun dashboardStatus(): List<String> = listOf(
        "Chat command center online",
        "APK factory connected",
        "Security gate armed",
        "Knowledge hive ready",
        "Offline routing active"
    )

    private fun String.hasAny(vararg terms: String): Boolean = terms.any { contains(it) }

    private data class TaskRoute(val agent: String, val action: String, val result: String)
}
