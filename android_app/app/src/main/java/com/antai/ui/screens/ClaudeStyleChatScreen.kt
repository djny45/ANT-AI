package com.antai.ui.screens

import androidx.compose.foundation.layout.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import com.antai.ai.OllamaStreamService
import com.antai.ui.components.AntThinkingAnimation
import com.antai.ui.components.MarkdownRenderer
import kotlinx.coroutines.launch

private data class ChatItem(val text: String, val user: Boolean)

@Composable
fun ClaudeStyleChatScreen() {
    var message by remember { mutableStateOf("") }
    var typing by remember { mutableStateOf(false) }
    val messages = remember { mutableStateListOf<ChatItem>() }
    val scope = rememberCoroutineScope()
    val ollama = remember { OllamaStreamService() }

    Column(Modifier.fillMaxSize().padding(20.dp)) {
        Text("ANT CLAW", style = MaterialTheme.typography.headlineMedium)

        Column(Modifier.weight(1f)) {
            messages.forEach { item ->
                if (item.user) {
                    Text("You: ${item.text}")
                } else {
                    MarkdownRenderer(item.text)
                }
                Spacer(Modifier.height(8.dp))
            }
            if (typing) AntThinkingAnimation()
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
                            var index = messages.size
                            messages.add(ChatItem("", false))
                            ollama.chat(prompt).collect { token ->
                                messages[index] = ChatItem(messages[index].text + token, false)
                            }
                            typing = false
                        }
                    }
                }) { Text("➤") }
            }
        )
    }
}
