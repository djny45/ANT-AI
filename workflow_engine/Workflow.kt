package com.antai.workflow

data class Workflow(
    val id: String,
    val name: String,
    val description: String,
    val source: String = "n8n"
)
