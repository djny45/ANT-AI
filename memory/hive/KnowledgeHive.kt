package memory.hive

/**
 * Shared memory layer for ANT AI agents.
 */
object KnowledgeHive {

    private val memories = mutableListOf<MemoryEntry>()

    fun store(entry: MemoryEntry) {
        memories.add(entry)
    }

    fun recall(agentId: String? = null): List<MemoryEntry> {
        return if (agentId == null) {
            memories.toList()
        } else {
            memories.filter { it.agentId == agentId }
        }
    }

    fun search(keyword: String): List<MemoryEntry> {
        return memories.filter {
            it.content.contains(keyword, ignoreCase = true) ||
            it.tags.any { tag -> tag.contains(keyword, ignoreCase = true) }
        }
    }

    fun clear() {
        memories.clear()
    }
}
