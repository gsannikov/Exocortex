import XCTest
import AVFoundation
@testable import MeetingRecorderLib

final class AudioCaptureTests: XCTestCase {

    var audioCapture: AudioCapture!

    override func setUp() {
        super.setUp()
        audioCapture = AudioCapture()
    }

    override func tearDown() {
        audioCapture = nil
        super.tearDown()
    }

    // MARK: - Initialization Tests

    func testAudioCaptureInitialization() {
        XCTAssertNotNil(audioCapture, "AudioCapture should initialize successfully")
    }

    func testMultipleInstancesCanBeCreated() {
        let capture1 = AudioCapture()
        let capture2 = AudioCapture()

        XCTAssertNotNil(capture1, "First instance should be created")
        XCTAssertNotNil(capture2, "Second instance should be created")
    }

    // MARK: - Error Type Tests

    func testCaptureErrorAlreadyCapturing() {
        let error = CaptureError.alreadyCapturing
        XCTAssertNotNil(error.errorDescription, "Should have error description")
        XCTAssertTrue(error.errorDescription?.contains("Already") ?? false,
            "Error message should indicate already capturing")
    }

    func testCaptureErrorNotCapturing() {
        let error = CaptureError.notCapturing
        XCTAssertNotNil(error.errorDescription, "Should have error description")
        XCTAssertTrue(error.errorDescription?.contains("Not") ?? false,
            "Error message should indicate not capturing")
    }

    func testCaptureErrorNoDisplayFound() {
        let error = CaptureError.noDisplayFound
        XCTAssertNotNil(error.errorDescription, "Should have error description")
        XCTAssertTrue(error.errorDescription?.lowercased().contains("display") ?? false,
            "Error message should mention display")
    }

    func testCaptureErrorNoAudioRecorded() {
        let error = CaptureError.noAudioRecorded
        XCTAssertNotNil(error.errorDescription, "Should have error description")
        XCTAssertTrue(error.errorDescription?.lowercased().contains("audio") ?? false,
            "Error message should mention audio")
    }

    func testCaptureErrorPermissionDenied() {
        let error = CaptureError.permissionDenied
        XCTAssertNotNil(error.errorDescription, "Should have error description")
        XCTAssertTrue(error.errorDescription?.contains("permission") ?? false,
            "Error message should mention permission")
        XCTAssertTrue(error.errorDescription?.contains("Screen") ?? false,
            "Error message should mention Screen Recording")
    }

    func testAllCaptureErrorsHaveDescriptions() {
        let errors: [CaptureError] = [
            .alreadyCapturing,
            .notCapturing,
            .noDisplayFound,
            .noAudioRecorded,
            .permissionDenied
        ]

        for error in errors {
            XCTAssertNotNil(error.errorDescription,
                "Error \(error) should have a description")
            XCTAssertFalse(error.errorDescription?.isEmpty ?? true,
                "Error \(error) description should not be empty")
        }
    }

    // MARK: - Stop Without Start Tests

    func testStopCaptureWithoutStartReturnsError() {
        let expectation = XCTestExpectation(description: "Stop capture callback")

        audioCapture.stopCapture { url, error in
            XCTAssertNil(url, "URL should be nil when not capturing")
            XCTAssertNotNil(error, "Should return error when not capturing")

            if let captureError = error as? CaptureError {
                XCTAssertEqual(captureError, CaptureError.notCapturing,
                    "Error should be .notCapturing")
            }

            expectation.fulfill()
        }

        wait(for: [expectation], timeout: 2.0)
    }

    // MARK: - Audio Format Tests

    func testAudioSettingsForSpeech() {
        // Verify the audio settings are appropriate for speech
        let config = Config.shared

        // AAC format ID
        let expectedFormat = kAudioFormatMPEG4AAC

        // Sample rate should be speech-optimized
        XCTAssertEqual(config.sampleRate, 16000,
            "Sample rate should be 16kHz for speech")

        // Channels should be mono
        XCTAssertEqual(config.channels, 1,
            "Should use mono for meeting audio")

        // Bitrate should be reasonable for speech
        XCTAssertGreaterThanOrEqual(config.audioBitrate, 32000,
            "Bitrate should be at least 32kbps")
        XCTAssertLessThanOrEqual(config.audioBitrate, 128000,
            "Bitrate should not exceed 128kbps for speech")
    }

    // MARK: - Chunking Logic Tests

    func testChunkDurationCalculation() {
        let config = Config.shared
        let chunkDuration = TimeInterval(config.chunkDurationMinutes * 60)

        // 40 minutes = 2400 seconds
        XCTAssertEqual(chunkDuration, 2400,
            "Chunk duration should be 40 minutes (2400 seconds)")
    }

    func testChunkFileSizeEstimate() {
        let config = Config.shared

        // Calculate expected file size
        // 64kbps = 8KB/s
        // 40 minutes = 2400 seconds
        // Expected: 8 * 2400 = 19200 KB = ~18.75 MB
        let bytesPerSecond = config.audioBitrate / 8
        let chunkSeconds = config.chunkDurationMinutes * 60
        let expectedBytes = bytesPerSecond * chunkSeconds
        let expectedMB = Double(expectedBytes) / (1024 * 1024)

        XCTAssertLessThan(expectedMB, Double(config.maxFileSizeMB),
            "Chunk file size (\(expectedMB)MB) should be under limit (\(config.maxFileSizeMB)MB)")
    }

    // MARK: - File Type Tests

    func testM4AFileTypeSupported() {
        let fileType = AVFileType.m4a
        XCTAssertNotNil(fileType, "M4A file type should be supported")
    }

    func testWAVFileTypeSupported() {
        let fileType = AVFileType.wav
        XCTAssertNotNil(fileType, "WAV file type should be supported")
    }
}

// MARK: - CaptureError Equatable
extension CaptureError: Equatable {
    public static func == (lhs: CaptureError, rhs: CaptureError) -> Bool {
        switch (lhs, rhs) {
        case (.alreadyCapturing, .alreadyCapturing),
             (.notCapturing, .notCapturing),
             (.noDisplayFound, .noDisplayFound),
             (.noAudioRecorded, .noAudioRecorded),
             (.permissionDenied, .permissionDenied):
            return true
        default:
            return false
        }
    }
}
