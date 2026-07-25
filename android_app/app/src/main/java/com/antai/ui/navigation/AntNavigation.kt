package com.antai.ui.navigation

import androidx.compose.material3.Text
import androidx.compose.runtime.Composable

sealed class AntScreen(val title: String) {
    data object Home : AntScreen("Home")
    data object Projects : AntScreen("Projects")
    data object Agents : AntScreen("Agents")
    data object Tools : AntScreen("Tools")
    data object Memory : AntScreen("Memory")
    data object Settings : AntScreen("Settings")
}

@Composable
fun AntNavigationPlaceholder() {
    Text("ANT AI Navigation")
}
