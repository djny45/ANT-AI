package com.antai.ui

import androidx.compose.material3.ColorScheme
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.darkColorScheme
import androidx.compose.runtime.Composable
import androidx.compose.ui.graphics.Color

private val AntColorScheme: ColorScheme = darkColorScheme(
    primary = Color(0xFFE0B980),
    onPrimary = Color(0xFF24180B),
    secondary = Color(0xFF7BAE7F),
    onSecondary = Color(0xFF07170A),
    tertiary = Color(0xFFB7C4D8),
    background = Color(0xFF181511),
    onBackground = Color(0xFFF8EFE0),
    surface = Color(0xFF211D18),
    onSurface = Color(0xFFF8EFE0),
    surfaceVariant = Color(0xFF312B24),
    onSurfaceVariant = Color(0xFFE2D6C6)
)

@Composable
fun ANTTheme(content: @Composable () -> Unit) {
    MaterialTheme(
        colorScheme = AntColorScheme,
        content = content
    )
}
