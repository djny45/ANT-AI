package com.antai.ui.screens

import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.Card
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp

@Composable
fun WorkflowLibraryScreen() {
    Column(
        modifier = Modifier.padding(24.dp)
    ) {
        Text(
            text = "Workflow Lab",
            style = MaterialTheme.typography.headlineMedium
        )

        Spacer(modifier = Modifier.height(16.dp))

        WorkflowCard("AI Research Workflow")
        WorkflowCard("Automation Agent")
        WorkflowCard("Developer Assistant")
        WorkflowCard("Data Analysis Flow")
    }
}

@Composable
private fun WorkflowCard(name: String) {
    Card {
        Text(
            text = name,
            modifier = Modifier.padding(16.dp)
        )
    }
}
