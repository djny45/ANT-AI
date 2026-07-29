package com.antclaw.data

class AntRoomDatabase {
    private val dao = mutableListOf<MessageEntity>()

    fun messageDao(): List<MessageEntity> = dao
}
