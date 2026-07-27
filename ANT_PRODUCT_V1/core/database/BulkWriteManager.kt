package com.antai.core.database

/**
 * ANT database write optimization foundation.
 *
 * Purpose:
 * Replace repeated single writes with controlled batch operations.
 *
 * Usage pattern:
 *
 * transaction {
 *     bulkInsert(items.chunked(BATCH_SIZE))
 * }
 */

object BulkWriteManager {

    const val DEFAULT_BATCH_SIZE = 500

    fun <T> chunk(items: List<T>, size: Int = DEFAULT_BATCH_SIZE): List<List<T>> {
        return items.chunked(size)
    }
}
