package security

/**
 * Defines sandbox restrictions for agents.
 */
data class SandboxPolicy(
    val allowNetwork: Boolean = false,
    val allowFileWrite: Boolean = false,
    val allowSystemActions: Boolean = false
)
