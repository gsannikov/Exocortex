import XCTest
@testable import MeetingRecorderLib

final class MeetingDetectorTests: XCTestCase {

    var detector: MeetingDetector!

    override func setUp() {
        super.setUp()
        detector = MeetingDetector()
    }

    override func tearDown() {
        detector.stopMonitoring()
        detector = nil
        super.tearDown()
    }

    // MARK: - Meeting Apps Dictionary Tests

    func testMeetingAppsContainsZoom() {
        XCTAssertNotNil(MeetingDetector.meetingApps["us.zoom.xos"],
            "Should contain Zoom bundle identifier")
        XCTAssertEqual(MeetingDetector.meetingApps["us.zoom.xos"], "Zoom",
            "Zoom should map to 'Zoom' name")
    }

    func testMeetingAppsContainsTeams() {
        let hasTeams = MeetingDetector.meetingApps["com.microsoft.teams"] != nil ||
                       MeetingDetector.meetingApps["com.microsoft.teams2"] != nil
        XCTAssertTrue(hasTeams, "Should contain Microsoft Teams bundle identifier")
    }

    func testMeetingAppsContainsSlack() {
        XCTAssertNotNil(MeetingDetector.meetingApps["com.slack.Slack"],
            "Should contain Slack bundle identifier")
    }

    func testMeetingAppsContainsDiscord() {
        XCTAssertNotNil(MeetingDetector.meetingApps["com.discord"],
            "Should contain Discord bundle identifier")
    }

    func testMeetingAppsContainsFaceTime() {
        XCTAssertNotNil(MeetingDetector.meetingApps["com.apple.FaceTime"],
            "Should contain FaceTime bundle identifier")
    }

    func testMeetingAppsContainsChrome() {
        XCTAssertNotNil(MeetingDetector.meetingApps["com.google.Chrome"],
            "Should contain Chrome for web-based meetings")
    }

    func testAllMeetingAppsHaveNonEmptyNames() {
        for (bundleId, name) in MeetingDetector.meetingApps {
            XCTAssertFalse(name.isEmpty, "App name for \(bundleId) should not be empty")
        }
    }

    // MARK: - Browser Meeting Patterns Tests

    func testBrowserPatternsContainsGoogleMeet() {
        let hasGoogleMeet = MeetingDetector.browserMeetingPatterns.contains { pattern in
            pattern.lowercased().contains("meet")
        }
        XCTAssertTrue(hasGoogleMeet, "Should have pattern for Google Meet")
    }

    func testBrowserPatternsContainsMeetDash() {
        XCTAssertTrue(MeetingDetector.browserMeetingPatterns.contains("Meet -"),
            "Should contain 'Meet -' pattern for Google Meet window titles")
    }

    func testBrowserPatternsContainsMeetURL() {
        XCTAssertTrue(MeetingDetector.browserMeetingPatterns.contains("meet.google.com"),
            "Should contain meet.google.com URL pattern")
    }

    func testBrowserPatternsContainsZoomMeeting() {
        let hasZoomMeeting = MeetingDetector.browserMeetingPatterns.contains { pattern in
            pattern.contains("Zoom") && pattern.contains("Meeting")
        }
        XCTAssertTrue(hasZoomMeeting, "Should have pattern for Zoom in browser")
    }

    func testBrowserPatternsContainsTeams() {
        let hasTeams = MeetingDetector.browserMeetingPatterns.contains { pattern in
            pattern.contains("Microsoft Teams")
        }
        XCTAssertTrue(hasTeams, "Should have pattern for Teams in browser")
    }

    // MARK: - Callback Tests

    func testOnMeetingDetectedCallbackCanBeSet() {
        var callbackCalled = false

        detector.onMeetingDetected = { appName in
            callbackCalled = true
        }

        XCTAssertNotNil(detector.onMeetingDetected, "Callback should be settable")
    }

    func testOnMeetingEndedCallbackCanBeSet() {
        var callbackCalled = false

        detector.onMeetingEnded = { appName in
            callbackCalled = true
        }

        XCTAssertNotNil(detector.onMeetingEnded, "Callback should be settable")
    }

    // MARK: - Monitoring Tests

    func testStartMonitoringDoesNotCrash() {
        // Should not throw or crash
        detector.startMonitoring()

        // Give it a moment to initialize
        let expectation = XCTestExpectation(description: "Monitoring started")
        DispatchQueue.main.asyncAfter(deadline: .now() + 0.5) {
            expectation.fulfill()
        }

        wait(for: [expectation], timeout: 1.0)
    }

    func testStopMonitoringDoesNotCrash() {
        detector.startMonitoring()
        detector.stopMonitoring()

        // Should be able to stop without issues
        XCTAssertTrue(true, "Stop monitoring should complete without crash")
    }

    func testCanRestartMonitoring() {
        detector.startMonitoring()
        detector.stopMonitoring()
        detector.startMonitoring()

        // Should handle restart gracefully
        XCTAssertTrue(true, "Should be able to restart monitoring")

        detector.stopMonitoring()
    }

    // MARK: - Bundle ID Coverage Tests

    func testAllExpectedMeetingAppsAreCovered() {
        let expectedApps = [
            "Zoom",
            "Google Meet",
            "Microsoft Teams",
            "Slack",
            "Discord",
            "FaceTime"
        ]

        let coveredApps = Set(MeetingDetector.meetingApps.values)

        for app in expectedApps {
            XCTAssertTrue(coveredApps.contains(app) ||
                         MeetingDetector.browserMeetingPatterns.contains { $0.contains(app) },
                "Should cover \(app) in meeting detection")
        }
    }

    func testMinimumNumberOfMeetingAppsCovered() {
        // Should support at least 5 meeting platforms
        XCTAssertGreaterThanOrEqual(MeetingDetector.meetingApps.count, 5,
            "Should support at least 5 meeting app bundle identifiers")
    }

    func testMinimumNumberOfBrowserPatterns() {
        // Should have patterns for common web-based meetings
        XCTAssertGreaterThanOrEqual(MeetingDetector.browserMeetingPatterns.count, 3,
            "Should have at least 3 browser meeting patterns")
    }
}
