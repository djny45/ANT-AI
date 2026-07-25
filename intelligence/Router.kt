package intelligence

/**
 * Routes tasks to the correct ANT AI agent.
 */
object Router {
    fun route(task: String): String {
        return "general_agent"
    }
}
