# ANT AI release optimization rules

# Keep application classes
-keep class com.antai.** { *; }

# Keep Kotlin metadata
-keep class kotlin.Metadata { *; }

# Keep Compose runtime classes
-keep class androidx.compose.** { *; }

# Keep annotations and signatures
-keepattributes *Annotation*
-keepattributes Signature
