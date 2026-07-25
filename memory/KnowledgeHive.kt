package memory

/**
 * Shared memory manager for ANT AI agents.
 */
object KnowledgeHive {
    private val memories = mutableListOf<KnowledgeMemory>()

    fun store(memory: KnowledgeMemory) {
        memories.add(memory)
    }

    fun search(query: String): List<KnowledgeMemory> {
        return memories.filter {
            it.content.contains(query, ignoreCase = true) ||
            it.category.contains(query, ignoreCase = true)
        }
    }

    fun all(): List<KnowledgeMemory> {
        return memories.toList()
    }

    fun clear() {
        memories.clear()
    }
}
