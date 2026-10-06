import AVFoundation
import SwiftUI

@main
struct SwoleClickerApp: App {
    init() {
        // Game audio mixes with the player's own music and respects the silent switch.
        try? AVAudioSession.sharedInstance().setCategory(.ambient, options: [.mixWithOthers])
    }

    var body: some Scene {
        WindowGroup {
            GameView()
                .ignoresSafeArea()   // the page pads itself with env(safe-area-inset-*)
                .background(Color("LaunchBackground").ignoresSafeArea())
                .statusBarHidden(true)
                .persistentSystemOverlays(.hidden)
        }
    }
}
