#!/usr/bin/env python3
"""
Claude 3.7 generated
SICP Server Module

This module provides a simple HTTP server to serve the built files.
It can run alongside the watch module to provide a live preview.
"""

import os
import sys
import threading
import http.server
import socketserver
from pathlib import Path

# Default configuration
DEFAULT_PORT = 8001
DEFAULT_DIRECTORY = "docs"

class SICPHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    """Custom HTTP request handler for SICP notes."""

    def __init__(self, *args, directory=None, **kwargs):
        # The directory attribute needs to be set *after* the server is created in start_server()
        # We'll handle this in the do_GET method instead
        super().__init__(*args, **kwargs)

    def log_message(self, format, *args):
        """Override to provide more minimal logging."""
        try:
            # Check if this is a status code (could be a string or HTTPStatus enum)
            if args and (
                (isinstance(args[0], str) and args[0].startswith('2')) or
                (hasattr(args[0], 'value') and 200 <= args[0].value < 300)
            ):
                # Don't log successful requests
                return
        except Exception:
            # If there's any error in our logging logic, fall back to default
            pass

        # Use default logging for everything else
        super().log_message(format, *args)

    def do_GET(self):
        """Handle GET requests with on-demand Racket file processing."""
        # Ensure we're using the correct directory
        if hasattr(self.server, 'root_dir'):
            self.directory = self.server.root_dir

        path = self.translate_path(self.path)

        # If the requested file is HTML and exists, check for missing .out files
        if path.endswith('.html') and os.path.exists(path):
            self._ensure_racket_outputs_exist(path)

        # Continue with normal request handling
        return super().do_GET()

    def _ensure_racket_outputs_exist(self, html_path):
        """Check and generate any missing .out files referenced in the HTML."""
        try:
            # Read the HTML file
            with open(html_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Import the build module from parent directory
            sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            import build

            # Map from docs/ to src/ paths
            src_dir = build.SRC_DIR
            out_dir = build.OUT_DIR

            # Look for references to .rkt files
            # Pattern could be src="some/path/file.rkt" or href="some/path/file.rkt"
            import re
            rkt_refs = re.findall(r'(?:src|href)=["\']([^"\']+\.rkt)["\']', content)

            # For each .rkt file, check if the .out exists
            for rkt_ref in rkt_refs:
                # Get full path from the reference (which could be relative)
                html_dir = os.path.dirname(html_path)
                rkt_path_in_docs = os.path.normpath(os.path.join(html_dir, rkt_ref))

                # Convert from docs/ path to src/ path
                if rkt_path_in_docs.startswith(out_dir):
                    rel_path = os.path.relpath(rkt_path_in_docs, out_dir)
                    rkt_path_in_src = os.path.join(src_dir, rel_path)
                else:
                    # If it's not in docs directory, try to guess the src path
                    rkt_path_in_src = os.path.join(src_dir, rkt_ref)

                # Check if the corresponding .out file exists
                out_path = os.path.splitext(rkt_path_in_src)[0] + ".out"
                if not os.path.exists(out_path) and os.path.exists(rkt_path_in_src):
                    print(f"\n🔄 Auto-generating missing output for {rkt_path_in_src}")

                    # Run the racket file
                    import subprocess
                    try:
                        result = subprocess.run(
                            ['racket', rkt_path_in_src],
                            capture_output=True,
                            text=True,
                            check=False
                        )

                        # Write output to .out file
                        with open(out_path, 'w', encoding='utf-8') as f:
                            if result.returncode != 0:
                                f.write(result.stdout)
                                f.write(f"\nError (exit code {result.returncode}):\n{result.stderr}")
                                print(f"  ❌ Error running {rkt_path_in_src}")
                            else:
                                f.write(result.stdout)
                                print(f"  ✅ Successfully generated {out_path}")

                        # Copy the output file to docs directory
                        out_path_in_docs = os.path.splitext(rkt_path_in_docs)[0] + ".out"
                        os.makedirs(os.path.dirname(out_path_in_docs), exist_ok=True)
                        import shutil
                        shutil.copy2(out_path, out_path_in_docs)
                    except Exception as e:
                        print(f"  ❌ Error: {str(e)}")
        except Exception as e:
            # Just log the error but don't block the request
            print(f"Error checking for Racket dependencies: {str(e)}")


class ServerThread(threading.Thread):
    """Thread that runs the HTTP server."""

    def __init__(self, root_dir=DEFAULT_DIRECTORY, port=DEFAULT_PORT):
        threading.Thread.__init__(self, daemon=True)
        self.root_dir = root_dir
        self.port = port
        self.server = None
        self.started_event = threading.Event()

    def run(self):
        """Run the server in a separate thread."""
        try:
            # Create a handler class with directory set to our root_dir
            handler = http.server.SimpleHTTPRequestHandler

            # Create a custom request handler class that includes our enhanced functionality
            class CustomHandler(SICPHTTPRequestHandler):
                # This ensures the directory is correctly set
                directory = self.root_dir

            # Create and configure the server
            self.server = socketserver.TCPServer(("", self.port), CustomHandler)
            self.server.root_dir = self.root_dir

            # Signal that we've started
            self.started_event.set()

            # Print server info
            print(f"\n🌐 Server running at http://localhost:{self.port}")
            print(f"📁 Serving files from: {os.path.abspath(self.root_dir)}")
            print("⌨️  Press Ctrl+C to stop the server and watcher\n")

            # Start serving
            self.server.serve_forever()
        except OSError as e:
            if e.errno == 98 or e.errno == 48:  # Address already in use (Linux uses 98, macOS uses 48)
                print(f"\n❌ Error: Port {self.port} is already in use.")
                print(f"   Try a different port with: make watch PORT={self.port+1}")
                print(f"   Or kill the existing process with: make kill-server PORT={self.port}")
            else:
                print(f"\n❌ Error starting server: {str(e)}")
            self.started_event.set()  # Signal that we tried to start
        except Exception as e:
            print(f"\n❌ Error starting server: {str(e)}")
            self.started_event.set()  # Signal that we tried to start

    def stop(self):
        """Stop the server."""
        if self.server:
            self.server.shutdown()
            self.server.server_close()


def start_server(root_dir=DEFAULT_DIRECTORY, port=DEFAULT_PORT):
    """Start the server in a background thread and return the thread."""
    # Ensure the root_dir exists
    if not os.path.isdir(root_dir):
        os.makedirs(root_dir, exist_ok=True)
        print(f"Created directory: {root_dir}")

    # Convert to absolute path to avoid issues
    root_dir = os.path.abspath(root_dir)

    server_thread = ServerThread(root_dir, port)
    server_thread.start()

    # Wait for the server to start or fail
    server_thread.started_event.wait()

    return server_thread


if __name__ == "__main__":
    # Handle command-line arguments if run directly
    import argparse

    parser = argparse.ArgumentParser(description="SICP HTTP Server")
    parser.add_argument("--port", type=int, default=DEFAULT_PORT,
                        help=f"Port to serve on (default: {DEFAULT_PORT})")
    parser.add_argument("--dir", type=str, default=DEFAULT_DIRECTORY,
                        help=f"Directory to serve (default: {DEFAULT_DIRECTORY})")

    args = parser.parse_args()

    try:
        thread = start_server(args.dir, args.port)
        # Keep the main thread running
        while True:
            import time
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Server stopped.")
