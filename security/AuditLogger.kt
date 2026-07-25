package security

/**
 * Records security events from agents and tools.
 */
object AuditLogger {
    private val events = mutableListOf<String>()

    fun log(event: String) {
        events.add(event)
    }

    fun history(): List<String> {
        return events.toList()
    }

    fun clear() {
        events.clear()
    }
}
