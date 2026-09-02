import UIKit
import WebKit
import AVFoundation

final class CatGameViewController: UIViewController, WKNavigationDelegate, WKUIDelegate, UIScrollViewDelegate {
    private var webView: WKWebView!

    // Cat-proofing 1: Defer system gestures on all edges so accidental paw swipes don't exit the app
    override var preferredScreenEdgesDeferringSystemGestures: UIRectEdge {
        return .all
    }

    // Cat-proofing 2: Auto-hide the iPad home indicator bar
    override var prefersHomeIndicatorAutoHidden: Bool {
        return true
    }

    // Cat-proofing 3: Hide the status bar completely
    override var prefersStatusBarHidden: Bool {
        return true
    }

    override func viewDidLoad() {
        super.viewDidLoad()
        view.backgroundColor = UIColor(red: 0x10/255.0, green: 0x16/255.0, blue: 0x1c/255.0, alpha: 1.0)

        setupAudioSession()
        setupWebView()
        loadGame()
    }

    private func setupAudioSession() {
        do {
            let session = AVAudioSession.sharedInstance()
            try session.setCategory(.ambient, mode: .default, options: [.mixWithOthers])
            try session.setActive(true)
        } catch {
            print("Audio session setup failed: \(error.localizedDescription)")
        }
    }

    private func setupWebView() {
        let configuration = WKWebViewConfiguration()
        configuration.allowsInlineMediaPlayback = true
        configuration.mediaTypesRequiringUserActionForPlayback = []
        configuration.preferences.setValue(true, forKey: "allowFileAccessFromFileURLs")

        // Disable callout, selection, and magnifier in WKWebView
        let css = """
        * { -webkit-touch-callout: none !important; -webkit-user-select: none !important; user-select: none !important; }
        body { -webkit-text-size-adjust: none !important; }
        """
        let userScript = WKUserScript(
            source: "const style = document.createElement('style'); style.textContent = '\(css)'; document.head.appendChild(style);",
            injectionTime: .atDocumentEnd,
            forMainFrameOnly: true
        )
        configuration.userContentController.addUserScript(userScript)

        webView = WKWebView(frame: view.bounds, configuration: configuration)
        webView.autoresizingMask = [.flexibleWidth, .flexibleHeight]
        webView.navigationDelegate = self
        webView.uiDelegate = self
        webView.isOpaque = false
        webView.backgroundColor = UIColor(red: 0x10/255.0, green: 0x16/255.0, blue: 0x1c/255.0, alpha: 1.0)
        webView.isMultipleTouchEnabled = true

        // Home/setup must scroll; play is position:fixed and overflow-hidden so paws cannot drag the field
        let scrollView = webView.scrollView
        scrollView.isScrollEnabled = true
        scrollView.bounces = false
        scrollView.bouncesZoom = false
        scrollView.contentInsetAdjustmentBehavior = .never
        scrollView.showsVerticalScrollIndicator = false
        scrollView.showsHorizontalScrollIndicator = false
        scrollView.isMultipleTouchEnabled = true
        scrollView.delegate = self

        if #available(iOS 16.4, *) {
            webView.isInspectable = true
        }

        view.addSubview(webView)
    }

    private func loadGame() {
        let candidates = [
            Bundle.main.url(forResource: "index", withExtension: "html", subdirectory: "www"),
            Bundle.main.url(forResource: "quarry", withExtension: "html"),
            Bundle.main.url(forResource: "index", withExtension: "html")
        ]

        guard let gameURL = candidates.compactMap({ $0 }).first else {
            print("Error: Could not find quarry HTML file in app bundle.")
            NSLog("Error: Could not find quarry HTML file in app bundle.")
            return
        }

        webView.loadFileURL(gameURL, allowingReadAccessTo: Bundle.main.bundleURL)
    }

    // UIScrollViewDelegate: Prevent zooming
    func viewForZooming(in scrollView: UIScrollView) -> UIView? {
        return nil
    }

    override func viewDidLayoutSubviews() {
        super.viewDidLayoutSubviews()
        setNeedsUpdateOfScreenEdgesDeferringSystemGestures()
        setNeedsUpdateOfHomeIndicatorAutoHidden()
    }
}
