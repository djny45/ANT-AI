package memory

/**
 * Shared memory storage layer for ANT AI agents.
 * Provides persistent knowledge access between agents.
 */
object KnowledgeHive {
    private val records = mutableListOf<KnowledgeRecord>()

    fun store(record: KnowledgeRecord) {
        records.add(record)
    }

    fun retrieveByAgent(agentId: String): List<KnowledgeRecord> {
        return records.filter { it.agentId == agentId }
    }

    fun search(keyword: String): List<KnowledgeRecord> {
        return records.filter { record ->
            record.content.contains(keyword, ignoreCase = true) ||
                record.tags.any { tag -> tag.contains(keyword, ignoreCase = true) }
        }
    }

    fun all(): List<KnowledgeRecord> {
        return records.toList()
    }

    fun clear() {
        records.clear()
    }
}
