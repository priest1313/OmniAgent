package com.omniagent.app

import android.accessibilityservice.AccessibilityService
import android.util.Log
import android.view.accessibility.AccessibilityEvent

class OmniAccessibilityService : AccessibilityService() {

    companion object {
        private const val TAG = "OmniAgentCore"
    }

    override fun onServiceConnected() {
        super.onServiceConnected()
        Log.d(TAG, "OmniAgent Accessibility Service Connected Successfully.")
    }

    override fun onAccessibilityEvent(event: AccessibilityEvent) {
        val eventType = event.eventType
        val packageName = event.packageName?.toString() ?: "unknown"
        Log.d(TAG, "Event captured from package: $packageName | Type: $eventType")
    }

    override fun onInterrupt() {
        Log.d(TAG, "OmniAgent Accessibility Service Interrupted.")
    }
}
