package com.antai.core.ux

/**
 * ANT Optimistic Action Manager
 *
 * Provides a reusable pattern:
 * 1. Apply UI state immediately
 * 2. Execute remote operation
 * 3. Confirm or rollback
 */
class OptimisticActionManager {

    suspend fun <T> execute(
        optimisticUpdate: () -> Unit,
        rollback: () -> Unit,
        action: suspend () -> Result<T>,
        onError: (String) -> Unit
    ) {
        optimisticUpdate()

        val result = action()

        if (result.isFailure) {
            rollback()
            onError(
                result.exceptionOrNull()?.message
                    ?: "Action failed and was restored"
            )
        }
    }
}
