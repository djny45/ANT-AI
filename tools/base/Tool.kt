package tools.base

/**
 * Base contract for ANT AI tools.
 * Agents use tools through the registry layer.
 */
interface Tool {
    val id: String
    val name: String
    val description: String

    fun execute(input: String): String
}
