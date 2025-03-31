#!/usr/bin/env python3

"""
Generated using Claude 3.7
SICP Watch Module - Fixed Version
Watch for file changes and trigger appropriate rebuilds.
"""

import os
import sys
import time
import shutil
import subprocess
import signal
from pathlib import Path
try:
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler
except ImportError:
    print("Error: watchdog package is not installed.")
    print("Please install it with: pip install watchdog")
    sys.exit(1)

# Import build script functions
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build

# Try to import the server module
try:
    import server
except ImportError:
    print("Warning: server.py module not found. Live preview will not be available.")
    server = None

class ChangeHandler(FileSystemEventHandler):
    """Handles file system change events and triggers appropriate rebuilds."""

    def __init__(self, src_dir, out_dir, verbose=True):
        self.src_dir = src_dir
        self.out_dir = out_dir
        self.verbose = verbose
        # Track when we last processed an event for each file to avoid duplicates
        self.last_processed = {}
        # Cooldown period in seconds to avoid multiple rebuilds for the same file
        self.cooldown = 1.0
        # Set to track which files we've already rebuilt in this cycle
        self.rebuilt_files = set()
        # Timer for batch processing
        self.last_batch_time = time.time()
        self.batch_cooldown = 2.0
        self.pending_changes = set()

    def _should_rebuild_racket_output(self, rkt_file):
        """Check if a Racket file's output needs to be rebuilt based on timestamps."""
        out_file = os.path.splitext(rkt_file)[0] + ".out"

        # If .out file doesn't exist, definitely rebuild
        if not os.path.exists(out_file):
            print(f"Missing output file for {rkt_file}, will rebuild")
            return True

        # Check if .rkt file is newer than .out file
        rkt_mtime = os.path.getmtime(rkt_file)
        out_mtime = os.path.getmtime(out_file)

        if rkt_mtime > out_mtime:
            if self.verbose:
                print(f"Racket file {os.path.basename(rkt_file)} is newer than its output, rebuilding...")
            return True

        return False

    def on_modified(self, event):
        """Handle file modification events."""
        if event.is_directory:
            return

        # Get the file path
        file_path = event.src_path

        # Skip files that are not processable or in wrong directory
        if not build.should_process_file(file_path):
            return
        if '/docs/' in file_path or '\\docs\\' in file_path:
            return
        if file_path.endswith('.out'):
            return

        # Check if we're in the cooldown period for this file
        current_time = time.time()
        if file_path in self.last_processed:
            if current_time - self.last_processed[file_path] < self.cooldown:
                return

        # Update the last processed time
        self.last_processed[file_path] = current_time

        # Add to pending changes
        self.pending_changes.add(file_path)

        # Check if it's time to process batch
        if current_time - self.last_batch_time > self.batch_cooldown:
            self._process_batch()

    def on_created(self, event):
        """Handle file creation events."""
        if not event.is_directory:
            self.on_modified(event)

    def _process_batch(self):
        """Process all pending file changes as a batch."""
        if not self.pending_changes:
            return

        if self.verbose:
            print(f"\nProcessing {len(self.pending_changes)} pending changes...")

        # Group changes by file type
        rkt_files = []
        md_files = []
        build_system_files = []
        other_files = []

        for file_path in self.pending_changes:
            _, ext = os.path.splitext(file_path)
            file_name = os.path.basename(file_path)

            if ext.lower() == '.rkt':
                rkt_files.append(file_path)
            elif ext.lower() == '.md':
                md_files.append(file_path)
            elif file_name in ['composable_markdown.py', 'md2html.py']:
                build_system_files.append(file_path)
            else:
                other_files.append(file_path)

        # Process build system files first
        if build_system_files:
            if self.verbose:
                print("Build system files changed. Rebuilding all markdown files...")
            self._rebuild_all_markdown()
        else:
            # Process Racket files first
            if rkt_files:
                for rkt_file in rkt_files:
                    self._handle_racket_change(rkt_file)

            # Then process markdown files
            if md_files:
                for md_file in md_files:
                    self._handle_markdown_change(md_file)

            # Process other files
            if other_files:
                for other_file in other_files:
                    self._handle_other_file(other_file)

        # Clear pending changes
        self.pending_changes.clear()

        # Reset batch timer
        self.last_batch_time = time.time()

    def _handle_racket_change(self, file_path):
        """Handle changes to Racket files."""
        if self.verbose:
            print(f"Running Racket file: {os.path.basename(file_path)}")

        # Check if we actually need to rebuild this file
        if not self._should_rebuild_racket_output(file_path):
            if self.verbose:
                print(f"  Skipping {os.path.basename(file_path)} - output is up to date")
            return

        # Run the Racket file
        try:
            # Create output directory if it doesn't exist
            out_file = os.path.splitext(file_path)[0] + ".out"
            os.makedirs(os.path.dirname(out_file), exist_ok=True)

            result = subprocess.run(
                ['racket', file_path],
                capture_output=True,
                text=True,
                check=False
            )

            # Write output to .out file
            with open(out_file, 'w', encoding='utf-8') as f:
                f.write(result.stdout)
                if result.returncode != 0:
                    f.write(f"\nError (exit code {result.returncode}):\n{result.stderr}")
                    print(f"  Error running {os.path.basename(file_path)}")
                else:
                    if self.verbose:
                        print(f"  Successfully ran {os.path.basename(file_path)}")

            # Find which markdown files reference this file
            self._update_dependent_markdown(file_path)

            # Copy the updated Racket file and its output to docs
            self._copy_file_to_docs(file_path)
            self._copy_file_to_docs(out_file)

        except Exception as e:
            print(f"  Error: {str(e)}")
            # Create an error output file
            try:
                out_file = os.path.splitext(file_path)[0] + ".out"
                with open(out_file, 'w', encoding='utf-8') as f:
                    f.write(f"Error running {os.path.basename(file_path)}:\n{str(e)}")
            except:
                pass

    def _handle_markdown_change(self, file_path):
        """Handle changes to markdown files."""
        if self.verbose:
            print(f"Rebuilding markdown file: {os.path.basename(file_path)}")

        # Convert the path from src/ to docs/
        rel_path = os.path.relpath(file_path, build.SRC_DIR)
        out_path = os.path.join(build.OUT_DIR, rel_path)
        out_html_path = os.path.splitext(out_path)[0] + '.html'

        # Ensure output directory exists
        os.makedirs(os.path.dirname(out_html_path), exist_ok=True)

        # Build the HTML file
        base_path = os.path.dirname(file_path)
        try:
            success = build.build_html(file_path, out_html_path)
            if success and self.verbose:
                print(f"  Successfully built {os.path.basename(out_html_path)}")
        except Exception as e:
            print(f"  Error building HTML: {str(e)}")

    def _handle_other_file(self, file_path):
        """Handle changes to other files."""
        # Simply copy the file to the docs directory
        self._copy_file_to_docs(file_path)

    def _copy_file_to_docs(self, file_path):
        """Copy a file from src to docs directory."""
        # Skip dotfiles and files with underscore prefix
        if not build.should_process_file(file_path):
            return

        try:
            rel_path = os.path.relpath(file_path, build.SRC_DIR)
            out_path = os.path.join(build.OUT_DIR, rel_path)

            # Ensure the output directory exists
            os.makedirs(os.path.dirname(out_path), exist_ok=True)

            # Copy the file
            shutil.copy2(file_path, out_path)
            if self.verbose:
                print(f"Copied {os.path.basename(file_path)} to {os.path.dirname(out_path)}")
        except Exception as e:
            print(f"  Error copying file: {str(e)}")

    def _rebuild_all_markdown(self):
        """Rebuild all markdown files in the source directory."""
        markdown_files = []

        # Find all markdown files
        for root, dirs, files in os.walk(build.SRC_DIR):
            # Skip directories starting with underscore or dot
            dirs[:] = [d for d in dirs if not (d.startswith('_') or d.startswith('.'))]

            for file in files:
                if file.endswith('.md') and build.should_process_file(os.path.join(root, file)):
                    file_path = os.path.join(root, file)
                    markdown_files.append(file_path)

        # Build each markdown file
        for md_file in markdown_files:
            self._handle_markdown_change(md_file)

    def _update_dependent_markdown(self, rkt_file):
        """Find and update markdown files that might reference this Racket file."""
        rkt_basename = os.path.basename(rkt_file)
        rkt_rel_path = os.path.relpath(rkt_file, build.SRC_DIR)
        markdown_files = []

        # Find all markdown files
        for root, dirs, files in os.walk(build.SRC_DIR):
            # Skip directories starting with underscore or dot
            dirs[:] = [d for d in dirs if not (d.startswith('_') or d.startswith('.'))]

            for file in files:
                if file.endswith('.md') and build.should_process_file(os.path.join(root, file)):
                    md_path = os.path.join(root, file)

                    # Check if this markdown file references the Racket file
                    try:
                        with open(md_path, 'r', encoding='utf-8') as f:
                            content = f.read()

                        # Check various ways a markdown file might reference the Racket file
                        rkt_name_no_ext = os.path.splitext(rkt_basename)[0]
                        patterns = [
                            rkt_basename,              # Direct filename
                            rkt_rel_path,              # Relative path
                            rkt_name_no_ext,           # Filename without extension
                            f"@src({rkt_basename})",   # @src directive with filename
                            f"@src({rkt_rel_path})",   # @src directive with path
                            f"@src({rkt_name_no_ext})" # @src directive with name
                        ]

                        for pattern in patterns:
                            if pattern in content:
                                markdown_files.append(md_path)
                                break
                    except Exception:
                        # Skip if we can't read the file
                        pass

        if self.verbose and markdown_files:
            print(f"Found {len(markdown_files)} markdown files referencing {rkt_basename}")

        # If we couldn't find any specific files, rebuild markdown files in the Racket file's directory
        if not markdown_files:
            rkt_dir = os.path.dirname(rkt_file)
            for root, dirs, files in os.walk(rkt_dir):
                dirs[:] = [d for d in dirs if not (d.startswith('_') or d.startswith('.'))]
                for file in files:
                    if file.endswith('.md') and build.should_process_file(os.path.join(root, file)):
                        markdown_files.append(os.path.join(root, file))

        # Build each relevant markdown file
        for md_file in markdown_files:
            self._handle_markdown_change(md_file)


def find_missing_outputs(src_dir=build.SRC_DIR):
    """Find Racket files that don't have corresponding .out files."""
    missing_outputs = []

    for root, dirs, files in os.walk(src_dir):
        dirs[:] = [d for d in dirs if not (d.startswith('_') or d.startswith('.'))]
        for file in files:
            if file.endswith('.rkt') and build.should_process_file(os.path.join(root, file)):
                rkt_path = os.path.join(root, file)
                out_path = os.path.splitext(rkt_path)[0] + ".out"

                # Check if .out file exists
                if not os.path.exists(out_path):
                    print(f"Missing output file: {rkt_path}")
                    missing_outputs.append(rkt_path)

    return missing_outputs

def find_racket_references(src_dir=build.SRC_DIR):
    """Find Racket files referenced in markdown files that need to be built or rebuilt."""
    needs_building = set()
    all_references = set()
    print("Scanning markdown files for Racket references...")

    # Find all markdown files
    for root, dirs, files in os.walk(src_dir):
        dirs[:] = [d for d in dirs if not (d.startswith('_') or d.startswith('.'))]

        for file in files:
            if file.endswith('.md') and build.should_process_file(os.path.join(root, file)):
                md_path = os.path.join(root, file)

                # Read the markdown file
                try:
                    with open(md_path, 'r', encoding='utf-8') as f:
                        content = f.read()

                    # Look for references to .rkt files
                    import re

                    # Markdown link syntax: [text](file.rkt)
                    md_links = re.findall(r'\[.*?\]\((.*?\.rkt)(?:\s.*?)?\)', content)

                    # HTML-style links: src="file.rkt" or href="file.rkt"
                    html_links = re.findall(r'(?:src|href)=["\']([^"\']+\.rkt)["\']', content)

                    # Include syntax: <!--include: file.rkt-->
                    include_refs = re.findall(r'<!--\s*include:\s*(.*?\.rkt)\s*-->', content)

                    # @src directive: @src(file.rkt)
                    src_directives = re.findall(r'@src\((.*?\.rkt)\)', content)

                    # Also look for just the filename mentioned
                    file_mentions = re.findall(r'(?:^|\s|\()([\w\-]+\.rkt)(?:\s|$|\))', content)

                    # Combine all references
                    all_refs = md_links + html_links + include_refs + src_directives + file_mentions

                    # Process each reference
                    for rkt_ref in all_refs:
                        # Handle both relative and absolute paths
                        if os.path.isabs(rkt_ref):
                            rkt_path = rkt_ref
                        else:
                            # First, try directly relative to markdown file
                            md_dir = os.path.dirname(md_path)
                            rkt_path = os.path.normpath(os.path.join(md_dir, rkt_ref))

                            # If that doesn't exist, try just the filename in the src directory
                            if not os.path.exists(rkt_path):
                                # Search in the source directory for any file with the same basename
                                basename = os.path.basename(rkt_ref)
                                for search_root, search_dirs, search_files in os.walk(src_dir):
                                    if basename in search_files:
                                        rkt_path = os.path.join(search_root, basename)
                                        break

                        # Add to all references for logging
                        all_references.add(rkt_path)

                        # Check if the Racket file exists and needs rebuilding
                        if os.path.exists(rkt_path) and rkt_path.endswith('.rkt'):
                            out_path = os.path.splitext(rkt_path)[0] + ".out"

                            # Add to list if:
                            # 1. .out file doesn't exist, or
                            # 2. .rkt file is newer than .out file
                            if not os.path.exists(out_path):
                                needs_building.add(rkt_path)
                            elif os.path.exists(out_path):
                                rkt_mtime = os.path.getmtime(rkt_path)
                                out_mtime = os.path.getmtime(out_path)
                                if rkt_mtime > out_mtime:
                                    needs_building.add(rkt_path)
                except Exception:
                    pass  # Skip files we can't read

    print(f"Found {len(all_references)} Racket references in markdown files")
    print(f"Of those, {len(needs_building)} need to be built or rebuilt")

    return list(needs_building)

def find_outdated_outputs(src_dir=build.SRC_DIR):
    """Find Racket files whose outputs are older than the source files."""
    outdated_files = []

    for root, dirs, files in os.walk(src_dir):
        dirs[:] = [d for d in dirs if not (d.startswith('_') or d.startswith('.'))]

        for file in files:
            if file.endswith('.rkt') and build.should_process_file(os.path.join(root, file)):
                rkt_path = os.path.join(root, file)
                out_path = os.path.splitext(rkt_path)[0] + ".out"

                # Skip if output doesn't exist
                if not os.path.exists(out_path):
                    continue

                # Check if source is newer than output
                rkt_mtime = os.path.getmtime(rkt_path)
                out_mtime = os.path.getmtime(out_path)

                if rkt_mtime > out_mtime:
                    print(f"Outdated output for {rkt_path}")
                    outdated_files.append(rkt_path)

    return outdated_files

def clean_zombie_processes():
    """Try to clean up any zombie or lingering Python processes."""
    if sys.platform != 'win32' and server is not None:
        try:
            # Send SIGTERM to any Python processes using server ports
            server.cleanup_ports()
        except Exception as e:
            print(f"Error cleaning up processes: {str(e)}")

def watch_directory(src_dir=build.SRC_DIR, out_dir=build.OUT_DIR, verbose=True, initial_build=True,
                   start_server=True, port=8000):
    """Watch the source directory for changes and rebuild as needed."""

    # Try to clean up any lingering processes first
    if server is not None:
        clean_zombie_processes()

    # Track what we need to clean up
    server_thread = None

    try:
        # Perform an initial build if requested
        if initial_build:
            print("Performing initial build...")

            # Find all Racket files that need rebuilding
            print("\n==== Finding Racket Files Needing Updates ====")
            missing_outputs = find_missing_outputs(src_dir)
            outdated_outputs = find_outdated_outputs(src_dir)
            required_files = find_racket_references(src_dir)

            # Combine all files that need processing
            all_needed_files = list(set(required_files + missing_outputs + outdated_outputs))

            if all_needed_files:
                print(f"\n==== Processing {len(all_needed_files)} Racket Files ====")
                build.run_racket_files(file_list=all_needed_files)
            else:
                print("No Racket files need processing.")

            # Build the markdown files
            print("\n==== Building Markdown Files ====")
            build.process_directory()

            print("\nInitial build completed. Other Racket files will be built on demand.")

        # Start the server if requested
        if start_server and server is not None:
            print("\nStarting development server...")
            server_thread = server.start_server(out_dir, port)

        print(f"\nWatching directory {src_dir} for changes...")
        print("Press Ctrl+C to stop watching and server.")

        # Create an observer and event handler
        observer = Observer()
        event_handler = ChangeHandler(src_dir, out_dir, verbose)

        # Schedule the observer to watch the source directory recursively
        observer.schedule(event_handler, src_dir, recursive=True)

        # Start the observer
        observer.start()

        # Keep the main thread running and check for batched changes
        while True:
            time.sleep(0.5)
            # Process any pending changes
            event_handler._process_batch()

    except KeyboardInterrupt:
        print("\nStopping watcher and server...")
        # Stop the observer
        if 'observer' in locals():
            observer.stop()
            observer.join()

        # Stop the server
        if server_thread:
            server_thread.stop()
            server_thread.join()

        print("Watcher and server stopped.")

    return True


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description="SICP Watch Module")
    parser.add_argument("--no-initial-build", action="store_true",
                        help="Skip initial build when watching")
    parser.add_argument("--no-server", action="store_true",
                        help="Don't start a development server")
    parser.add_argument("--port", type=int, default=8000,
                        help="Port for the development server (default: 8000)")

    args = parser.parse_args()

    # Watch the source directory with the given options
    watch_directory(
        initial_build=not args.no_initial_build,
        start_server=not args.no_server,
        port=args.port
    )
