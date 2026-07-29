package com.antclaw.core

interface Agent {
    val name: String
    fun execute(input: String): String
}

class CodeAgent : Agent {
    override val name = "Code Agent"
    override fun execute(input: String) = "Analyzing code request"
}

class ResearchAgent : Agent {
    override val name = "Research Agent"
    override fun execute(input: String) = "Analyzing research request"
}
