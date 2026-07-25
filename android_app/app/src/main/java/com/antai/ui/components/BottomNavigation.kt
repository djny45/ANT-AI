package com.antai.ui.components

import androidx.compose.material3.NavigationBar
import androidx.compose.material3.NavigationBarItem
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable

@Composable
fun AntBottomNavigation() {
    NavigationBar {
        listOf("Home", "Projects", "Agents", "Tools", "Memory").forEach { item ->
            NavigationBarItem(
                selected = item == "Home",
                onClick = {},
                icon = { Text("•") },
                label = { Text(item) }
            )
        }
    }
}
