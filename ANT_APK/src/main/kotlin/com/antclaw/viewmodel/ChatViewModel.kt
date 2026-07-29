package com.antclaw.viewmodel

class ChatViewModel {
    private val _messages = mutableListOf<String>()

    val messages: List<String>
        get() = _messages

    fun send(message: String) {
        _messages.add(message)
    }
}
