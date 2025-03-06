#!/usr/bin/env python3
"""
Simple HTTP server to preview the website locally
"""

import http.server
import socketserver
import os
import webbrowser
from pathlib import Path

# Configuration
PORT = 8000
DIRECTORY = "website"

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

def main():
    # Change to the script's directory
    os.chdir(Path(__file__).parent)
    
    # Ensure the website directory exists
    if not os.path.isdir(DIRECTORY):
        print(f"Error: '{DIRECTORY}' directory not found")
        return 1
    
    print(f"Starting server at http://localhost:{PORT}")
    print(f"Serving files from: {DIRECTORY}")
    print("Press Ctrl+C to stop the server")
    
    # Open the browser
    webbrowser.open(f"http://localhost:{PORT}")
    
    # Start the server
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServer stopped")
    
    return 0

if __name__ == "__main__":
    exit(main())
