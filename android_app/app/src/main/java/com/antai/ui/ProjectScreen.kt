package com.antai.ui

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp

@Composable
fun ProjectScreen(modifier: Modifier = Modifier) {
    Column(
        modifier = modifier
            .fillMaxSize()
            .padding(16.dp),
        verticalArrangement = Arrangement.spacedBy(12.dp)
    ) {
        Text("Projects", color = MaterialTheme.colorScheme.onBackground, style = MaterialTheme.typography.headlineMedium)
        listOf("Android APK", "Automation workflows", "Knowledge imports").forEach { project ->
            Card(
                modifier = Modifier.fillMaxWidth(),
                colors = CardDefaults.cardColors(containerColor = Color(0xCC2A241C)),
                shape = RoundedCornerShape(22.dp)
            ) {
                Column(Modifier.padding(16.dp)) {
                    Text(project, color = MaterialTheme.colorScheme.primary, fontWeight = FontWeight.Bold)
                    Text("Tracked and ready for ANT execution", color = MaterialTheme.colorScheme.onSurfaceVariant)
                }
            }
        }
    }
}
