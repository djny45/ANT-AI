package com.antai.ui

import androidx.compose.animation.core.FastOutSlowInEasing
import androidx.compose.animation.core.RepeatMode
import androidx.compose.animation.core.animateFloat
import androidx.compose.animation.core.infiniteRepeatable
import androidx.compose.animation.core.rememberInfiniteTransition
import androidx.compose.animation.core.tween
import androidx.compose.foundation.Canvas
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.ExperimentalLayoutApi
import androidx.compose.foundation.layout.FlowRow
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.shape.CircleShape
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
import androidx.compose.ui.draw.clip
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.StrokeCap
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import com.antai.core.ANTBridge
import kotlinx.coroutines.delay

private data class ChatMessage(val author: String, val text: String, val fromUser: Boolean)

@Composable
@OptIn(ExperimentalLayoutApi::class)
fun ChatScreen(modifier: Modifier = Modifier) {
    val bridge = remember { ANTBridge() }
    val messages = remember { mutableStateListOf<ChatMessage>() }
    var input by remember { mutableStateOf("") }
    var isThinking by remember { mutableStateOf(false) }

    LaunchedEffect(isThinking, messages.size) {
        if (isThinking) {
            delay(900)
            val lastTask = messages.lastOrNull { it.fromUser }?.text.orEmpty()
            messages += ChatMessage("Ant AI", bridge.executeTask(lastTask), false)
            isThinking = false
        }
    }

    LazyColumn(
        modifier = modifier
            .fillMaxSize()
            .padding(horizontal = 18.dp),
        verticalArrangement = Arrangement.spacedBy(16.dp)
    ) {
        item { TopBar() }
        item { HeroHeader() }
        item {
            PromptBox(
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
        item {
            FlowRow(horizontalArrangement = Arrangement.spacedBy(8.dp), verticalArrangement = Arrangement.spacedBy(8.dp)) {
                listOf("Explain a complex topic", "Help me write code", "Analyze data", "Build APK").forEach { label ->
                    SuggestionChip(label) {
                        messages += ChatMessage("You", label, true)
                        isThinking = true
                    }
                }
            }
        }
        if (isThinking) item { ThinkingBubble() }
        messages.forEach { message -> item { MessageCard(message) } }
        item { FeatureGrid() }
        item { RecentChats() }
        item { DownloadCard() }
        item { Spacer(Modifier.height(10.dp)) }
    }
}

@Composable
private fun TopBar() {
    Row(
        modifier = Modifier
            .fillMaxWidth()
            .padding(top = 8.dp),
        verticalAlignment = Alignment.CenterVertically,
        horizontalArrangement = Arrangement.SpaceBetween
    ) {
        Text("Ant AI", color = MaterialTheme.colorScheme.onBackground, style = MaterialTheme.typography.titleMedium, fontWeight = FontWeight.Bold)
        Row(horizontalArrangement = Arrangement.spacedBy(10.dp), verticalAlignment = Alignment.CenterVertically) {
            Text("+", color = MaterialTheme.colorScheme.primary, style = MaterialTheme.typography.headlineSmall)
            Text("Edit", color = Color(0xFF7A4A2F), style = MaterialTheme.typography.labelMedium)
        }
    }
}

@Composable
private fun HeroHeader() {
    Column(
        modifier = Modifier.fillMaxWidth(),
        horizontalAlignment = Alignment.CenterHorizontally
    ) {
        AnimatedAnt(72.dp)
        Spacer(Modifier.height(12.dp))
        Text(
            "Good morning, Yogesh Nayak",
            color = MaterialTheme.colorScheme.onBackground,
            style = MaterialTheme.typography.headlineSmall,
            textAlign = TextAlign.Center,
            fontWeight = FontWeight.Bold,
            fontFamily = FontFamily.Serif
        )
        Spacer(Modifier.height(6.dp))
        Text("How can I help you today?", color = Color(0xFF6F6259), style = MaterialTheme.typography.bodyMedium)
    }
}

@Composable
private fun PromptBox(value: String, enabled: Boolean, onValueChange: (String) -> Unit, onSend: () -> Unit) {
    Card(
        modifier = Modifier.fillMaxWidth(),
        shape = RoundedCornerShape(24.dp),
        colors = CardDefaults.cardColors(containerColor = Color.White),
        elevation = CardDefaults.cardElevation(defaultElevation = 8.dp)
    ) {
        Column(Modifier.padding(14.dp)) {
            OutlinedTextField(
                modifier = Modifier.fillMaxWidth(),
                value = value,
                enabled = enabled,
                onValueChange = onValueChange,
                placeholder = { Text("Message Ant AI...") },
                minLines = 2,
                shape = RoundedCornerShape(18.dp)
            )
            Spacer(Modifier.height(12.dp))
            Row(
                modifier = Modifier.fillMaxWidth(),
                verticalAlignment = Alignment.CenterVertically,
                horizontalArrangement = Arrangement.SpaceBetween
            ) {
                Row(horizontalArrangement = Arrangement.spacedBy(10.dp), verticalAlignment = Alignment.CenterVertically) {
                    RoundIcon("+")
                    RoundIcon("Web")
                    RoundIcon("Tune")
                    Text(
                        "Ant Core",
                        modifier = Modifier
                            .clip(RoundedCornerShape(100.dp))
                            .background(Color(0xFFF7EFE7))
                            .padding(horizontal = 12.dp, vertical = 8.dp),
                        color = MaterialTheme.colorScheme.onSurface,
                        style = MaterialTheme.typography.labelMedium,
                        fontWeight = FontWeight.Bold
                    )
                }
                Button(
                    onClick = onSend,
                    enabled = enabled && value.trim().isNotEmpty(),
                    shape = CircleShape,
                    colors = ButtonDefaults.buttonColors(containerColor = MaterialTheme.colorScheme.primary),
                    modifier = Modifier.size(46.dp),
                    contentPadding = androidx.compose.foundation.layout.PaddingValues(0.dp)
                ) { Text("->", color = Color.White, fontWeight = FontWeight.Bold) }
            }
        }
    }
}

@Composable
private fun RoundIcon(label: String) {
    Box(
        modifier = Modifier
            .size(34.dp)
            .clip(CircleShape)
            .background(Color(0xFFF7EFE7)),
        contentAlignment = Alignment.Center
    ) {
        Text(label, color = Color(0xFF7A4A2F), style = MaterialTheme.typography.labelSmall, fontWeight = FontWeight.Bold)
    }
}

@Composable
private fun SuggestionChip(label: String, onClick: () -> Unit) {
    Text(
        text = label,
        modifier = Modifier
            .clip(RoundedCornerShape(100.dp))
            .background(Color.White)
            .clickable { onClick() }
            .padding(horizontal = 12.dp, vertical = 9.dp),
        color = MaterialTheme.colorScheme.onSurface,
        style = MaterialTheme.typography.labelMedium,
        fontWeight = FontWeight.Bold
    )
}

@Composable
private fun FeatureGrid() {
    Column(verticalArrangement = Arrangement.spacedBy(10.dp)) {
        Row(horizontalArrangement = Arrangement.spacedBy(10.dp)) {
            FeatureCard("Smart Agents", "Specialized AI agents for any task", Modifier.weight(1f))
            FeatureCard("Deep Research", "Get in-depth insights and reports", Modifier.weight(1f))
        }
        Row(horizontalArrangement = Arrangement.spacedBy(10.dp)) {
            FeatureCard("Code Assistant", "Write, debug, and improve code", Modifier.weight(1f))
            FeatureCard("File Analysis", "Upload and analyze documents", Modifier.weight(1f))
        }
    }
}

@Composable
private fun FeatureCard(title: String, subtitle: String, modifier: Modifier = Modifier) {
    Card(
        modifier = modifier.height(132.dp),
        colors = CardDefaults.cardColors(containerColor = Color.White),
        shape = RoundedCornerShape(22.dp),
        elevation = CardDefaults.cardElevation(defaultElevation = 2.dp)
    ) {
        Column(Modifier.padding(14.dp), verticalArrangement = Arrangement.SpaceBetween) {
            RoundIcon("ANT")
            Column {
                Text(title, color = MaterialTheme.colorScheme.onSurface, fontWeight = FontWeight.Bold)
                Text(subtitle, color = Color(0xFF6F6259), style = MaterialTheme.typography.bodySmall)
            }
        }
    }
}

@Composable
private fun RecentChats() {
    Column(verticalArrangement = Arrangement.spacedBy(10.dp)) {
        Row(Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween, verticalAlignment = Alignment.CenterVertically) {
            Text("Recent Chats", color = MaterialTheme.colorScheme.onBackground, fontWeight = FontWeight.Bold)
            Text("View all", color = MaterialTheme.colorScheme.primary, style = MaterialTheme.typography.labelMedium, fontWeight = FontWeight.Bold)
        }
        listOf("Build e-waste recycling app", "Market research analysis", "Explain quantum computing").forEachIndexed { index, title ->
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .clip(RoundedCornerShape(16.dp))
                    .background(Color.White)
                    .padding(14.dp),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically
            ) {
                Text(title, color = MaterialTheme.colorScheme.onSurface, style = MaterialTheme.typography.bodyMedium)
                Text(listOf("2h ago", "Yesterday", "2d ago")[index], color = Color(0xFF9A8C82), style = MaterialTheme.typography.labelSmall)
            }
        }
    }
}

@Composable
private fun DownloadCard() {
    Card(
        modifier = Modifier.fillMaxWidth(),
        colors = CardDefaults.cardColors(containerColor = Color(0xFFFFE7D7)),
        shape = RoundedCornerShape(22.dp)
    ) {
        Column(Modifier.padding(16.dp)) {
            Text("APK Download", color = MaterialTheme.colorScheme.primary, fontWeight = FontWeight.Bold)
            Text("https://github.com/djny45/ANT-AI/releases/", color = MaterialTheme.colorScheme.onSurface, style = MaterialTheme.typography.bodySmall)
        }
    }
}

@Composable
private fun MessageCard(message: ChatMessage) {
    val background = if (message.fromUser) Color(0xFFFFE7D7) else Color.White
    Card(
        modifier = Modifier.fillMaxWidth(),
        colors = CardDefaults.cardColors(containerColor = background),
        shape = RoundedCornerShape(22.dp),
        elevation = CardDefaults.cardElevation(defaultElevation = 2.dp)
    ) {
        Column(Modifier.padding(16.dp)) {
            Text(message.author, color = MaterialTheme.colorScheme.primary, fontWeight = FontWeight.Bold)
            Spacer(Modifier.height(6.dp))
            Text(message.text, color = MaterialTheme.colorScheme.onSurface, style = MaterialTheme.typography.bodyMedium)
        }
    }
}

@Composable
private fun ThinkingBubble() {
    Card(
        modifier = Modifier.fillMaxWidth(),
        colors = CardDefaults.cardColors(containerColor = Color.White),
        shape = RoundedCornerShape(22.dp),
        elevation = CardDefaults.cardElevation(defaultElevation = 2.dp)
    ) {
        Row(
            modifier = Modifier.padding(16.dp),
            verticalAlignment = Alignment.CenterVertically,
            horizontalArrangement = Arrangement.spacedBy(12.dp)
        ) {
            AnimatedAnt(42.dp)
            Column {
                Text("Ant AI is thinking", color = MaterialTheme.colorScheme.primary, fontWeight = FontWeight.Bold)
                Text("Routing your request", color = Color(0xFF6F6259))
            }
        }
    }
}

@Composable
private fun AnimatedAnt(size: androidx.compose.ui.unit.Dp) {
    val transition = rememberInfiniteTransition(label = "ant-walk")
    val step by transition.animateFloat(
        initialValue = -5f,
        targetValue = 5f,
        animationSpec = infiniteRepeatable(
            animation = tween(durationMillis = 620, easing = FastOutSlowInEasing),
            repeatMode = RepeatMode.Reverse
        ),
        label = "step"
    )
    val orange = MaterialTheme.colorScheme.primary
    Canvas(modifier = Modifier.size(size)) {
        drawCircle(Color(0x22F26A21), radius = this.size.minDimension / 2.3f, center = center)
        val centerY = this.size.height / 2f
        val x = this.size.width / 2f + step
        drawCircle(orange, radius = this.size.minDimension * 0.12f, center = Offset(x - 13f, centerY))
        drawCircle(orange, radius = this.size.minDimension * 0.16f, center = Offset(x + 2f, centerY))
        drawCircle(orange, radius = this.size.minDimension * 0.10f, center = Offset(x + 18f, centerY - 2f))
        listOf(-12f, 0f, 12f).forEach { leg ->
            drawLine(orange, Offset(x + leg, centerY + 5f), Offset(x + leg - 8f, centerY + 18f + step / 2f), 3f, StrokeCap.Round)
            drawLine(orange, Offset(x + leg, centerY - 5f), Offset(x + leg + 8f, centerY - 18f - step / 2f), 3f, StrokeCap.Round)
        }
        drawLine(orange, Offset(x + 22f, centerY - 6f), Offset(x + 31f, centerY - 18f), 2.5f, StrokeCap.Round)
        drawLine(orange, Offset(x + 22f, centerY - 5f), Offset(x + 33f, centerY - 8f), 2.5f, StrokeCap.Round)
    }
}
