package com.antclaw.core

class PerformanceManager {
    private val cache = mutableMapOf<String, String>()

    fun cache(key: String, value: String) {
        cache[key] = value
    }

    fun get(key: String): String? = cache[key]
}
