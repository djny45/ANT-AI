package com.antai.ui.components

import android.content.Context
import android.content.Intent

fun openAttachmentPicker(context: Context) {
    val intent = Intent(Intent.ACTION_OPEN_DOCUMENT).apply {
        type = "*/*"
        putExtra(Intent.EXTRA_ALLOW_MULTIPLE, true)
        addCategory(Intent.CATEGORY_OPENABLE)
    }
    context.startActivity(intent)
}
