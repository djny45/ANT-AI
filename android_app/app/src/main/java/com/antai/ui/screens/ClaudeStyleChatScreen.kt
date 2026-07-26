package com.antai.ui.screens

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.text.BasicTextField
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.runtime.saveable.rememberSaveable
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import com.antai.ai.RouterChatService
import com.antai.ui.components.AntThinkingAnimation
import com.antai.ui.components.MarkdownRenderer
import kotlinx.coroutines.launch

private data class ChatItem(val text: String, val user: Boolean)

@Composable
fun ClaudeStyleChatScreen(routerChatService: RouterChatService) {
    var message by rememberSaveable { mutableStateOf("") }
    var typing by rememberSaveable { mutableStateOf(false) }
    val messages = remember { mutableStateListOf<ChatItem>() }
    val scope = rememberCoroutineScope()

    Column(Modifier.fillMaxSize().padding(20.dp)) {
        Text("ANT CLAW", style = MaterialTheme.typography.headlineMedium)

        Column(Modifier.weight(1f)) {
            messages.forEach { item ->
                if (item.user) Text("You: ${item.text}")
                else MarkdownRenderer(item.text)
            }
            if (typing) AntThinkingAnimation()
        }

        Row(Modifier.fillMaxWidth()) {
            BasicTextField(
                value = message,
                onValueChange = { message = it },
                modifier = Modifier.weight(1f).padding(16.dp)
            )

            Button(onClick = {
                val prompt = message
                if (prompt.isNotBlank()) {
                    messages.add(ChatItem(prompt, true))
                    message = ""
                    scope.launch {
                        typing = true
                        messages.add(ChatItem("", false))
                        val index = messages.lastIndex
                        routerChatService.send(prompt).collect { token ->
                            messages[index] = ChatItem(messages[index].text + token, false)
                        }
                        typing = false
                    }
                }
            }) {
                Text("➤")
            }
        }
    }
}
