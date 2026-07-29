package com.antclaw.core

class MemoryEngine {
    private val memory = mutableListOf<String>()

    fun remember(value: String) {
        memory.add(value)
    }

    fun recall(): List<String> = memory.toList()
}
