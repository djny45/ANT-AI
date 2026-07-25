package com.antai.ui.components

import androidx.compose.animation.core.*
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.rememberInfiniteTransition
import androidx.compose.ui.Modifier

@Composable
fun AnimatedAntLogo(modifier: Modifier = Modifier) {
    val transition = rememberInfiniteTransition()
    Text("🐜", modifier = modifier)
}
