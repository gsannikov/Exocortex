import AppKit
import Foundation
import MeetingRecorderLib

// Entry point for the Meeting Recorder app
let app = NSApplication.shared
let delegate = AppDelegate()
app.delegate = delegate

// Run as a menu bar app (no dock icon)
app.setActivationPolicy(.accessory)
app.run()
