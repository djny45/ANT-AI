package com.antai.ui.screens

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
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
    // Input state - persists across recompositions
    var message by rememberSaveable { mutableStateOf("") }
    
    // UI state - persists across lifecycle events
    var typing by rememberSaveable { mutableStateOf(false) }
    var error by rememberSaveable { mutableStateOf("") }
    var isSending by rememberSaveable { mutableStateOf(false) }
    
    // Message history - persists via serialization
    val messages = rememberSaveable(saver = ChatItemListSaver) { 
        mutableStateListOf<ChatItem>() 
    }
    
    // Scroll state for UI
    val listState = rememberLazyListState()
    val scope = rememberCoroutineScope()
    
    // Auto-scroll to bottom when new message arrives
    LaunchedEffect(messages.size) {
        if (messages.isNotEmpty()) {
            listState.animateScrollToItem(messages.size - 1)
        }
    }

    Column(Modifier.fillMaxSize().padding(20.dp)) {
        Text("ANT CLAW", style = MaterialTheme.typography.headlineMedium)

        // Message history with proper scrolling
        LazyColumn(
            modifier = Modifier
                .weight(1f)
                .fillMaxWidth(),
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
            
            // Show thinking animation only if actively typing
            if (typing) {
                item {
                    AntThinkingAnimation()
                }
            }
        }
        
        // Error display
        if (error.isNotEmpty()) {
            Text(
                text = "Error: $error",
                color = MaterialTheme.colorScheme.error,
                modifier = Modifier.padding(8.dp)
            )
        }

        // Input row with improved stability
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
                                
                                // Add user message
                                messages.add(ChatItem(prompt, user = true))
                                message = "" // Clear input
                                
                                // Add placeholder for assistant response
                                val responseId = System.nanoTime().toString()
                                messages.add(ChatItem("", user = false, id = responseId))
                                val responseIndex = messages.lastIndex
                                
                                typing = true
                                var fullResponse = ""
                                
                                try {
                                    // Stream response with proper error handling
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
                                isSending = false
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

// Saver for persisting ChatItem list across process death
private val ChatItemListSaver = listSaver<MutableList<ChatItem>, List<Any>>(
    save = { list ->
        list.map { 
            listOf(it.text, it.user, it.id) as List<Any>
        }
    },
    restore = { savedList ->
        mutableStateListOf<ChatItem>().apply {
            addAll(
                savedList.map { item ->
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
