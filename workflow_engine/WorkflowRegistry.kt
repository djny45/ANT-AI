package com.antai.workflow

class WorkflowRegistry {
    private val workflows = mutableMapOf<String, Workflow>()

    fun register(workflow: Workflow) {
        workflows[workflow.id] = workflow
    }

    fun list(): List<Workflow> {
        return workflows.values.toList()
    }

    fun find(id: String): Workflow? {
        return workflows[id]
    }
}
