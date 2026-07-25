package intelligence

/**
 * Executes planned ANT AI tasks.
 */
object TaskExecutor {
    fun execute(plan: List<String>): String {
        return plan.joinToString(" -> ")
    }
}
