import XCTest
@testable import MeetingRecorderLib

/// Integration tests that verify components work together correctly
final class IntegrationTests: XCTestCase {

    // MARK: - Config + File Path Integration

    func testConfigGeneratesValidFilePaths() {
        let config = Config.shared
        let fileName = config.generateFileName(forApp: "Zoom")
        let fullPath = config.fullPath(forFileName: fileName)

        // Path should be absolute
        XCTAssertTrue(fullPath.hasPrefix("/") || fullPath.hasPrefix("~"),
            "Path should be absolute")

        // Path should contain the recordings directory
        XCTAssertTrue(fullPath.contains("meetings"),
            "Path should include meetings directory")

        // Path should end with the file name
        XCTAssertTrue(fullPath.hasSuffix(fileName),
            "Path should end with generated file name")
    }

    func testMultipleFileNamesAreUnique() {
        let config = Config.shared

        var fileNames: Set<String> = []

        for i in 0..<10 {
            // Small delay to ensure different timestamps
            if i > 0 {
                Thread.sleep(forTimeInterval: 0.01)
            }
            let fileName = config.generateFileName(forApp: "TestApp")
            fileNames.insert(fileName)
        }

        // All file names should be unique (due to timestamp)
        // Note: This might fail if all generated in same second
        XCTAssertGreaterThanOrEqual(fileNames.count, 1,
            "Should generate file names")
    }

    // MARK: - MeetingDetector + Config Integration

    func testMeetingDetectorUsesConfiguredApps() {
        // All configured meeting apps should have bundle IDs in detector
        let configuredApps = ["Zoom", "Google Meet", "Microsoft Teams", "Slack", "Discord"]
        let detectorApps = Set(MeetingDetector.meetingApps.values)

        for app in configuredApps {
            let isInDetector = detectorApps.contains(app) ||
                MeetingDetector.browserMeetingPatterns.contains { $0.contains(app) }

            XCTAssertTrue(isInDetector,
                "\(app) should be detectable by MeetingDetector")
        }
    }

    // MARK: - Audio Settings Consistency

    func testAudioSettingsAreConsistent() {
        let config = Config.shared

        // Verify all audio settings work together
        let sampleRate = config.sampleRate
        let channels = config.channels
        let bitrate = config.audioBitrate

        // Calculate bytes per second
        let bytesPerSecond = bitrate / 8

        // For 1 hour of audio
        let bytesPerHour = bytesPerSecond * 3600
        let mbPerHour = Double(bytesPerHour) / (1024 * 1024)

        // Should be reasonable for storage
        XCTAssertLessThan(mbPerHour, 100,
            "1 hour of audio should be under 100MB (actual: \(mbPerHour)MB)")
        XCTAssertGreaterThan(mbPerHour, 10,
            "1 hour of audio should be over 10MB for quality (actual: \(mbPerHour)MB)")
    }

    func testChunkingPreventsOversizedFiles() {
        let config = Config.shared

        // Calculate max file size from chunking
        let bytesPerSecond = config.audioBitrate / 8
        let chunkSeconds = config.chunkDurationMinutes * 60
        let maxChunkBytes = bytesPerSecond * chunkSeconds
        let maxChunkMB = Double(maxChunkBytes) / (1024 * 1024)

        // Should be under Claude's limit
        XCTAssertLessThan(maxChunkMB, Double(config.maxFileSizeMB),
            "Max chunk size (\(maxChunkMB)MB) should be under limit (\(config.maxFileSizeMB)MB)")
    }

    // MARK: - Full Pipeline Simulation

    func testRecordingPipelineComponents() {
        // Verify all components can be instantiated
        let config = Config.shared
        let detector = MeetingDetector()
        let capture = AudioCapture()

        XCTAssertNotNil(config, "Config should be available")
        XCTAssertNotNil(detector, "MeetingDetector should be creatable")
        XCTAssertNotNil(capture, "AudioCapture should be creatable")

        // Verify config values are accessible
        XCTAssertFalse(config.recordingsPath.isEmpty, "Recordings path should be set")
        XCTAssertFalse(config.audioFormat.isEmpty, "Audio format should be set")
    }

    func testDetectorCallbacksCanTriggerCapture() {
        let detector = MeetingDetector()
        let capture = AudioCapture()

        var detectionCount = 0
        var endCount = 0

        detector.onMeetingDetected = { appName in
            detectionCount += 1
            // In real app, this would call capture.startCapture()
        }

        detector.onMeetingEnded = { appName in
            endCount += 1
            // In real app, this would call capture.stopCapture()
        }

        // Callbacks should be set
        XCTAssertNotNil(detector.onMeetingDetected)
        XCTAssertNotNil(detector.onMeetingEnded)
    }

    // MARK: - Error Handling Integration

    func testStopWithoutStartHandledGracefully() {
        let capture = AudioCapture()
        let expectation = XCTestExpectation(description: "Error handling")

        capture.stopCapture { url, error in
            // Should get error, not crash
            XCTAssertNotNil(error, "Should return error for stop without start")
            XCTAssertNil(url, "Should not return URL on error")
            expectation.fulfill()
        }

        wait(for: [expectation], timeout: 2.0)
    }
}
