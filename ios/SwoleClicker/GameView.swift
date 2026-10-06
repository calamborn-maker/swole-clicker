import SwiftUI
import UIKit
import WebKit

/// Full-screen web view running the bundled game (Web/index.html), served from a private
/// `swole://` origin so localStorage saves persist like a normal website.
struct GameView: UIViewRepresentable {
    static let startURL = URL(string: "swole://game/index.html")!

    func makeCoordinator() -> Coordinator { Coordinator() }

    func makeUIView(context: Context) -> WKWebView {
        let config = WKWebViewConfiguration()
        config.setURLSchemeHandler(BundleSchemeHandler(), forURLScheme: "swole")
        config.websiteDataStore = .default()
        config.allowsInlineMediaPlayback = true
        config.mediaTypesRequiringUserActionForPlayback = []

        // Tell the game it's running in the app (no ads, native haptics + share sheet).
        let flag = WKUserScript(source: "window.__SWOLE_APP__={platform:'ios'};",
                                injectionTime: .atDocumentStart, forMainFrameOnly: true)
        config.userContentController.addUserScript(flag)
        let bridge = WeakScriptHandler(context.coordinator)
        config.userContentController.add(bridge, name: "haptic")
        config.userContentController.add(bridge, name: "share")
        #if DEBUG
        // Debug builds: forward page errors / console output to the Xcode console.
        let logJS = "['log','warn','error'].forEach(k=>{const o=console[k];console[k]=(...a)=>{try{webkit.messageHandlers.log.postMessage(k+': '+a.join(' '))}catch(e){};o.apply(console,a)}});window.addEventListener('error',e=>webkit.messageHandlers.log.postMessage('ERROR: '+e.message+' @'+e.lineno));"
        config.userContentController.addUserScript(WKUserScript(source: logJS, injectionTime: .atDocumentStart, forMainFrameOnly: true))
        config.userContentController.add(bridge, name: "log")
        #endif

        let web = WKWebView(frame: .zero, configuration: config)
        #if DEBUG
        web.isInspectable = true   // Safari ▸ Develop ▸ Simulator to inspect the game
        #endif
        web.isOpaque = false
        web.backgroundColor = UIColor(named: "LaunchBackground")
        web.scrollView.backgroundColor = web.backgroundColor
        web.scrollView.bounces = false
        web.scrollView.contentInsetAdjustmentBehavior = .never
        web.scrollView.delegate = context.coordinator          // blocks pinch-zoom
        web.navigationDelegate = context.coordinator
        web.uiDelegate = context.coordinator
        web.allowsLinkPreview = false
        context.coordinator.webView = web
        web.load(URLRequest(url: Self.startURL))
        return web
    }

    func updateUIView(_ uiView: WKWebView, context: Context) {}

    final class Coordinator: NSObject, WKNavigationDelegate, WKUIDelegate, WKScriptMessageHandler, UIScrollViewDelegate {
        weak var webView: WKWebView?
        private let light = UIImpactFeedbackGenerator(style: .light)
        private let medium = UIImpactFeedbackGenerator(style: .medium)
        private let heavy = UIImpactFeedbackGenerator(style: .heavy)

        // MARK: JS → native
        func userContentController(_ controller: WKUserContentController, didReceive message: WKScriptMessage) {
            switch message.name {
            case "haptic":
                let ms = (message.body as? NSNumber)?.intValue ?? 8
                (ms <= 10 ? light : ms <= 30 ? medium : heavy).impactOccurred()
            case "share":
                share(message.body as? [String: Any] ?? [:])
            case "log":
                NSLog("[game] %@", String(describing: message.body))
            default:
                break
            }
        }

        private func share(_ payload: [String: Any]) {
            guard let web = webView, let host = web.window?.rootViewController else { return }
            var items: [Any] = []
            if let text = payload["text"] as? String { items.append(text) }
            if let link = payload["url"] as? String, let url = URL(string: link) { items.append(url) }
            if let dataURL = payload["image"] as? String,
               let comma = dataURL.firstIndex(of: ","),
               let data = Data(base64Encoded: String(dataURL[dataURL.index(after: comma)...])),
               let image = UIImage(data: data) { items.append(image) }
            guard !items.isEmpty else { return }
            let sheet = UIActivityViewController(activityItems: items, applicationActivities: nil)
            sheet.popoverPresentationController?.sourceView = web
            sheet.popoverPresentationController?.sourceRect = CGRect(x: web.bounds.midX, y: web.bounds.midY, width: 1, height: 1)
            var top = host
            while let presented = top.presentedViewController { top = presented }
            top.present(sheet, animated: true)
        }

        // MARK: Navigation — the game stays on swole://, anything else opens in Safari
        func webView(_ webView: WKWebView, decidePolicyFor action: WKNavigationAction,
                     decisionHandler: @escaping (WKNavigationActionPolicy) -> Void) {
            guard let url = action.request.url else { return decisionHandler(.cancel) }
            if url.scheme == "swole" || url.scheme == "about" { return decisionHandler(.allow) }
            if ["http", "https", "mailto"].contains(url.scheme ?? "") { UIApplication.shared.open(url) }
            decisionHandler(.cancel)
        }

        func webView(_ webView: WKWebView, createWebViewWith configuration: WKWebViewConfiguration,
                     for action: WKNavigationAction, windowFeatures: WKWindowFeatures) -> WKWebView? {
            if let url = action.request.url { UIApplication.shared.open(url) }   // window.open / target=_blank
            return nil
        }

        func webView(_ webView: WKWebView, didFailProvisionalNavigation navigation: WKNavigation!, withError error: Error) {
            NSLog("[game] load failed: %@", error.localizedDescription)
        }

        func webView(_ webView: WKWebView, didFinish navigation: WKNavigation!) {
            NSLog("[game] loaded %@", webView.url?.absoluteString ?? "?")
        }

        func webViewWebContentProcessDidTerminate(_ webView: WKWebView) {
            webView.load(URLRequest(url: GameView.startURL))                     // recover if iOS kills the page
        }

        func viewForZooming(in scrollView: UIScrollView) -> UIView? { nil }
    }
}

/// Avoids the WKUserContentController → handler retain cycle.
private final class WeakScriptHandler: NSObject, WKScriptMessageHandler {
    weak var target: WKScriptMessageHandler?
    init(_ target: WKScriptMessageHandler) { self.target = target }
    func userContentController(_ controller: WKUserContentController, didReceive message: WKScriptMessage) {
        target?.userContentController(controller, didReceive: message)
    }
}

/// Serves files from the app bundle's Web/ folder for swole:// URLs.
private final class BundleSchemeHandler: NSObject, WKURLSchemeHandler {
    private let root = Bundle.main.url(forResource: "Web", withExtension: nil)

    func webView(_ webView: WKWebView, start task: WKURLSchemeTask) {
        guard let url = task.request.url, let root else {
            return task.didFailWithError(URLError(.fileDoesNotExist))
        }
        let path = url.path.isEmpty || url.path == "/" ? "index.html" : String(url.path.dropFirst())
        let file = root.appendingPathComponent(path).standardizedFileURL
        guard file.path.hasPrefix(root.standardizedFileURL.path), let data = try? Data(contentsOf: file) else {
            return task.didFailWithError(URLError(.fileDoesNotExist))
        }
        let types = ["html": "text/html; charset=utf-8", "js": "text/javascript", "css": "text/css",
                     "png": "image/png", "jpg": "image/jpeg", "svg": "image/svg+xml", "json": "application/json"]
        let mime = types[file.pathExtension.lowercased()] ?? "application/octet-stream"
        let response = HTTPURLResponse(url: url, statusCode: 200, httpVersion: "HTTP/1.1",
                                       headerFields: ["Content-Type": mime, "Content-Length": "\(data.count)"])!
        task.didReceive(response)
        task.didReceive(data)
        task.didFinish()
    }

    func webView(_ webView: WKWebView, stop task: WKURLSchemeTask) {}
}
