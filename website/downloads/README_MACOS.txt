
IMPORTANT INSTRUCTIONS FOR MACOS USERS
====================================

If you see a message that the app is damaged or can't be opened:

1. Open Terminal (Applications > Utilities > Terminal)
2. Run the following command (copy and paste the entire line):
   xattr -d com.apple.quarantine /path/to/CustomCursorApp.app
   
   (Replace /path/to/CustomCursorApp.app with the actual path to the app)

3. Try opening the app again

This is necessary because macOS has strict security measures for apps not from the App Store.
