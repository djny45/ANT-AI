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
            text = "ANT CLAW",
            style = MaterialTheme.typography.headlineLarge
        )

        Spacer(modifier = Modifier.weight(1f))

        Text(
            text = "How can I help you today?",
            style = MaterialTheme.typography.headlineSmall
        )

        Spacer(modifier = Modifier.height(8.dp))

        Text("Ask anything or give me a task.")

        Spacer(modifier = Modifier.height(24.dp))

        OutlinedTextField(
            value = "",
            onValueChange = {},
            placeholder = {
                Text("Message ANT CLAW...")
            },
            modifier = Modifier.fillMaxWidth()
        )
    }
}
