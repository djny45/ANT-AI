package com.antclaw.core

class VoicePipeline {
    fun process(audio: ByteArray): String {
        return "Voice input received: ${audio.size} bytes"
    }
}
