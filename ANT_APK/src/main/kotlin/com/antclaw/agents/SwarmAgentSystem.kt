package com.antclaw.agents

/**
 * Swarm architecture foundation.
 * Each primary agent can manage specialized sub-agents.
 */

interface SwarmAgent {
    val name: String
    val subAgents: List<String>
}

class CodeSwarm : SwarmAgent {
    override val name = "Code Commander"
    override val subAgents = listOf(
        "Bug Hunter",
        "Optimizer",
        "Test Agent",
        "Security Agent"
    )
}

class ResearchSwarm : SwarmAgent {
    override val name = "Research Commander"
    override val subAgents = listOf(
        "Trend Scanner",
        "Paper Analyzer",
        "Repository Scout"
    )
}
