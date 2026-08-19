from statistics import mean, median
from typing import Any

from .base import BaseCapability


class DataAnalysisCapability(BaseCapability):
    capability_name = "Data Skill"
    execution_target = "data"
    handler_name = "data_analysis_capability"

    def run(self, *, task: dict[str, Any], context: dict[str, Any]) -> dict[str, Any]:
        request = self.request_text(task, context)
        dataset = task.get("dataset")
        if dataset is None:
            dataset = context.get("dataset")
        if not isinstance(dataset, list):
            result = {
                "mode": "analysis_plan",
                "objective": request,
                "steps": [
                    "Load the dataset and inspect its schema.",
                    "Measure missing values and infer field types.",
                    "Compute numeric summary statistics.",
                ],
                "dataset_provided": False,
                "headline": "Prepared a request-derived data analysis plan; no dataset was provided.",
                "skill_metadata": self.skill_metadata(),
            }
            verification = {
                "dataset_provided": False,
                "evidence": "No list-based dataset was provided.",
            }
            return self.envelope(
                result=result,
                confidence=self.derive_confidence(request, 0, 4),
                verification=verification,
            )

        if all(isinstance(value, (int, float)) and not isinstance(value, bool) for value in dataset):
            rows = [{"value": value} for value in dataset]
        elif all(isinstance(value, dict) for value in dataset):
            rows = dataset
        else:
            rows = [{"value": value} for value in dataset]

        fields = sorted({field for row in rows for field in row})
        inferred_types: dict[str, list[str]] = {}
        missing_values: dict[str, int] = {}
        numeric_statistics: dict[str, dict[str, float | int]] = {}
        for field in fields:
            values = [row.get(field) for row in rows]
            present = [value for value in values if value is not None]
            type_names = sorted({
                type(value).__name__
                for value in present
            })
            inferred_types[field] = type_names or ["null"]
            missing_values[field] = len(values) - len(present)
            numeric_values = [
                value
                for value in present
                if isinstance(value, (int, float)) and not isinstance(value, bool)
            ]
            if numeric_values:
                numeric_statistics[field] = {
                    "min": min(numeric_values),
                    "max": max(numeric_values),
                    "mean": mean(numeric_values),
                    "median": median(numeric_values),
                }

        result = {
            "mode": "dataset_analysis",
            "dataset_provided": True,
            "row_count": len(rows),
            "field_count": len(fields),
            "fields": fields,
            "inferred_types": inferred_types,
            "missing_values": missing_values,
            "numeric_statistics": numeric_statistics,
            "headline": (
                f"Analyzed {len(rows)} row(s) across {len(fields)} field(s)."
            ),
            "skill_metadata": self.skill_metadata(),
        }
        verification = {
            "dataset_provided": True,
            "row_count": len(rows),
            "field_count": len(fields),
            "fields": fields,
            "numeric_fields": sorted(numeric_statistics),
        }
        concrete_evidence = len(rows) + len(fields) + len(numeric_statistics)
        return self.envelope(
            result=result,
            confidence=self.derive_confidence(request, concrete_evidence, 10),
            verification=verification,
        )
