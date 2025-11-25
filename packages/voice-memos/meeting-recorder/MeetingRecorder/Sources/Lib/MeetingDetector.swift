import AppKit
import Foundation

/// Monitors for meeting applications and notifies when meetings start/end
public class MeetingDetector {
    // Bundle identifiers for common meeting apps
    public static let meetingApps: [String: String] = [
        "us.zoom.xos": "Zoom",
        "com.google.Chrome": "Google Meet",  // Meet runs in Chrome
        "com.microsoft.teams": "Microsoft Teams",
        "com.microsoft.teams2": "Microsoft Teams",
        "com.slack.Slack": "Slack",
        "com.discord": "Discord",
        "com.webex.meetingmanager": "Webex",
        "com.gotomeeting": "GoToMeeting",
        "com.apple.FaceTime": "FaceTime"
    ]

    // For Chrome-based apps, check window titles
    public static let browserMeetingPatterns: [String] = [
        "Meet -",           // Google Meet
        "meet.google.com",  // Google Meet URL
        "Zoom Meeting",     // Zoom in browser
        "Microsoft Teams",  // Teams in browser
    ]

    public var onMeetingDetected: ((String) -> Void)?
    public var onMeetingEnded: ((String) -> Void)?

    private var monitorTimer: Timer?
    private var activeMeetings: Set<String> = []
    private var lastWindowTitles: [String] = []

    public init() {}

    public func startMonitoring() {
        // Check every 5 seconds
        monitorTimer = Timer.scheduledTimer(withTimeInterval: 5.0, repeats: true) { [weak self] _ in
            self?.checkForMeetings()
        }
        // Also check immediately
        checkForMeetings()
    }

    public func stopMonitoring() {
        monitorTimer?.invalidate()
        monitorTimer = nil
    }

    private func checkForMeetings() {
        let runningApps = NSWorkspace.shared.runningApplications
        var currentMeetings: Set<String> = []

        for app in runningApps {
            guard let bundleId = app.bundleIdentifier else { continue }

            // Check for native meeting apps
            if let appName = Self.meetingApps[bundleId] {
                // For Zoom, check if actually in a meeting (has meeting window)
                if bundleId == "us.zoom.xos" {
                    if isZoomInMeeting(app: app) {
                        currentMeetings.insert(appName)
                    }
                }
                // For other native apps, just check if running
                else if !bundleId.contains("Chrome") && !bundleId.contains("Safari") {
                    if app.isActive || hasVisibleWindows(app: app) {
                        currentMeetings.insert(appName)
                    }
                }
            }

            // Check browsers for web-based meetings
            if bundleId.contains("Chrome") || bundleId.contains("Safari") || bundleId.contains("Firefox") {
                if let meetingType = checkBrowserForMeeting(app: app) {
                    currentMeetings.insert(meetingType)
                }
            }
        }

        // Detect new meetings
        let newMeetings = currentMeetings.subtracting(activeMeetings)
        for meeting in newMeetings {
            print("Meeting detected: \(meeting)")
            onMeetingDetected?(meeting)
        }

        // Detect ended meetings
        let endedMeetings = activeMeetings.subtracting(currentMeetings)
        for meeting in endedMeetings {
            print("Meeting ended: \(meeting)")
            onMeetingEnded?(meeting)
        }

        activeMeetings = currentMeetings
    }

    private func isZoomInMeeting(app: NSRunningApplication) -> Bool {
        // Zoom shows specific windows when in a meeting
        // This is a heuristic - check for window count and titles
        guard let windows = CGWindowListCopyWindowInfo([.optionOnScreenOnly, .excludeDesktopElements], kCGNullWindowID) as? [[String: Any]] else {
            return false
        }

        let zoomWindows = windows.filter { window in
            guard let ownerPID = window[kCGWindowOwnerPID as String] as? Int32,
                  ownerPID == app.processIdentifier else {
                return false
            }
            return true
        }

        // Zoom typically has multiple windows during a meeting
        // and one of them contains "Zoom Meeting" or similar
        for window in zoomWindows {
            if let title = window[kCGWindowName as String] as? String {
                if title.contains("Zoom Meeting") || title.contains("zoom share") {
                    return true
                }
            }
        }

        // If there are 2+ Zoom windows, likely in a meeting
        return zoomWindows.count >= 2
    }

    private func checkBrowserForMeeting(app: NSRunningApplication) -> String? {
        guard let windows = CGWindowListCopyWindowInfo([.optionOnScreenOnly, .excludeDesktopElements], kCGNullWindowID) as? [[String: Any]] else {
            return nil
        }

        for window in windows {
            guard let ownerPID = window[kCGWindowOwnerPID as String] as? Int32,
                  ownerPID == app.processIdentifier,
                  let title = window[kCGWindowName as String] as? String else {
                continue
            }

            // Check for meeting patterns in browser window titles
            if title.contains("Meet -") || title.contains("meet.google.com") {
                return "Google Meet"
            }
            if title.contains("Microsoft Teams") {
                return "Teams (Browser)"
            }
            if title.contains("Zoom") && title.contains("Meeting") {
                return "Zoom (Browser)"
            }
        }

        return nil
    }

    private func hasVisibleWindows(app: NSRunningApplication) -> Bool {
        guard let windows = CGWindowListCopyWindowInfo([.optionOnScreenOnly, .excludeDesktopElements], kCGNullWindowID) as? [[String: Any]] else {
            return false
        }

        return windows.contains { window in
            guard let ownerPID = window[kCGWindowOwnerPID as String] as? Int32 else {
                return false
            }
            return ownerPID == app.processIdentifier
        }
    }
}
