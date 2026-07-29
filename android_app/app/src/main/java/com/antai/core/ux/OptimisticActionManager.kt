package com.antai.core.ux

/**
 * ANT optimistic action controller.
 *
 * UI changes should happen immediately, while the remote operation is
 * reconciled in the background. On failure the previous state is restored.
 */
class OptimisticActionManager {

    suspend fun <T> execute(
        previousState: T,
        applyOptimistic: () -> Unit,
        commit: suspend () -> Result<T>,
        rollback: (T) -> Unit,
        onError: (String) -> Unit
    ): T? {
        applyOptimistic()

        val result = commit()

        return result.fold(
            onSuccess = { confirmed -> confirmed },
            onFailure = { error ->
                rollback(previousState)
                onError(error.message ?: "Action failed")
                null
            }
        )
    }
}
