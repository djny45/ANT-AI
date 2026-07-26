package com.antai.ui

import androidx.compose.animation.core.FastOutSlowInEasing
import androidx.compose.animation.core.RepeatMode
import androidx.compose.animation.core.animateFloat
import androidx.compose.animation.core.infiniteRepeatable
import androidx.compose.animation.core.rememberInfiniteTransition
import androidx.compose.animation.core.tween
import androidx.compose.foundation.Canvas
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.Button
import androidx.compose.material3.ButtonDefaults
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateListOf
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.StrokeCap
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import kotlinx.coroutines.delay

private data class ChatMessage(val author: String, val text: String, val fromUser: Boolean)

@Composable
fun ChatScreen(modifier: Modifier = Modifier) {
    val messages = remember {
        mutableStateListOf(
            ChatMessage(
                author = "ANT",
                text = "I am ready. Describe a build, research, or automation task and I will route it through the swarm.",
                fromUser = false
            )
        )
    }
    var input by remember { mutableStateOf("") }
    var isThinking by remember { mutableStateOf(false) }

    LaunchedEffect(isThinking, messages.size) {
        if (isThinking) {
            delay(1200)
            val lastTask = messages.lastOrNull { it.fromUser }?.text.orEmpty()
            messages += ChatMessage(
                author = "ANT",
                text = "Queued and analyzed: $lastTask\n\nSwarm plan: research, code review, security check, and APK build verification.",
                fromUser = false
            )
            isThinking = false
        }
    }

    Column(
        modifier = modifier
            .fillMaxSize()
            .padding(horizontal = 16.dp),
        verticalArrangement = Arrangement.SpaceBetween
    ) {
        LazyColumn(
            modifier = Modifier
                .weight(1f)
                .fillMaxWidth(),
            verticalArrangement = Arrangement.spacedBy(12.dp)
        ) {
            item { ChatHero() }
            items(messages) { message -> MessageBubble(message) }
            if (isThinking) {
                item { ThinkingBubble() }
            }
        }
        ChatInput(
            value = input,
            enabled = !isThinking,
            onValueChange = { input = it },
            onSend = {
                val task = input.trim()
                if (task.isNotEmpty()) {
                    messages += ChatMessage("You", task, true)
                    input = ""
                    isThinking = true
                }
            }
        )
    }
}

@Composable
private fun ChatHero() {
    Card(
        modifier = Modifier
            .fillMaxWidth()
            .padding(top = 4.dp),
        colors = CardDefaults.cardColors(containerColor = Color(0xCC2A241C)),
        shape = RoundedCornerShape(28.dp)
    ) {
        Column(Modifier.padding(20.dp)) {
            Text(
                text = "Good evening, commander.",
                color = MaterialTheme.colorScheme.onSurface,
                style = MaterialTheme.typography.headlineMedium,
                fontFamily = FontFamily.Serif,
                fontWeight = FontWeight.Bold
            )
            Spacer(Modifier.height(8.dp))
            Text(
                text = "A calm Claude-like workspace for focused requests, with ANT swarm feedback while you wait.",
                color = MaterialTheme.colorScheme.onSurfaceVariant,
                style = MaterialTheme.typography.bodyMedium
            )
        }
    }
}

@Composable
private fun MessageBubble(message: ChatMessage) {
    Row(
        modifier = Modifier.fillMaxWidth(),
        horizontalArrangement = if (message.fromUser) Arrangement.End else Arrangement.Start
    ) {
        Card(
            modifier = Modifier.fillMaxWidth(if (message.fromUser) 0.86f else 0.92f),
            colors = CardDefaults.cardColors(
                containerColor = if (message.fromUser) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.surfaceVariant
            ),
            shape = RoundedCornerShape(24.dp)
        ) {
            Column(Modifier.padding(16.dp)) {
                Text(
                    text = message.author,
                    color = if (message.fromUser) MaterialTheme.colorScheme.onPrimary else MaterialTheme.colorScheme.primary,
                    style = MaterialTheme.typography.labelMedium,
                    fontWeight = FontWeight.Bold
                )
                Spacer(Modifier.height(6.dp))
                Text(
                    text = message.text,
                    color = if (message.fromUser) MaterialTheme.colorScheme.onPrimary else MaterialTheme.colorScheme.onSurfaceVariant,
                    style = MaterialTheme.typography.bodyMedium
                )
            }
        }
    }
}

@Composable
private fun ThinkingBubble() {
    Card(
        modifier = Modifier.fillMaxWidth(0.78f),
        colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surfaceVariant),
        shape = RoundedCornerShape(24.dp)
    ) {
        Row(
            modifier = Modifier.padding(16.dp),
            verticalAlignment = Alignment.CenterVertically,
            horizontalArrangement = Arrangement.spacedBy(12.dp)
        ) {
            AnimatedAnt()
            Column {
                Text("ANT is thinking", color = MaterialTheme.colorScheme.primary, fontWeight = FontWeight.Bold)
                Text("Routing task through the swarm", color = MaterialTheme.colorScheme.onSurfaceVariant)
            }
        }
    }
}

@Composable
private fun AnimatedAnt() {
    val transition = rememberInfiniteTransition(label = "ant-walk")
    val step by transition.animateFloat(
        initialValue = -6f,
        targetValue = 6f,
        animationSpec = infiniteRepeatable(
            animation = tween(durationMillis = 620, easing = FastOutSlowInEasing),
            repeatMode = RepeatMode.Reverse
        ),
        label = "step"
    )
    val body = MaterialTheme.colorScheme.primary
    Canvas(modifier = Modifier.size(54.dp)) {
        val centerY = size.height / 2f
        val x = size.width / 2f + step
        drawCircle(body, radius = 8f, center = Offset(x - 13f, centerY))
        drawCircle(body, radius = 11f, center = Offset(x + 2f, centerY))
        drawCircle(body, radius = 7f, center = Offset(x + 18f, centerY - 2f))
        listOf(-12f, 0f, 12f).forEach { leg ->
            drawLine(body, Offset(x + leg, centerY + 5f), Offset(x + leg - 7f, centerY + 17f + step / 2f), 3f, StrokeCap.Round)
            drawLine(body, Offset(x + leg, centerY - 5f), Offset(x + leg + 7f, centerY - 17f - step / 2f), 3f, StrokeCap.Round)
        }
        drawLine(body, Offset(x + 22f, centerY - 6f), Offset(x + 30f, centerY - 18f), 2f, StrokeCap.Round)
        drawLine(body, Offset(x + 22f, centerY - 5f), Offset(x + 32f, centerY - 8f), 2f, StrokeCap.Round)
    }
}

@Composable
private fun ChatInput(value: String, enabled: Boolean, onValueChange: (String) -> Unit, onSend: () -> Unit) {
    Row(
        modifier = Modifier
            .fillMaxWidth()
            .padding(vertical = 12.dp)
            .background(Color(0xAA211D18), RoundedCornerShape(28.dp))
            .padding(8.dp),
        verticalAlignment = Alignment.CenterVertically,
        horizontalArrangement = Arrangement.spacedBy(8.dp)
    ) {
        OutlinedTextField(
            modifier = Modifier.weight(1f),
            value = value,
            enabled = enabled,
            onValueChange = onValueChange,
            placeholder = { Text("Message ANT AI") },
            shape = RoundedCornerShape(22.dp)
        )
        Button(
            enabled = enabled && value.trim().isNotEmpty(),
            onClick = onSend,
            colors = ButtonDefaults.buttonColors(containerColor = MaterialTheme.colorScheme.primary)
        ) {
            Text("Send", color = MaterialTheme.colorScheme.onPrimary)
        }
    }
}
