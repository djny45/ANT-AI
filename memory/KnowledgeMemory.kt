package memory

/**
 * Core memory object stored inside the ANT AI Knowledge Hive.
 */
data class KnowledgeMemory(
    val id: String,
    val owner: String,
    val content: String,
    val category: String,
    val timestamp: Long = System.currentTimeMillis()
)
