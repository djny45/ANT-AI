package com.antai.ui.screens

import androidx.compose.foundation.layout.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import com.antai.ai.OllamaStreamService
import com.antai.ui.components.AntThinkingAnimation
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
    val ollama = remember { OllamaStreamService() }

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
                AntThinkingAnimation()
            }
        }

        OutlinedTextField(
            value = message,
            onValueChange = { message = it },
            modifier = Modifier.fillMaxWidth(),
            placeholder = { Text("Message ANT CLAW...") },
            trailingIcon = {
                Button(onClick = {
                    if (message.isNotBlank()) {
                        val prompt = message
                        messages.add(ChatItem(prompt, true))
                        message = ""

                        scope.launch {
                            typing = true
                            var response = ""
                            ollama.chat(prompt).collect { token ->
                                response += token
                            }
                            typing = false
                            messages.add(ChatItem(response, false))
                        }
                    }
                }) {
                    Text("➤")
                }
            }
        )
    }
}
