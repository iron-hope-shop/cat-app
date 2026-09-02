import SwiftUI

@main
struct QuarryApp: App {
    var body: some Scene {
        WindowGroup {
            ContentView()
                .ignoresSafeArea()
                .background(Color(red: 0x10/255.0, green: 0x16/255.0, blue: 0x1c/255.0))
        }
    }
}
