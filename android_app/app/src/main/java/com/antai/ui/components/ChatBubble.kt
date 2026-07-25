package com.antai.ui.components

import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable

@Composable
fun ChatBubble(
    message: String,
    user: Boolean
) {
    Surface {
        Text(
            text = if (user) "You: $message" else "ANT AI: $message"
        )
    }
}
