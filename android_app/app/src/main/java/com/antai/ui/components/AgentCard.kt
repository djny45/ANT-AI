package com.antai.ui.components

import androidx.compose.material3.Card
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable

@Composable
fun AgentCard(
    name: String,
    status: String = "Online"
) {
    Card {
        Text("$name\n$status")
    }
}
