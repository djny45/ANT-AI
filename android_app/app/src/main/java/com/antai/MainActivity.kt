package com.antai

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import com.antai.ui.screens.HomeScreen
import com.antai.ui.theme.AntTheme

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            AntTheme(darkTheme = true) {
                HomeScreen()
            }
        }
    }
}
