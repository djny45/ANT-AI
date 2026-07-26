package com.antai.ui

import androidx.compose.material3.ColorScheme
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.lightColorScheme
import androidx.compose.runtime.Composable
import androidx.compose.ui.graphics.Color

private val AntColorScheme: ColorScheme = lightColorScheme(
    primary = Color(0xFFF26A21),
    onPrimary = Color(0xFFFFFFFF),
    secondary = Color(0xFF7A4A2F),
    onSecondary = Color(0xFFFFFFFF),
    tertiary = Color(0xFF2F6B4F),
    background = Color(0xFFFFFAF4),
    onBackground = Color(0xFF201A17),
    surface = Color(0xFFFFFFFF),
    onSurface = Color(0xFF201A17),
    surfaceVariant = Color(0xFFF7EFE7),
    onSurfaceVariant = Color(0xFF6F6259)
)

@Composable
fun ANTTheme(content: @Composable () -> Unit) {
    MaterialTheme(
        colorScheme = AntColorScheme,
        content = content
    )
}
