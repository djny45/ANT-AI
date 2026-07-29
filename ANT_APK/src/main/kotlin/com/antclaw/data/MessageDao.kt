package com.antclaw.data

interface MessageDao {
    fun insert(message: MessageEntity)
    fun getMessages(): List<MessageEntity>
}
