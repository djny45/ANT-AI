package tools.registry

import tools.base.Tool

/**
 * Central registry for ANT AI tools.
 */
object ToolRegistry {
    private val tools = mutableMapOf<String, Tool>()

    fun register(tool: Tool) {
        tools[tool.id] = tool
    }

    fun unregister(id: String) {
        tools.remove(id)
    }

    fun get(id: String): Tool? {
        return tools[id]
    }

    fun list(): List<Tool> {
        return tools.values.toList()
    }
}
