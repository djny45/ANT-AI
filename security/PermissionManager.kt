package security

/**
 * Controls permissions for ANT AI agent actions.
 */
object PermissionManager {
    private val permissions = mutableMapOf<String, MutableSet<String>>()

    fun grant(agentId: String, permission: String) {
        permissions.getOrPut(agentId) { mutableSetOf() }.add(permission)
    }

    fun revoke(agentId: String, permission: String) {
        permissions[agentId]?.remove(permission)
    }

    fun hasPermission(agentId: String, permission: String): Boolean {
        return permissions[agentId]?.contains(permission) == true
    }
}
