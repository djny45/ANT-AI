package com.antai.ui.screens

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.text.BasicTextField
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.focus.FocusRequester
import androidx.compose.ui.focus.focusRequester
import androidx.compose.ui.focus.onFocusChanged
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
    val focusRequester = remember { FocusRequester() }

    Column(Modifier.fillMaxSize().padding(20.dp)) {
        Text("ANT CLAW", style = MaterialTheme.typography.headlineMedium)

        Column(Modifier.weight(1f)) {
            messages.forEach { item ->
                if (item.user) Text("You: ${item.text}")
                else MarkdownRenderer(item.text)
                Spacer(Modifier.height(8.dp))
            }
            if (typing) AntThinkingAnimation()
        }

        Surface(
            modifier = Modifier
                .fillMaxWidth()
                .focusRequester(focusRequester)
        ) {
            Row(modifier = Modifier.fillMaxWidth()) {
                BasicTextField(
                    value = message,
                    onValueChange = { message = it },
                    modifier = Modifier
                        .weight(1f)
                        .padding(16.dp)
                        .onFocusChanged { },
                    decorationBox = { inner ->
                        if (message.isEmpty()) {
                            Text("Message ANT CLAW...")
                        }
                        inner()
                    }
                )

                Button(onClick = {
                    if (message.isNotBlank()) {
                        val prompt = message
                        messages.add(ChatItem(prompt, true))
                        message = ""
                        scope.launch {
                            typing = true
                            val index = messages.size
                            messages.add(ChatItem("", false))
                            ollama.chat(prompt).collect { token ->
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
}
