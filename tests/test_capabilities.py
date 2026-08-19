import asyncio

from ant_langgraph.executor import WorkflowExecutor
from ant_langgraph.graph import build_default_graph
from ant_langgraph.integration_pipeline import run_pipeline
from ANT_X_OS.skills.loader import load_builtin_skills
from ANT_X_OS.skills.registry import registry
from capabilities import (
    CodingCapability,
    DataAnalysisCapability,
    ResearchCapability,
    SecurityCapability,
)


def setup_module():
    registry.clear()
    load_builtin_skills()


def test_coding_capability_reports_syntax_and_inventory_evidence():
    invalid = CodingCapability().run(
        task={"objective": "inspect Python source"},
        context={"source": "def broken(:\n    pass\n"},
    )
    valid = CodingCapability().run(
        task={"objective": "inspect Python source"},
        context={"source": "def useful():\n    return 1\n"},
    )

    assert invalid["result"]["syntax_valid"] is False
    assert invalid["result"]["syntax_errors"][0]["line"] == 1
    assert valid["result"]["functions"][0]["name"] == "useful"
    assert valid["result"]["missing_docstrings"][0]["name"] == "useful"
    assert valid["confidence"] > CodingCapability().run(
        task={"objective": "inspect Python source"},
        context={},
    )["confidence"]


def test_security_capability_reports_risky_line_numbers():
    result = SecurityCapability().run(
        task={"objective": "scan this source"},
        context={"source": "value = 1\nresult = eval(value)\n"},
    )

    findings = result["result"]["findings"]
    assert any(
        finding["pattern"] == "eval_or_exec" and finding["line"] == 2
        for finding in findings
    )
    assert result["verification"]["lines_scanned"] == 2


def test_data_capability_computes_numeric_and_missing_value_statistics():
    result = DataAnalysisCapability().run(
        task={"objective": "analyze this dataset"},
        context={
            "dataset": [
                {"age": 10, "name": "Ada"},
                {"age": 20, "name": None},
                {"age": 30},
            ],
        },
    )

    analysis = result["result"]
    assert analysis["row_count"] == 3
    assert analysis["field_count"] == 2
    assert analysis["missing_values"]["name"] == 2
    assert analysis["numeric_statistics"]["age"] == {
        "min": 10,
        "max": 30,
        "mean": 20,
        "median": 20,
    }


def test_research_capability_attributes_memory_items():
    result = ResearchCapability().run(
        task={"objective": "compare the prior findings and open questions"},
        context={
            "memory_context": {
                "short_term": [
                    {"input": "prior finding", "verification": {"status": "verified"}},
                ],
            },
        },
    )

    assert result["result"]["findings"] == [{
        "source": "memory",
        "item": {
            "input": "prior finding",
            "verification": {"status": "verified"},
        },
    }]
    assert result["result"]["request_evidence"]["source"] == "request"
    assert result["verification"]["external_sources_used"] == 0


def test_default_graph_registers_real_handlers_without_clobbering_injected_handler():
    custom = lambda **kwargs: {"success": True}
    executor = WorkflowExecutor({"coding": custom})

    build_default_graph(workflow_executor=executor)

    assert executor.handlers["coding"] is custom
    assert executor.handlers["research"].handler_name == "research_capability"
    assert executor.handlers["security"].handler_name == "security_capability"
    assert executor.handlers["data"].handler_name == "data_analysis_capability"


def test_pipeline_exposes_real_handler_result_in_trace_and_audit():
    result = asyncio.run(
        run_pipeline({
            "user_input": "Analyze this Python project and suggest improvements",
            "conversation_id": "capability-evidence",
            "context": {
                "source": "def useful():\n    return 1\n",
            },
        })
    )

    execution_results = result["execution"]["results"]
    coding_record = next(
        item
        for item in execution_results
        if item["agent"] == "coding"
    )
    assert coding_record["execution_path"] == "capability_handler"
    assert coding_record["capability"] == "Coding Skill"
    assert coding_record["handler"] == "coding_capability"
    assert coding_record["confidence"] > 0
    assert coding_record["verification"]["source_inspected"] is True
    assert "execution_result" not in coding_record
    assert coding_record["result"]["functions"][0]["name"] == "useful"

    check = next(
        item
        for item in result["verification"]["result"]["checks"]
        if item["agent"] == "coding"
    )
    assert check["handler_verification"]["source_inspected"] is True
    audit_result = next(
        item
        for item in result["audit"]["metadata"]["audit_record"]["result"]
        if item["agent"] == "coding"
    )
    assert audit_result["execution_path"] == "capability_handler"
    assert audit_result["verification"]["source_inspected"] is True
    assert audit_result["result"]["functions"][0]["name"] == "useful"
    assert result["audit"]["metadata"]["audit_record"]["verification_status"] in {
        "verified",
        "failed",
    }
    assert "Coding Skill" in result["response"]["final_response"]
