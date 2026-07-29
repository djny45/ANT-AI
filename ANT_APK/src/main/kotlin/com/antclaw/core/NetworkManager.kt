package com.antclaw.core

class NetworkManager {
    fun compress(payload: String): String {
        return payload.trim()
    }

    fun isAvailable(): Boolean = true
}
