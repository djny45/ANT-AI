package com.antai.ui.screens

import androidx.compose.foundation.layout.*
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp

@Composable
fun HomeScreen(
    darkMode: Boolean = true
) {
    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(24.dp)
    ) {
        Text(
            text = "Ant AI",
            style = MaterialTheme.typography.headlineLarge
        )

        Spacer(modifier = Modifier.height(16.dp))

        Text("How can I help you today?")

        Spacer(modifier = Modifier.height(24.dp))

        OutlinedTextField(
            value = "",
            onValueChange = {},
            placeholder = {
                Text("Ask anything or give a task...")
            },
            modifier = Modifier.fillMaxWidth()
        )

        Spacer(modifier = Modifier.height(20.dp))

        Text("Quick Actions")
        Text("🧠 Research")
        Text("💻 Code")
        Text("🔍 Analyze")
        Text("🏗 Build")

        Spacer(modifier = Modifier.height(20.dp))

        Text("Agents")
        Text("Coding Agent")
        Text("Research Agent")
        Text("Security Agent")
    }
}
