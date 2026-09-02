import SwiftUI

struct ContentView: UIViewControllerRepresentable {
    func makeUIViewController(context: Context) -> CatGameViewController {
        return CatGameViewController()
    }

    func updateUIViewController(_ uiViewController: CatGameViewController, context: Context) {
        // No dynamic SwiftUI state updates needed; game runs in WKWebView
    }
}

#Preview {
    ContentView()
}
