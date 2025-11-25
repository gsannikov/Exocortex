// swift-tools-version:5.9
import PackageDescription

let package = Package(
    name: "MeetingRecorder",
    platforms: [
        .macOS(.v13)  // ScreenCaptureKit requires macOS 12.3+, we use 13 for better APIs
    ],
    products: [
        .executable(name: "MeetingRecorder", targets: ["MeetingRecorder"])
    ],
    dependencies: [],
    targets: [
        .executableTarget(
            name: "MeetingRecorder",
            dependencies: [],
            path: "Sources"
        ),
        .testTarget(
            name: "MeetingRecorderTests",
            dependencies: [],
            path: "Tests"
        )
    ]
)
