from ANT_X_OS.core.memory import Memory


def test_memory_routes_temporary_and_permanent_items():
    memory = Memory()
    temporary = {"value": "temporary"}
    permanent = {"value": "permanent"}

    memory.store(temporary)
    memory.store(permanent, permanent=True)

    assert memory.short_term == [temporary]
    assert memory.long_term == [permanent]


def test_memory_retrieve_concatenates_short_term_before_long_term():
    memory = Memory()
    memory.store("short")
    memory.store("long", permanent=True)

    assert memory.retrieve() == ["short", "long"]


def test_workflows_are_recorded_and_permanent_copy_is_retrievable():
    memory = Memory()
    temporary = {"id": "temporary"}
    permanent = {"id": "permanent"}

    memory.store_workflow(temporary)
    memory.store_workflow(permanent, permanent=True)

    assert memory.retrieve_workflows() == [temporary, permanent]
    assert memory.long_term == [{"workflow": permanent}]

    workflows = memory.retrieve_workflows()
    workflows.clear()
    assert memory.retrieve_workflows() == [temporary, permanent]
