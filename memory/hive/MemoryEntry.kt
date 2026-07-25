package memory.hive

/**
 * A single Knowledge Hive memory record.
 */
data class MemoryEntry(
    val id: String,
    val agentId: String,
    val content: String,
    val timestamp: Long,
    val tags: List<String> = emptyList()
)
