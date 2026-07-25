package memory.hive

/**
 * Controls memory permissions for agents.
 */
data class MemoryPolicy(
    val allowRead: Boolean = true,
    val allowWrite: Boolean = true,
    val shared: Boolean = false
)
