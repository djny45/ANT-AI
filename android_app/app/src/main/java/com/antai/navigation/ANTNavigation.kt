package com.antai.navigation

sealed class ANTScreen(val route: String) {
    data object Home : ANTScreen("home")
    data object Chat : ANTScreen("chat")
    data object Agents : ANTScreen("agents")
    data object Projects : ANTScreen("projects")
    data object Build : ANTScreen("build")
}
