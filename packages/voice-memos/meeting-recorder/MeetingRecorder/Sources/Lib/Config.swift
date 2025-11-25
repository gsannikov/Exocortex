import Foundation

/// Configuration for the Meeting Recorder app
public class Config {
    public static let shared = Config()

    // Default paths
    private let defaultDataPath: String
    private let defaultConfigPath: String

    // Loaded configuration
    private var configDict: [String: Any] = [:]

    public init() {
        // Default to claude-skills-data location
        let homeDir = FileManager.default.homeDirectoryForCurrentUser.path
        defaultDataPath = "\(homeDir)/MyDrive/claude-skills-data/voice-memos/meetings"
        defaultConfigPath = "\(homeDir)/MyDrive/claude-skills-data/voice-memos/meeting-recorder-config.yaml"

        // Create directories if needed
        createDirectoriesIfNeeded()

        // Load config
        loadConfig()
    }

    private func createDirectoriesIfNeeded() {
        let fileManager = FileManager.default

        // Create recordings directory
        if !fileManager.fileExists(atPath: defaultDataPath) {
            try? fileManager.createDirectory(atPath: defaultDataPath, withIntermediateDirectories: true)
            print("Created recordings directory: \(defaultDataPath)")
        }
    }

    private func loadConfig() {
        // For now, use defaults. In future, load from YAML file
        configDict = [
            "recordings_path": defaultDataPath,
            "audio_format": "m4a",
            "audio_bitrate": 64000,  // 64kbps for speech
            "sample_rate": 16000,    // 16kHz optimal for speech
            "channels": 1,           // Mono
            "max_file_size_mb": 25,  // Claude's limit
            "auto_chunk": true,
            "chunk_duration_minutes": 40,
            "auto_detect_meetings": true,
            "meeting_apps": [
                "Zoom",
                "Google Meet",
                "Microsoft Teams",
                "Slack",
                "Discord",
                "Webex",
                "FaceTime"
            ],
            "notifications_enabled": true,
            "auto_record": false,    // Require user confirmation by default
        ]
    }

    // MARK: - Accessors

    public var recordingsPath: String {
        return configDict["recordings_path"] as? String ?? defaultDataPath
    }

    public var configFilePath: String {
        return defaultConfigPath
    }

    public var audioFormat: String {
        return configDict["audio_format"] as? String ?? "m4a"
    }

    public var audioBitrate: Int {
        return configDict["audio_bitrate"] as? Int ?? 64000
    }

    public var sampleRate: Int {
        return configDict["sample_rate"] as? Int ?? 16000
    }

    public var channels: Int {
        return configDict["channels"] as? Int ?? 1
    }

    public var maxFileSizeMB: Int {
        return configDict["max_file_size_mb"] as? Int ?? 25
    }

    public var autoChunk: Bool {
        return configDict["auto_chunk"] as? Bool ?? true
    }

    public var chunkDurationMinutes: Int {
        return configDict["chunk_duration_minutes"] as? Int ?? 40
    }

    public var autoDetectMeetings: Bool {
        return configDict["auto_detect_meetings"] as? Bool ?? true
    }

    public var notificationsEnabled: Bool {
        return configDict["notifications_enabled"] as? Bool ?? true
    }

    public var autoRecord: Bool {
        return configDict["auto_record"] as? Bool ?? false
    }

    // MARK: - File naming

    public func generateFileName(forApp appName: String) -> String {
        let dateFormatter = DateFormatter()
        dateFormatter.dateFormat = "yyyy-MM-dd_HH-mm-ss"
        let timestamp = dateFormatter.string(from: Date())

        let sanitizedApp = appName
            .replacingOccurrences(of: " ", with: "-")
            .replacingOccurrences(of: "(", with: "")
            .replacingOccurrences(of: ")", with: "")
            .lowercased()

        return "\(timestamp)_\(sanitizedApp).\(audioFormat)"
    }

    public func fullPath(forFileName fileName: String) -> String {
        return "\(recordingsPath)/\(fileName)"
    }
}
