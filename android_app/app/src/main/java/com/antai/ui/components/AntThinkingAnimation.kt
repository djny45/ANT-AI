package com.antai.ui.components

import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import kotlinx.coroutines.delay

@Composable
fun AntThinkingAnimation() {
    val dots = remember { mutableStateOf(".") }

    LaunchedEffect(Unit) {
        while (true) {
            dots.value = when (dots.value) {
                "." -> ".."
                ".." -> "..."
                else -> "."
            }
            delay(400)
        }
    }

    Text("🐜 ANT CLAW thinking${dots.value}")
}
