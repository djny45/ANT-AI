package com.antclaw.core

class SafetyLayer {
    fun validate(input: String): Boolean {
        return input.isNotBlank()
    }
}
