"""
Simple HTTP server to serve the test_page.html file.
This avoids CORS issues when opening HTML files directly.
Run this script and then open http://127.0.0.1:8080/test_page.html in your browser.
"""
import http.server
import socketserver
import webbrowser
import os

PORT = 8080

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # Add CORS headers
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

    def log_message(self, format, *args):
        # Suppress default logging
        pass

def main():
    # Change to project root (parent of scripts directory)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    os.chdir(project_root)
    
    with socketserver.TCPServer(("", PORT), MyHTTPRequestHandler) as httpd:
        url = f"http://127.0.0.1:{PORT}/test_page.html"
        print(f"Server started at http://127.0.0.1:{PORT}")
        print(f"Opening {url} in your browser...")
        print("Press Ctrl+C to stop the server")
        
        try:
            webbrowser.open(url)
        except:
            print(f"Could not open browser automatically. Please open {url} manually.")
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServer stopped.")

if __name__ == "__main__":
    main()

