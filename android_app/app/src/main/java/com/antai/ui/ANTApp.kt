package com.antai.ui

import androidx.compose.material3.Scaffold
import androidx.compose.runtime.Composable
import com.antai.ai.RouterChatService
import com.antai.ui.components.AntBottomNavigation
import com.antai.ui.screens.ClaudeStyleChatScreen
import com.antai.ui.theme.AntTheme

@Composable
fun ANTApp(routerChatService: RouterChatService) {
    AntTheme(darkTheme = true) {
        Scaffold(
            bottomBar = {
                AntBottomNavigation()
            }
        ) {
            ClaudeStyleChatScreen(routerChatService = routerChatService)
        }
    }
}
