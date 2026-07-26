package com.antai.ui.screens

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.lazy.rememberLazyListState
import androidx.compose.foundation.text.BasicTextField
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.runtime.saveable.listSaver
import androidx.compose.runtime.saveable.rememberSaveable
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import com.antai.ai.RouterChatService
import com.antai.ui.components.AntThinkingAnimation
import com.antai.ui.components.MarkdownRenderer
import kotlinx.coroutines.launch

private data class ChatItem(val text: String, val user: Boolean, val id: String = System.nanoTime().toString())

@Composable
fun ClaudeStyleChatScreen(routerChatService: RouterChatService) {
    var message by rememberSaveable { mutableStateOf("") }
    var typing by rememberSaveable { mutableStateOf(false) }
    var error by rememberSaveable { mutableStateOf("") }
    var isSending by rememberSaveable { mutableStateOf(false) }

    val messages = rememberSaveable(saver = ChatItemListSaver) {
        mutableStateListOf<ChatItem>()
    }

    val listState = rememberLazyListState()
    val scope = rememberCoroutineScope()

    LaunchedEffect(messages.size) {
        if (messages.isNotEmpty()) {
            listState.animateScrollToItem(messages.size - 1)
        }
    }

    Column(Modifier.fillMaxSize().padding(20.dp)) {
        Text("ANT CLAW", style = MaterialTheme.typography.headlineMedium)

        LazyColumn(
            modifier = Modifier.weight(1f).fillMaxWidth(),
            state = listState
        ) {
            items(messages.size) { index ->
                val item = messages[index]
                if (item.user) {
                    Text("You: ${item.text}", modifier = Modifier.padding(8.dp))
                } else if (item.text.isNotEmpty()) {
                    MarkdownRenderer(item.text)
                }
            }

            if (typing) {
                item { AntThinkingAnimation() }
            }
        }

        if (error.isNotEmpty()) {
            Text(
                text = "Error: $error",
                color = MaterialTheme.colorScheme.error,
                modifier = Modifier.padding(8.dp)
            )
        }

        Row(Modifier.fillMaxWidth()) {
            BasicTextField(
                value = message,
                onValueChange = { message = it },
                modifier = Modifier.weight(1f).padding(16.dp),
                enabled = !isSending && error.isEmpty()
            )

            Button(
                onClick = {
                    val prompt = message.trim()
                    if (prompt.isNotBlank() && !isSending) {
                        scope.launch {
                            try {
                                isSending = true
                                error = ""
                                messages.add(ChatItem(prompt, user = true))
                                message = ""

                                val responseId = System.nanoTime().toString()
                                messages.add(ChatItem("", user = false, id = responseId))
                                val responseIndex = messages.lastIndex

                                typing = true
                                var fullResponse = ""

                                try {
                                    routerChatService.send(prompt).collect { token ->
                                        fullResponse += token
                                        if (responseIndex < messages.size) {
                                            messages[responseIndex] = ChatItem(
                                                fullResponse,
                                                user = false,
                                                id = responseId
                                            )
                                        }
                                    }
                                } finally {
                                    typing = false
                                }
                            } catch (e: Exception) {
                                error = e.message ?: "Unknown error occurred"
                                typing = false
                            } finally {
                                isSending = false
                            }
                        }
                    }
                },
                enabled = !isSending && message.isNotBlank()
            ) {
                Text(if (isSending) "⟳" else "➤")
            }
        }
    }
}

private val ChatItemListSaver = listSaver<MutableList<ChatItem>, List<Any>>(
    save = { list ->
        list.map { item ->
            listOf(item.text, item.user, item.id)
        }
    },
    restore = { savedList ->
        mutableStateListOf<ChatItem>().apply {
            addAll(
                savedList.map { item: List<Any> ->
                    ChatItem(
                        text = item[0] as String,
                        user = item[1] as Boolean,
                        id = item[2] as String
                    )
                }
            )
        }
    }
)