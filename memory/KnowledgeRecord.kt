package memory

/**
 * A single Knowledge Hive memory record.
 */
data class KnowledgeRecord(
    val id: String,
    val agentId: String,
    val content: String,
    val timestamp: Long,
    val tags: List<String> = emptyList()
)
