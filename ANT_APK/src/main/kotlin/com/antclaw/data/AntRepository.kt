package com.antclaw.data

class AntRepository(
    private val api: AntApiService
) {
    fun send(message: String): String {
        return api.sendMessage(message)
    }
}
