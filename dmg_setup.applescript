
                tell application "Finder"
                    tell disk "Custom Cursors"
                        open
                        set current view of container window to icon view
                        set toolbar visible of container window to false
                        set statusbar visible of container window to false
                        set the bounds of container window to {100, 100, 700, 500}
                        set theViewOptions to the icon view options of container window
                        set arrangement of theViewOptions to not arranged
                        set icon size of theViewOptions to 80
                        set background picture of theViewOptions to file ".background:background.png"
                        set position of item "Custom Cursors.app" of container window to {150, 200}
                        set position of item "Applications" of container window to {450, 200}
                        update without registering applications
                        delay 5
                        close
                    end tell
                end tell
                