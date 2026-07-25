package plugins.registry

import plugins.base_agent.AgentPlugin

/**
 * Registry for loading and managing ANT AI plugins.
 */
object AgentRegistry {
    private val agents = mutableMapOf<String, AgentPlugin>()

    fun register(agent: AgentPlugin) {
        agents[agent.id] = agent
    }

    fun unregister(id: String) {
        agents.remove(id)
    }

    fun get(id: String): AgentPlugin? {
        return agents[id]
    }

    fun list(): List<AgentPlugin> {
        return agents.values.toList()
    }
}
