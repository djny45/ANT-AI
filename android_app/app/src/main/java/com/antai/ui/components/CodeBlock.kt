package com.antai.ui.components

import androidx.compose.material3.Card
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp

@Composable
fun CodeBlock(code: String) {
    Card(modifier = Modifier) {
        Text(code)
    }
}
