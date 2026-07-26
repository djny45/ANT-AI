package com.antai.ui

import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp

private enum class MainTab(val title: String) {
    Home("Home"), Projects("Projects"), Agents("Agents"), Tools("Tools"), Settings("Settings")
}

@Composable
fun ANTApp() {
    ANTTheme {
        var selectedTab by remember { mutableStateOf(MainTab.Home) }
        Surface(modifier = Modifier.fillMaxSize(), color = MaterialTheme.colorScheme.background) {
            Column(
                modifier = Modifier
                    .fillMaxSize()
                    .background(
                        Brush.verticalGradient(
                            listOf(Color(0xFFFFFBF6), Color(0xFFFFF4EA), Color(0xFFF7ECE1))
                        )
                    )
            ) {
                AppHeader()
                Box(
                    modifier = Modifier
                        .weight(1f)
                        .fillMaxWidth()
                ) {
                    when (selectedTab) {
                        MainTab.Home -> ChatScreen(Modifier.fillMaxSize())
                        MainTab.Agents -> AgentScreen(Modifier.fillMaxSize())
                        MainTab.Projects -> ProjectScreen(Modifier.fillMaxSize())
                        MainTab.Tools -> BuildScreen(Modifier.fillMaxSize())
                        MainTab.Settings -> SettingsPanel(Modifier.fillMaxSize())
                    }
                }
                BottomTabs(selectedTab = selectedTab, onSelected = { selectedTab = it })
            }
        }
    }
}

@Composable
private fun AppHeader() {
    Row(
        modifier = Modifier
            .fillMaxWidth()
            .padding(horizontal = 20.dp, vertical = 18.dp),
        verticalAlignment = Alignment.CenterVertically,
        horizontalArrangement = Arrangement.SpaceBetween
    ) {
        Column {
            Text(
                text = "ANT AI",
                color = MaterialTheme.colorScheme.onBackground,
                style = MaterialTheme.typography.headlineSmall,
                fontWeight = FontWeight.Bold,
                fontFamily = FontFamily.Serif
            )
            Text(
                text = "Autonomous neural taskforce",
                color = Color(0xFF7D6A5E),
                style = MaterialTheme.typography.bodySmall
            )
        }
        Box(
            modifier = Modifier
                .clip(RoundedCornerShape(100.dp))
                .background(MaterialTheme.colorScheme.primary)
                .size(40.dp),
            contentAlignment = Alignment.Center
        ) {
            Text("ANT", color = MaterialTheme.colorScheme.onPrimary, style = MaterialTheme.typography.labelSmall)
        }
    }
}

@Composable
private fun BottomTabs(selectedTab: MainTab, onSelected: (MainTab) -> Unit) {
    Row(
        modifier = Modifier
            .fillMaxWidth()
            .padding(12.dp)
            .clip(RoundedCornerShape(24.dp))
                .background(Color(0xEEFFFFFF))
            .padding(6.dp),
        horizontalArrangement = Arrangement.spacedBy(4.dp)
    ) {
        MainTab.entries.forEach { tab ->
            val active = tab == selectedTab
            Box(
                modifier = Modifier
                    .weight(1f)
                    .clip(RoundedCornerShape(18.dp))
                    .background(if (active) Color(0xFFFFE7D7) else Color.Transparent)
                    .clickable { onSelected(tab) }
                    .padding(vertical = 10.dp),
                contentAlignment = Alignment.Center
            ) {
                Text(
                    text = tab.title,
                    color = if (active) MaterialTheme.colorScheme.primary else Color(0xFF7D6A5E),
                    style = MaterialTheme.typography.labelSmall,
                    fontWeight = if (active) FontWeight.Bold else FontWeight.Normal
                )
            }
        }
    }
}

@Composable
private fun SettingsPanel(modifier: Modifier = Modifier) {
    Column(
        modifier = modifier.padding(20.dp),
        verticalArrangement = Arrangement.spacedBy(12.dp)
    ) {
        Text("Settings", color = MaterialTheme.colorScheme.onBackground, style = MaterialTheme.typography.headlineMedium, fontWeight = FontWeight.Bold)
        listOf("Theme: Light", "Model: ANT Router", "Download: https://github.com/djny45/ANT-AI/releases/", "Status: Offline ready").forEach { item ->
            Box(
                modifier = Modifier
                    .fillMaxWidth()
                    .clip(RoundedCornerShape(20.dp))
                    .background(Color.White)
                    .padding(18.dp)
            ) {
                Text(item, color = MaterialTheme.colorScheme.onSurface)
            }
        }
    }
}
