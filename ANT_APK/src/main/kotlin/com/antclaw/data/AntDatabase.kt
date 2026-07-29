package com.antclaw.data

class AntDatabase {
    private val messages = mutableListOf<String>()

    fun save(message: String) {
        messages.add(message)
    }

    fun getAll(): List<String> = messages
}
