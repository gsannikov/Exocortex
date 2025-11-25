import AppKit
import Foundation
import UserNotifications

public class AppDelegate: NSObject, NSApplicationDelegate {
    var statusItem: NSStatusItem!
    var meetingDetector: MeetingDetector!
    var audioCapture: AudioCapture!
    var isRecording = false
    var recordingStartTime: Date?
    var currentMeetingApp: String?
    var recordingTimer: Timer?

    public func applicationDidFinishLaunching(_ notification: Notification) {
        // Request notification permission
        requestNotificationPermission()

        // Setup menu bar
        setupMenuBar()

        // Initialize components
        meetingDetector = MeetingDetector()
        audioCapture = AudioCapture()

        // Set up meeting detection callback
        meetingDetector.onMeetingDetected = { [weak self] appName in
            self?.handleMeetingDetected(appName: appName)
        }

        meetingDetector.onMeetingEnded = { [weak self] appName in
            self?.handleMeetingEnded(appName: appName)
        }

        // Start monitoring for meetings
        meetingDetector.startMonitoring()

        print("Meeting Recorder started. Monitoring for meeting apps...")
    }

    func setupMenuBar() {
        statusItem = NSStatusBar.system.statusItem(withLength: NSStatusItem.variableLength)

        if let button = statusItem.button {
            button.image = NSImage(systemSymbolName: "mic.circle", accessibilityDescription: "Meeting Recorder")
            button.image?.isTemplate = true
        }

        updateMenu()
    }

    func updateMenu() {
        let menu = NSMenu()

        // Status header
        let statusTitle = isRecording ? "Recording..." : "Ready"
        let statusItem = NSMenuItem(title: statusTitle, action: nil, keyEquivalent: "")
        statusItem.isEnabled = false
        menu.addItem(statusItem)

        if isRecording, let startTime = recordingStartTime {
            let duration = Date().timeIntervalSince(startTime)
            let durationStr = formatDuration(duration)
            let durationItem = NSMenuItem(title: "  Duration: \(durationStr)", action: nil, keyEquivalent: "")
            durationItem.isEnabled = false
            menu.addItem(durationItem)

            if let app = currentMeetingApp {
                let appItem = NSMenuItem(title: "  App: \(app)", action: nil, keyEquivalent: "")
                appItem.isEnabled = false
                menu.addItem(appItem)
            }
        }

        menu.addItem(NSMenuItem.separator())

        // Record/Stop button
        if isRecording {
            menu.addItem(NSMenuItem(title: "Stop Recording", action: #selector(stopRecording), keyEquivalent: "s"))
        } else {
            menu.addItem(NSMenuItem(title: "Start Recording", action: #selector(startRecordingManual), keyEquivalent: "r"))
        }

        menu.addItem(NSMenuItem.separator())

        // Open recordings folder
        menu.addItem(NSMenuItem(title: "Open Recordings Folder", action: #selector(openRecordingsFolder), keyEquivalent: "o"))

        // Settings
        menu.addItem(NSMenuItem(title: "Settings...", action: #selector(openSettings), keyEquivalent: ","))

        menu.addItem(NSMenuItem.separator())

        // Quit
        menu.addItem(NSMenuItem(title: "Quit", action: #selector(quitApp), keyEquivalent: "q"))

        self.statusItem.menu = menu
    }

    func requestNotificationPermission() {
        UNUserNotificationCenter.current().requestAuthorization(options: [.alert, .sound]) { granted, error in
            if granted {
                print("Notification permission granted")
            }
        }
    }

    func handleMeetingDetected(appName: String) {
        currentMeetingApp = appName

        // Show notification asking to record
        let content = UNMutableNotificationContent()
        content.title = "Meeting Detected"
        content.body = "Would you like to record this \(appName) meeting?"
        content.sound = .default
        content.categoryIdentifier = "MEETING_DETECTED"

        // Add actions
        let recordAction = UNNotificationAction(identifier: "RECORD", title: "Record", options: [.foreground])
        let ignoreAction = UNNotificationAction(identifier: "IGNORE", title: "Ignore", options: [])
        let category = UNNotificationCategory(identifier: "MEETING_DETECTED", actions: [recordAction, ignoreAction], intentIdentifiers: [])

        UNUserNotificationCenter.current().setNotificationCategories([category])
        UNUserNotificationCenter.current().delegate = self

        let request = UNNotificationRequest(identifier: UUID().uuidString, content: content, trigger: nil)
        UNUserNotificationCenter.current().add(request)

        // Update menu bar icon
        DispatchQueue.main.async {
            if let button = self.statusItem.button {
                button.image = NSImage(systemSymbolName: "mic.badge.plus", accessibilityDescription: "Meeting Detected")
            }
        }
    }

    func handleMeetingEnded(appName: String) {
        if isRecording {
            // Show notification that meeting ended
            let content = UNMutableNotificationContent()
            content.title = "Meeting Ended"
            content.body = "Recording will stop. Would you like to process the transcript?"
            content.sound = .default

            let request = UNNotificationRequest(identifier: UUID().uuidString, content: content, trigger: nil)
            UNUserNotificationCenter.current().add(request)

            stopRecording()
        }

        currentMeetingApp = nil

        // Reset menu bar icon
        DispatchQueue.main.async {
            if let button = self.statusItem.button {
                button.image = NSImage(systemSymbolName: "mic.circle", accessibilityDescription: "Meeting Recorder")
            }
        }
    }

    @objc func startRecordingManual() {
        startRecording(appName: "Manual Recording")
    }

    func startRecording(appName: String) {
        guard !isRecording else { return }

        currentMeetingApp = appName
        isRecording = true
        recordingStartTime = Date()

        // Update icon to recording state
        if let button = statusItem.button {
            button.image = NSImage(systemSymbolName: "record.circle.fill", accessibilityDescription: "Recording")
        }

        // Start audio capture
        audioCapture.startCapture(forApp: appName) { [weak self] error in
            if let error = error {
                print("Failed to start capture: \(error)")
                DispatchQueue.main.async {
                    self?.isRecording = false
                    self?.showError("Failed to start recording: \(error.localizedDescription)")
                }
            }
        }

        // Start timer to update menu periodically
        recordingTimer = Timer.scheduledTimer(withTimeInterval: 1.0, repeats: true) { [weak self] _ in
            self?.updateMenu()
        }

        updateMenu()

        print("Started recording: \(appName)")
    }

    @objc func stopRecording() {
        guard isRecording else { return }

        isRecording = false
        recordingTimer?.invalidate()
        recordingTimer = nil

        // Update icon
        if let button = statusItem.button {
            button.image = NSImage(systemSymbolName: "mic.circle", accessibilityDescription: "Meeting Recorder")
        }

        // Stop audio capture and save file
        audioCapture.stopCapture { [weak self] fileURL, error in
            if let error = error {
                print("Failed to stop capture: \(error)")
                self?.showError("Failed to save recording: \(error.localizedDescription)")
                return
            }

            if let fileURL = fileURL {
                print("Recording saved to: \(fileURL.path)")
                self?.showRecordingSaved(fileURL: fileURL)
            }
        }

        recordingStartTime = nil
        updateMenu()

        print("Stopped recording")
    }

    func showRecordingSaved(fileURL: URL) {
        let content = UNMutableNotificationContent()
        content.title = "Recording Saved"
        content.body = "Meeting recording saved. Ready for transcription."
        content.sound = .default
        content.categoryIdentifier = "RECORDING_SAVED"

        let openAction = UNNotificationAction(identifier: "OPEN_FOLDER", title: "Open Folder", options: [.foreground])
        let transcribeAction = UNNotificationAction(identifier: "TRANSCRIBE", title: "Transcribe Now", options: [.foreground])
        let category = UNNotificationCategory(identifier: "RECORDING_SAVED", actions: [openAction, transcribeAction], intentIdentifiers: [])

        UNUserNotificationCenter.current().setNotificationCategories([category])

        let request = UNNotificationRequest(identifier: UUID().uuidString, content: content, trigger: nil)
        UNUserNotificationCenter.current().add(request)
    }

    func showError(_ message: String) {
        let content = UNMutableNotificationContent()
        content.title = "Recording Error"
        content.body = message
        content.sound = .default

        let request = UNNotificationRequest(identifier: UUID().uuidString, content: content, trigger: nil)
        UNUserNotificationCenter.current().add(request)
    }

    @objc func openRecordingsFolder() {
        let recordingsPath = Config.shared.recordingsPath
        NSWorkspace.shared.open(URL(fileURLWithPath: recordingsPath))
    }

    @objc func openSettings() {
        // Open config file in default editor
        let configPath = Config.shared.configFilePath
        NSWorkspace.shared.open(URL(fileURLWithPath: configPath))
    }

    @objc func quitApp() {
        if isRecording {
            stopRecording()
        }
        NSApplication.shared.terminate(nil)
    }

    func formatDuration(_ interval: TimeInterval) -> String {
        let hours = Int(interval) / 3600
        let minutes = (Int(interval) % 3600) / 60
        let seconds = Int(interval) % 60

        if hours > 0 {
            return String(format: "%d:%02d:%02d", hours, minutes, seconds)
        } else {
            return String(format: "%02d:%02d", minutes, seconds)
        }
    }
}

// MARK: - Notification Delegate
extension AppDelegate: UNUserNotificationCenterDelegate {
    public func userNotificationCenter(_ center: UNUserNotificationCenter, didReceive response: UNNotificationResponse, withCompletionHandler completionHandler: @escaping () -> Void) {
        switch response.actionIdentifier {
        case "RECORD":
            if let appName = currentMeetingApp {
                startRecording(appName: appName)
            }
        case "OPEN_FOLDER":
            openRecordingsFolder()
        case "TRANSCRIBE":
            // Trigger transcription via voice-memos skill
            triggerTranscription()
        default:
            break
        }
        completionHandler()
    }

    public func userNotificationCenter(_ center: UNUserNotificationCenter, willPresent notification: UNNotification, withCompletionHandler completionHandler: @escaping (UNNotificationPresentationOptions) -> Void) {
        completionHandler([.banner, .sound])
    }

    func triggerTranscription() {
        // Write a trigger file that Claude can detect
        let triggerPath = Config.shared.recordingsPath + "/.transcribe_trigger"
        FileManager.default.createFile(atPath: triggerPath, contents: Data(), attributes: nil)
        print("Transcription trigger created")
    }
}
