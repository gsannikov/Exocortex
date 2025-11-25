import XCTest
@testable import MeetingRecorder

final class ConfigTests: XCTestCase {

    // MARK: - Default Values Tests

    func testDefaultAudioFormat() {
        let config = Config.shared
        XCTAssertEqual(config.audioFormat, "m4a", "Default audio format should be m4a")
    }

    func testDefaultAudioBitrate() {
        let config = Config.shared
        XCTAssertEqual(config.audioBitrate, 64000, "Default bitrate should be 64kbps")
    }

    func testDefaultSampleRate() {
        let config = Config.shared
        XCTAssertEqual(config.sampleRate, 16000, "Default sample rate should be 16kHz for speech")
    }

    func testDefaultChannels() {
        let config = Config.shared
        XCTAssertEqual(config.channels, 1, "Default should be mono (1 channel)")
    }

    func testDefaultMaxFileSizeMB() {
        let config = Config.shared
        XCTAssertEqual(config.maxFileSizeMB, 25, "Max file size should be 25MB (Claude's limit)")
    }

    func testDefaultChunkDuration() {
        let config = Config.shared
        XCTAssertEqual(config.chunkDurationMinutes, 40, "Default chunk duration should be 40 minutes")
    }

    func testAutoChunkEnabledByDefault() {
        let config = Config.shared
        XCTAssertTrue(config.autoChunk, "Auto-chunking should be enabled by default")
    }

    func testAutoDetectMeetingsEnabledByDefault() {
        let config = Config.shared
        XCTAssertTrue(config.autoDetectMeetings, "Auto-detect meetings should be enabled")
    }

    func testNotificationsEnabledByDefault() {
        let config = Config.shared
        XCTAssertTrue(config.notificationsEnabled, "Notifications should be enabled by default")
    }

    func testAutoRecordDisabledByDefault() {
        let config = Config.shared
        XCTAssertFalse(config.autoRecord, "Auto-record should be disabled by default (require confirmation)")
    }

    // MARK: - File Name Generation Tests

    func testFileNameGeneration() {
        let config = Config.shared
        let fileName = config.generateFileName(forApp: "Zoom")

        // Should contain date pattern and app name
        XCTAssertTrue(fileName.contains("zoom"), "File name should contain sanitized app name")
        XCTAssertTrue(fileName.hasSuffix(".m4a"), "File name should have correct extension")
        XCTAssertTrue(fileName.contains("_"), "File name should use underscores as separator")
    }

    func testFileNameSanitization() {
        let config = Config.shared

        // Test with special characters
        let fileName1 = config.generateFileName(forApp: "Google Meet")
        XCTAssertTrue(fileName1.contains("google-meet"), "Spaces should be replaced with hyphens")

        let fileName2 = config.generateFileName(forApp: "Teams (Browser)")
        XCTAssertFalse(fileName2.contains("("), "Parentheses should be removed")
        XCTAssertFalse(fileName2.contains(")"), "Parentheses should be removed")
    }

    func testFileNameDateFormat() {
        let config = Config.shared
        let fileName = config.generateFileName(forApp: "Zoom")

        // Should match pattern: YYYY-MM-DD_HH-mm-ss_app.m4a
        let pattern = #"^\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2}_.*\.m4a$"#
        let regex = try? NSRegularExpression(pattern: pattern)
        let range = NSRange(fileName.startIndex..., in: fileName)
        let match = regex?.firstMatch(in: fileName, range: range)

        XCTAssertNotNil(match, "File name should match expected date format pattern")
    }

    // MARK: - Path Tests

    func testRecordingsPathContainsExpectedDirectory() {
        let config = Config.shared
        let path = config.recordingsPath

        XCTAssertTrue(path.contains("voice-memos"), "Path should contain voice-memos")
        XCTAssertTrue(path.contains("meetings"), "Path should contain meetings subdirectory")
    }

    func testFullPathGeneration() {
        let config = Config.shared
        let fileName = "test-recording.m4a"
        let fullPath = config.fullPath(forFileName: fileName)

        XCTAssertTrue(fullPath.hasSuffix(fileName), "Full path should end with file name")
        XCTAssertTrue(fullPath.contains(config.recordingsPath), "Full path should contain recordings path")
    }

    // MARK: - Audio Settings Validation

    func testBitrateIsReasonableForSpeech() {
        let config = Config.shared
        // Speech typically needs 32-128 kbps
        XCTAssertGreaterThanOrEqual(config.audioBitrate, 32000, "Bitrate should be at least 32kbps")
        XCTAssertLessThanOrEqual(config.audioBitrate, 128000, "Bitrate should not exceed 128kbps for speech")
    }

    func testSampleRateIsOptimalForSpeech() {
        let config = Config.shared
        // 16kHz is optimal for speech recognition
        XCTAssertEqual(config.sampleRate, 16000, "16kHz is optimal for speech recognition")
    }

    func testChunkDurationKeepsFileSizeUnderLimit() {
        let config = Config.shared

        // Calculate expected file size for chunk duration
        // 64kbps = 64000 bits/sec = 8000 bytes/sec = 0.48 MB/min
        let bytesPerMinute = Double(config.audioBitrate) / 8.0 * 60.0
        let mbPerMinute = bytesPerMinute / (1024.0 * 1024.0)
        let expectedMB = mbPerMinute * Double(config.chunkDurationMinutes)

        XCTAssertLessThan(expectedMB, Double(config.maxFileSizeMB),
            "Chunk duration should produce files under max size limit. Expected: \(expectedMB)MB, Limit: \(config.maxFileSizeMB)MB")
    }
}
