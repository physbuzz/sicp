#!/usr/bin/env python3
"""
Claude 3.7 generated
SICP Server Module

This module provides a simple HTTP server to serve the built files.
It can run alongside the watch module to provide a live preview.
"""

import os
import sys
import time
import threading
import http.server
import socketserver
import socket
from pathlib import Path

# Default configuration
DEFAULT_PORT = 8000
DEFAULT_DIRECTORY = "docs"

# Allow socket reuse
socketserver.TCPServer.allow_reuse_address = True

class SICPHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    """Custom HTTP request handler for SICP notes."""

    def log_message(self, format, *args):
        """Override to provide more minimal logging."""
        try:
            # Check if this is a success status code
            if args and (
                (isinstance(args[0], str) and args[0].startswith('2')) or
                (hasattr(args[0], 'value') and 200 <= args[0].value < 300)
            ):
                # Don't log successful requests
                return
        except Exception:
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
                    print(f"\nAuto-generating missing output for {rkt_path_in_src}")

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
                                print(f"  Error running {rkt_path_in_src}")
                            else:
                                f.write(result.stdout)
                                print(f"  Successfully generated {out_path}")

                        # Copy the output file to docs directory
                        out_path_in_docs = os.path.splitext(rkt_path_in_docs)[0] + ".out"
                        os.makedirs(os.path.dirname(out_path_in_docs), exist_ok=True)
                        import shutil
                        shutil.copy2(out_path, out_path_in_docs)
                    except Exception as e:
                        print(f"  Error: {str(e)}")
        except Exception as e:
            # Just log the error but don't block the request
            print(f"Error checking for Racket dependencies: {str(e)}")


class ReuseAddressServer(socketserver.TCPServer):
    """TCPServer with address reuse enabled."""

    def __init__(self, *args, **kwargs):
        self.allow_reuse_address = True
        super().__init__(*args, **kwargs)

    def server_close(self):
        """Override to ensure socket is properly closed."""
        # First call the parent class method
        super().server_close()

        # Try to explicitly close the socket
        if hasattr(self, 'socket'):
            try:
                self.socket.close()
            except:
                pass


class ServerThread(threading.Thread):
    """Thread that runs the HTTP server."""

    def __init__(self, root_dir=DEFAULT_DIRECTORY, port=DEFAULT_PORT):
        threading.Thread.__init__(self, daemon=True)
        self.root_dir = root_dir
        self.port = port
        self.server = None
        self.started_event = threading.Event()
        self.shutdown_event = threading.Event()

        # Try to find an available port
        self.port = self._find_available_port(port)

    def _find_available_port(self, preferred_port):
        """Try to find an available port, starting with the preferred one."""
        port = preferred_port
        max_attempts = 10

        # Create a socket to test port availability
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Set socket option to allow port reuse
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        for attempt in range(max_attempts):
            try:
                s.bind(('', port))
                s.close()
                return port
            except OSError:
                port = preferred_port + attempt + 1

        # If we get here, we couldn't find an available port
        s.close()
        return preferred_port  # Just return the original port and let it fail normally

    def run(self):
        """Run the server in a separate thread."""
        try:
            # Create a custom request handler class
            class CustomHandler(SICPHTTPRequestHandler):
                directory = self.root_dir

            # Try to create and configure the server
            self.server = ReuseAddressServer(("", self.port), CustomHandler)
            self.server.root_dir = self.root_dir
            self.server.timeout = 1.0  # Set a timeout so we can check for shutdown

            # Signal that we've started
            self.started_event.set()

            # Print server info
            print(f"\nServer running at http://localhost:{self.port}")
            print(f"Serving files from: {os.path.abspath(self.root_dir)}")
            print("Press Ctrl+C to stop watching and server\n")

            # Start serving
            while not self.shutdown_event.is_set():
                self.server.handle_request()

        except OSError as e:
            if e.errno == 98 or e.errno == 48:  # Address already in use
                print(f"\nError: Port {self.port} is already in use.")
                print(f"Try a different port with the --port option")

                # Attempt to find a process using the port
                self._show_process_using_port(self.port)
            else:
                print(f"\nError starting server: {str(e)}")
            self.started_event.set()  # Signal that we tried to start

        except Exception as e:
            print(f"\nError starting server: {str(e)}")
            self.started_event.set()  # Signal that we tried to start

    def _show_process_using_port(self, port):
        """Try to find which process is using the port."""
        try:
            if sys.platform.startswith('linux'):
                import subprocess
                result = subprocess.run(
                    ['lsof', '-i', f':{port}'],
                    capture_output=True,
                    text=True,
                    check=False
                )
                if result.stdout:
                    print("\nProcess using this port:")
                    print(result.stdout)
                    print(f"You can kill it with: kill -9 <PID>")
            elif sys.platform == 'darwin':  # macOS
                import subprocess
                result = subprocess.run(
                    ['lsof', '-i', f':{port}'],
                    capture_output=True,
                    text=True,
                    check=False
                )
                if result.stdout:
                    print("\nProcess using this port:")
                    print(result.stdout)
                    print(f"You can kill it with: kill -9 <PID>")
            elif sys.platform == 'win32':
                import subprocess
                result = subprocess.run(
                    ['netstat', '-ano', '|', 'findstr', f':{port}'],
                    capture_output=True,
                    text=True,
                    shell=True,
                    check=False
                )
                if result.stdout:
                    print("\nProcess using this port:")
                    print(result.stdout)
                    print(f"You can kill it with: taskkill /F /PID <PID>")
        except Exception:
            pass

    def stop(self):
        """Stop the server."""
        if self.server:
            self.shutdown_event.set()

            # Set a very short timeout to unblock handle_request
            if hasattr(self.server, 'timeout'):
                self.server.timeout = 0.1

            try:
                # Try to send a dummy request to unblock the server
                self._send_dummy_request()

                # Shutdown and close the server
                self.server.server_close()

                # Ensure socket is closed
                if hasattr(self.server, 'socket'):
                    self.server.socket.close()

                print("Server stopped.")
            except Exception as e:
                print(f"Error stopping server: {str(e)}")

    def _send_dummy_request(self):
        """Send a dummy request to unblock the server."""
        try:
            # Try to connect to the server to unblock it
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.5)
            try:
                s.connect(('localhost', self.port))
                s.send(b'GET / HTTP/1.1\r\nHost: localhost\r\n\r\n')
            except:
                pass
            finally:
                s.close()
        except:
            pass


def start_server(root_dir=DEFAULT_DIRECTORY, port=DEFAULT_PORT):
    """Start the server in a background thread and return the thread."""
    # Set up signal handling in the main thread
    import signal

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

    # Set up keyboard interrupt handler in the main thread
    original_handler = signal.getsignal(signal.SIGINT)

    def signal_handler(sig, frame):
        # Restore the original handler
        signal.signal(signal.SIGINT, original_handler)

        # Stop the server
        if server_thread.is_alive():
            server_thread.stop()
            server_thread.join(timeout=1.0)

        # Let the original handler run if needed
        if callable(original_handler):
            original_handler(sig, frame)

    # Register our signal handler
    signal.signal(signal.SIGINT, signal_handler)

    return server_thread


def cleanup_ports():
    """Try to clean up any lingering connections on the server ports."""
    import subprocess
    import sys
    import signal

    if sys.platform == 'win32':
        return  # Not implemented for Windows yet

    try:
        # Look for Python processes listening on ports
        result = subprocess.run(
            ['lsof', '-i', ':8000-8100', '-a', '-c', 'python'],
            capture_output=True,
            text=True,
            check=False
        )

        if result.stdout:
            print("Found Python processes potentially holding onto ports:")
            print(result.stdout)

            # Extract PIDs
            import re
            pids = re.findall(r'python\s+(\d+)', result.stdout)

            if pids:
                print(f"Attempting to release ports by sending SIGTERM to {len(pids)} processes...")
                for pid in pids:
                    try:
                        os.kill(int(pid), signal.SIGTERM)
                        print(f"Sent SIGTERM to process {pid}")
                    except Exception as e:
                        print(f"Error terminating process {pid}: {str(e)}")

                # Give processes time to terminate
                time.sleep(0.5)
                print("Port cleanup completed.")
    except Exception as e:
        print(f"Error during port cleanup: {str(e)}")


if __name__ == "__main__":
    # Handle command-line arguments if run directly
    import argparse
    import signal

    parser = argparse.ArgumentParser(description="SICP HTTP Server")
    parser.add_argument("--port", type=int, default=DEFAULT_PORT,
                        help=f"Port to serve on (default: {DEFAULT_PORT})")
    parser.add_argument("--dir", type=str, default=DEFAULT_DIRECTORY,
                        help=f"Directory to serve (default: {DEFAULT_DIRECTORY})")
    parser.add_argument("--cleanup", action="store_true",
                        help="Clean up any lingering connections on server ports")

    args = parser.parse_args()

    if args.cleanup:
        cleanup_ports()
        sys.exit(0)

    try:
        thread = start_server(args.dir, args.port)
        # Keep the main thread running
        while thread.is_alive():
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nServer stopped.")
