package com.antai.ui.components

import android.content.Context
import androidx.compose.foundation.layout.Column
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.runtime.Composable

@Composable
fun CodeBlock(code: String, context: Context) {
    Column {
        Text(code)
        TextButton(onClick = { copyToClipboard(context, code) }) {
            Text("Copy")
        }
    }
}
