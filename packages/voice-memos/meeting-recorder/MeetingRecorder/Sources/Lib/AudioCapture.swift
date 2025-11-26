import AVFoundation
import Foundation
import ScreenCaptureKit

/// Captures audio from meeting applications using ScreenCaptureKit
/// Note: @unchecked Sendable because this class manages its own thread safety
/// through DispatchQueue.main for UI updates and serial access patterns
public final class AudioCapture: NSObject, @unchecked Sendable {
    private var stream: SCStream?
    private var audioWriter: AVAssetWriter?
    private var audioInput: AVAssetWriterInput?
    private var currentFileName: String?
    private var currentFilePath: URL?
    private var isCapturing = false
    private var chunkIndex = 0
    private var chunkStartTime: Date?
    private var recordedChunks: [URL] = []

    // For chunking long recordings
    private var chunkTimer: Timer?
    private let chunkDurationSeconds: TimeInterval

    public override init() {
        self.chunkDurationSeconds = TimeInterval(Config.shared.chunkDurationMinutes * 60)
        super.init()
    }

    /// Start capturing audio from the system or a specific app
    public func startCapture(forApp appName: String, completion: @escaping (Error?) -> Void) {
        guard !isCapturing else {
            completion(CaptureError.alreadyCapturing)
            return
        }

        Task {
            do {
                // Get available content to capture
                let content = try await SCShareableContent.current

                // Find the target application if specified
                var filter: SCContentFilter

                if appName != "Manual Recording" {
                    // Try to find the specific app
                    if let targetApp = content.applications.first(where: { app in
                        app.applicationName.contains(appName) ||
                        MeetingDetector.meetingApps.values.contains(where: { $0 == appName && app.applicationName.contains($0) })
                    }) {
                        // Capture only this app's audio
                        // Note: SCContentFilter for app-only audio requires including at least one window
                        if let window = content.windows.first(where: { $0.owningApplication?.processID == targetApp.processID }) {
                            filter = SCContentFilter(desktopIndependentWindow: window)
                        } else {
                            // Fall back to display capture
                            guard let display = content.displays.first else {
                                throw CaptureError.noDisplayFound
                            }
                            filter = SCContentFilter(display: display, excludingApplications: [], exceptingWindows: [])
                        }
                    } else {
                        // App not found, capture all audio
                        guard let display = content.displays.first else {
                            throw CaptureError.noDisplayFound
                        }
                        filter = SCContentFilter(display: display, excludingApplications: [], exceptingWindows: [])
                    }
                } else {
                    // Manual recording - capture all system audio
                    guard let display = content.displays.first else {
                        throw CaptureError.noDisplayFound
                    }
                    filter = SCContentFilter(display: display, excludingApplications: [], exceptingWindows: [])
                }

                // Configure stream for audio capture
                let config = SCStreamConfiguration()
                config.capturesAudio = true
                config.sampleRate = Config.shared.sampleRate
                config.channelCount = Config.shared.channels

                // Minimize video capture (we only want audio)
                config.width = 2
                config.height = 2
                config.minimumFrameInterval = CMTime(value: 1, timescale: 1) // 1 fps minimum
                config.showsCursor = false

                // Create and start the stream
                let stream = SCStream(filter: filter, configuration: config, delegate: self)

                // Add stream output for audio
                try stream.addStreamOutput(self, type: .audio, sampleHandlerQueue: .global(qos: .userInteractive))

                // Setup first chunk's audio writer
                try setupAudioWriter(appName: appName)

                // Start the stream
                try await stream.startCapture()

                self.stream = stream
                self.isCapturing = true
                self.chunkStartTime = Date()

                // Setup chunk timer if auto-chunking is enabled
                if Config.shared.autoChunk {
                    DispatchQueue.main.async {
                        self.chunkTimer = Timer.scheduledTimer(withTimeInterval: self.chunkDurationSeconds, repeats: true) { [weak self] _ in
                            self?.rotateChunk()
                        }
                    }
                }

                DispatchQueue.main.async {
                    completion(nil)
                }

            } catch {
                DispatchQueue.main.async {
                    completion(error)
                }
            }
        }
    }

    /// Stop capturing and finalize the recording
    public func stopCapture(completion: @escaping (URL?, Error?) -> Void) {
        guard isCapturing else {
            completion(nil, CaptureError.notCapturing)
            return
        }

        isCapturing = false
        chunkTimer?.invalidate()
        chunkTimer = nil

        Task {
            do {
                // Stop the stream
                try await stream?.stopCapture()
                stream = nil

                // Finalize current chunk
                await finalizeAudioWriter()

                // Return the file URL(s)
                DispatchQueue.main.async {
                    if self.recordedChunks.count == 1 {
                        // Single file
                        completion(self.recordedChunks.first, nil)
                    } else if self.recordedChunks.count > 1 {
                        // Multiple chunks - return first, but all are saved
                        // The voice-memos skill will process all files in the folder
                        completion(self.recordedChunks.first, nil)
                        print("Recording saved as \(self.recordedChunks.count) chunks")
                    } else {
                        completion(nil, CaptureError.noAudioRecorded)
                    }
                    self.recordedChunks = []
                    self.chunkIndex = 0
                }

            } catch {
                DispatchQueue.main.async {
                    completion(nil, error)
                }
            }
        }
    }

    // MARK: - Private Methods

    private func setupAudioWriter(appName: String) throws {
        let fileName: String
        if chunkIndex == 0 {
            fileName = Config.shared.generateFileName(forApp: appName)
            currentFileName = fileName
        } else {
            // For chunks, append chunk number
            let baseName = currentFileName?.replacingOccurrences(of: ".\(Config.shared.audioFormat)", with: "") ?? "recording"
            fileName = "\(baseName)_chunk\(chunkIndex).\(Config.shared.audioFormat)"
        }

        let filePath = URL(fileURLWithPath: Config.shared.fullPath(forFileName: fileName))
        currentFilePath = filePath

        // Remove existing file if any
        try? FileManager.default.removeItem(at: filePath)

        // Create asset writer
        let fileType: AVFileType = Config.shared.audioFormat == "m4a" ? .m4a : .wav

        audioWriter = try AVAssetWriter(outputURL: filePath, fileType: fileType)

        // Configure audio settings for speech-optimized compression
        let audioSettings: [String: Any] = [
            AVFormatIDKey: kAudioFormatMPEG4AAC,
            AVSampleRateKey: Config.shared.sampleRate,
            AVNumberOfChannelsKey: Config.shared.channels,
            AVEncoderBitRateKey: Config.shared.audioBitrate
        ]

        audioInput = AVAssetWriterInput(mediaType: .audio, outputSettings: audioSettings)
        audioInput?.expectsMediaDataInRealTime = true

        if let audioInput = audioInput, audioWriter?.canAdd(audioInput) == true {
            audioWriter?.add(audioInput)
        }

        audioWriter?.startWriting()
        audioWriter?.startSession(atSourceTime: .zero)

        print("Audio writer setup for: \(filePath.path)")
    }

    private func rotateChunk() {
        guard isCapturing else { return }

        print("Rotating to new chunk...")

        Task {
            // Finalize current chunk
            await finalizeAudioWriter()

            // Start new chunk
            chunkIndex += 1
            try? setupAudioWriter(appName: "")
            chunkStartTime = Date()
        }
    }

    private func finalizeAudioWriter() async {
        guard let writer = audioWriter, let input = audioInput else { return }

        input.markAsFinished()

        await withCheckedContinuation { continuation in
            writer.finishWriting {
                if let path = self.currentFilePath {
                    self.recordedChunks.append(path)
                    print("Chunk saved: \(path.lastPathComponent)")
                }
                continuation.resume()
            }
        }

        audioWriter = nil
        audioInput = nil
    }
}

// MARK: - SCStreamDelegate
extension AudioCapture: SCStreamDelegate {
    public func stream(_ stream: SCStream, didStopWithError error: Error) {
        print("Stream stopped with error: \(error)")
        isCapturing = false
    }
}

// MARK: - SCStreamOutput
extension AudioCapture: SCStreamOutput {
    public func stream(_ stream: SCStream, didOutputSampleBuffer sampleBuffer: CMSampleBuffer, of type: SCStreamOutputType) {
        guard type == .audio, isCapturing else { return }

        // Write audio sample to file
        if let input = audioInput, input.isReadyForMoreMediaData {
            input.append(sampleBuffer)
        }
    }
}

// MARK: - Errors
public enum CaptureError: LocalizedError {
    case alreadyCapturing
    case notCapturing
    case noDisplayFound
    case noAudioRecorded
    case permissionDenied

    public var errorDescription: String? {
        switch self {
        case .alreadyCapturing:
            return "Already capturing audio"
        case .notCapturing:
            return "Not currently capturing"
        case .noDisplayFound:
            return "No display found for capture"
        case .noAudioRecorded:
            return "No audio was recorded"
        case .permissionDenied:
            return "Screen recording permission denied. Please enable in System Preferences > Privacy & Security > Screen Recording"
        }
    }
}
