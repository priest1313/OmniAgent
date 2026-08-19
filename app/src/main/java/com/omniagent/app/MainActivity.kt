package com.omniagent.app

import android.content.Intent
import android.os.Bundle
import android.provider.Settings
import android.widget.Button
import android.widget.TextView
import androidx.appcompat.app.AppCompatActivity

class MainActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        
        // ساخت یک نمای ساده‌ی متنی و دکمه برای فعال‌سازی ایجنت روی گوشی
        val layout = android.widget.LinearLayout(this).apply {
            orientation = android.widget.LinearLayout.VERTICAL
            setPadding(50, 100, 50, 50)
        }

        val title = TextView(this).apply {
            text = "OmniAgent Controller"
            textSize = 22f
            setPadding(0, 0, 0, 40)
        }

        val btnEnable = Button(this).apply {
            text = "فعال‌سازی دسترسی ایجنت (Accessibility)"
            setOnClickListener {
                // هدایت کاربر به تنظیمات دسترسی‌پذیری اندروید برای فعال کردن سرویس
                val intent = Intent(Settings.ACTION_ACCESSIBILITY_SETTINGS)
                startActivity(intent)
            }
        }

        layout.addView(title)
        layout.addView(btnEnable)
        setContentView(layout)
    }
}
