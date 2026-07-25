package com.antai.agents.core

class AgentRegistry {
    private val agents = mutableMapOf<String, Agent>()

    fun register(agent: Agent) {
        agents[agent.name] = agent
    }

    fun get(name: String): Agent? {
        return agents[name]
    }

    fun list(): List<String> {
        return agents.keys.toList()
    }
}
