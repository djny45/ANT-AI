package plugins.base_agent

/**
 * Base contract for ANT AI agents.
 * Plugins implement this interface to become discoverable agents.
 */
interface AgentPlugin {
    val id: String
    val name: String
    val version: String
    val description: String

    fun initialize()

    fun execute(input: String): String

    fun shutdown()
}
