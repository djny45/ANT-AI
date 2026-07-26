package com.antai.ai

data class AIRequest(
    val message: String,
    val model: String = "auto"
)
