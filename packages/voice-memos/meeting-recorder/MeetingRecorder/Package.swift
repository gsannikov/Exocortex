// swift-tools-version:5.9
import PackageDescription

let package = Package(
    name: "MeetingRecorder",
    platforms: [
        .macOS(.v13)  // ScreenCaptureKit requires macOS 12.3+, we use 13 for better APIs
    ],
    products: [
        .executable(name: "MeetingRecorder", targets: ["MeetingRecorderApp"]),
        .library(name: "MeetingRecorderLib", targets: ["MeetingRecorderLib"])
    ],
    dependencies: [],
    targets: [
        // Library target with all the core code (testable)
        .target(
            name: "MeetingRecorderLib",
            dependencies: [],
            path: "Sources/Lib"
        ),
        // Executable target (just the entry point)
        .executableTarget(
            name: "MeetingRecorderApp",
            dependencies: ["MeetingRecorderLib"],
            path: "Sources/App"
        ),
        // Test target
        .testTarget(
            name: "MeetingRecorderTests",
            dependencies: ["MeetingRecorderLib"],
            path: "Tests"
        )
    ]
)
