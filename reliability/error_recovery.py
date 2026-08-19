"""ANT AI error recovery foundation."""


class ErrorRecovery:
    def recover(self, error, stage="unknown"):
        message = str(error)
        if isinstance(error, TimeoutError) or "timeout" in message.lower():
            recovery_action = "retry_stage"
        elif stage == "capability" and (
            isinstance(error, LookupError) or "capability" in message.lower()
        ):
            recovery_action = "use_fallback_capability"
        elif stage == "executor":
            recovery_action = "use_fallback_executor"
        elif stage in {"planner", "verifier"}:
            recovery_action = "retry_model"
        else:
            recovery_action = "continue_with_partial_results"
        return {
            "error": message,
            "stage": stage,
            "recovery_action": recovery_action,
        }
