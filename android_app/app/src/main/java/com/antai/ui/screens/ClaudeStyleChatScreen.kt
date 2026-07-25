package com.antai.ui.screens

import androidx.compose.foundation.layout.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp

@Composable
fun ClaudeStyleChatScreen() {
    var message by remember { mutableStateOf("") }
    val messages = remember { mutableStateListOf<Pair<String, Boolean>>() }

    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(20.dp)
    ) {
        Text(
            text = "ANT CLAW",
            style = MaterialTheme.typography.headlineMedium
        )

        Spacer(modifier = Modifier.height(20.dp))

        Column(
            modifier = Modifier.weight(1f)
        ) {
            messages.forEach { item ->
                Text(
                    text = if (item.second) "You: ${item.first}" else "ANT CLAW: ${item.first}",
                    modifier = Modifier.padding(vertical = 8.dp)
                )
            }
        }

        if (messages.isEmpty()) {
            Text(
                text = "How can I help you today?",
                style = MaterialTheme.typography.headlineSmall
            )

            Spacer(modifier = Modifier.height(8.dp))
            Text("Ask anything or give me a task.")
        }

        Spacer(modifier = Modifier.height(16.dp))

        OutlinedTextField(
            value = message,
            onValueChange = { message = it },
            modifier = Modifier.fillMaxWidth(),
            placeholder = {
                Text("Message ANT CLAW...")
            },
            trailingIcon = {
                Button(
                    onClick = {
                        if (message.isNotBlank()) {
                            messages.add(message to true)
                            messages.add(
                                "I received your task. I will help you complete it."
                                    to false
                            )
                            message = ""
                        }
                    }
                ) {
                    Text("➤")
                }
            }
        )
    }
}
