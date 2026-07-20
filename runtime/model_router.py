"""ANT AI lightweight model router."""

class ModelRouter:
    def choose(self, task, device):
        if device.get("ram", 0) < 8:
            return "small_quantized_model"
        return "larger_local_model"
