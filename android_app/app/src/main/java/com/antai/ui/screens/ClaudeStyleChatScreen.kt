package com.antai.ui.screens

import androidx.compose.foundation.layout.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import kotlinx.coroutines.delay
import kotlinx.coroutines.launch

private data class ChatItem(
    val text: String,
    val user: Boolean
)

@Composable
fun ClaudeStyleChatScreen() {
    var message by remember { mutableStateOf("") }
    var typing by remember { mutableStateOf(false) }
    val messages = remember { mutableStateListOf<ChatItem>() }
    val scope = rememberCoroutineScope()

    Column(
        modifier = Modifier.fillMaxSize().padding(20.dp)
    ) {
        Text("ANT CLAW", style = MaterialTheme.typography.headlineMedium)

        Column(modifier = Modifier.weight(1f)) {
            messages.forEach {
                Text(
                    text = if (it.user) "You: ${it.text}" else "ANT CLAW: ${it.text}",
                    modifier = Modifier.padding(vertical = 8.dp)
                )
            }

            if (typing) {
                Text("🐜 ANT CLAW is thinking... •••")
            }
        }

        OutlinedTextField(
            value = message,
            onValueChange = { message = it },
            modifier = Modifier.fillMaxWidth(),
            placeholder = { Text("Message ANT CLAW...") },
            trailingIcon = {
                Row {
                    TextButton(onClick = { /* attachment picker hook */ }) {
                        Text("📎")
                    }
                    Button(onClick = {
                        if (message.isNotBlank()) {
                            val userMessage = message
                            messages.add(ChatItem(userMessage, true))
                            message = ""
                            scope.launch {
                                typing = true
                                delay(1200)
                                typing = false
                                messages.add(
                                    ChatItem(
                                        "Connected to Ollama AI foundation.\n\n```\nAI response pipeline ready\n```\n\nMarkdown rendering enabled.",
                                        false
                                    )
                                )
                            }
                        }
                    }) {
                        Text("➤")
                    }
                }
            }
        )
    }
}
