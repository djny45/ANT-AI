package com.antai.ui.screens

import androidx.compose.foundation.layout.*
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp

@Composable
fun ClaudeStyleChatScreen() {
    var message by remember { mutableStateOf("") }

    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(20.dp)
    ) {
        Text(
            text = "ANT CLAW",
            style = MaterialTheme.typography.headlineMedium
        )

        Spacer(modifier = Modifier.weight(1f))

        Text(
            text = "How can I help you today?",
            style = MaterialTheme.typography.headlineSmall
        )

        Spacer(modifier = Modifier.height(8.dp))

        Text("Ask anything or give me a task.")

        Spacer(modifier = Modifier.height(32.dp))

        OutlinedTextField(
            value = message,
            onValueChange = { message = it },
            modifier = Modifier.fillMaxWidth(),
            placeholder = {
                Text("Message ANT CLAW...")
            },
            trailingIcon = {
                Text("➤")
            }
        )
    }
}
