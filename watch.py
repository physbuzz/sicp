#!/usr/bin/env python3
"""
Claude 3.7 generated
SICP Watch Module - Improved Version

This module provides functionality to watch for file changes and trigger
appropriate rebuild actions. It uses the watchdog library to monitor
file system events and responds based on file types.

Key features:
1. Monitors the src/ directory for changes
2. Rebuilds only what's necessary based on file type:
   - .rkt files: Runs the specific Racket file, updates .out, rebuilds only relevant HTML
   - .md files: Rebuilds specific markdown file to HTML
   - composable_markdown.py/md2html.py: Rebuilds all markdown files
3. Runs a development server for live preview
"""

import os
import sys
import time
import shutil
import subprocess
from pathlib import Path
try:
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler
except ImportError:
    print("Error: watchdog package is not installed.")
    print("Please install it with: pip install watchdog")
    sys.exit(1)

# Import build script functions (assuming build.py is in the same directory)
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

        time_diff = rkt_mtime - out_mtime

        # If .rkt file is more recent (with a small buffer), rebuild
        if time_diff > 0:
            # Get human-readable times for logging
            from datetime import datetime
            rkt_time = datetime.fromtimestamp(rkt_mtime).strftime('%Y-%m-%d %H:%M:%S')
            out_time = datetime.fromtimestamp(out_mtime).strftime('%Y-%m-%d %H:%M:%S')

            if self.verbose:
                print(f"Racket file {os.path.basename(rkt_file)} is newer than its output, rebuilding...")
                print(f"  Source: {rkt_time} vs Output: {out_time}")
            return True

        return False

    def on_modified(self, event):
        """Handle file modification events."""
        if event.is_directory:
            return

        # Get the file path
        file_path = event.src_path

        # Skip files that start with underscore or are in a directory starting with underscore
        if not build.should_process_file(file_path):
            return

        # Skip files in the docs directory and hidden files
        if '/docs/' in file_path or '\\docs\\' in file_path or os.path.basename(file_path).startswith('.'):
            return

        # Skip .out files - we'll handle them specially
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

        # Process build system files first (they require full rebuild)
        if build_system_files:
            if self.verbose:
                print("Build system files changed. Rebuilding all markdown files...")
            # We only need to rebuild markdown files
            self._rebuild_all_markdown()
        else:
            # Process Racket files FIRST
            if rkt_files:
                for rkt_file in rkt_files:
                    self._handle_racket_change(rkt_file)

            # THEN process markdown files (after Racket outputs are generated)
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
            result = subprocess.run(
                ['racket', file_path],
                capture_output=True,
                text=True,
                check=False
            )

            # Write output to .out file
            out_file = os.path.splitext(file_path)[0] + ".out"
            with open(out_file, 'w', encoding='utf-8') as f:
                if result.returncode != 0:
                    f.write(result.stdout)
                    f.write(f"\nError (exit code {result.returncode}):\n{result.stderr}")
                    print(f"  Error running {os.path.basename(file_path)}")
                else:
                    f.write(result.stdout)
                    if self.verbose:
                        print(f"  Successfully ran {os.path.basename(file_path)}")

            # Rather than rebuilding all markdown, let's find which ones reference this file
            self._update_dependent_markdown(file_path)

            # Copy the updated Racket file and its output to docs
            self._copy_file_to_docs(file_path)
            self._copy_file_to_docs(out_file)

        except Exception as e:
            print(f"  Error: {str(e)}")

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
        # Skip .out files unless explicitly requested
        if file_path.endswith('.out'):
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
            # Skip directories starting with underscore
            dirs[:] = [d for d in dirs if not d.startswith('_')]

            for file in files:
                if file.endswith('.md') and not file.startswith('_'):
                    file_path = os.path.join(root, file)
                    if build.should_process_file(file_path):
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
            # Skip directories starting with underscore
            dirs[:] = [d for d in dirs if not d.startswith('_')]

            for file in files:
                if file.endswith('.md') and not file.startswith('_'):
                    md_path = os.path.join(root, file)
                    if build.should_process_file(md_path):
                        # Check if this markdown file references the Racket file
                        try:
                            with open(md_path, 'r', encoding='utf-8') as f:
                                content = f.read()

                            # Check various ways a markdown file might reference the Racket file
                            if (rkt_basename in content or
                                rkt_rel_path in content or
                                os.path.splitext(rkt_basename)[0] in content):
                                markdown_files.append(md_path)
                        except Exception:
                            # If we can't read the file, skip it
                            pass

        if self.verbose and markdown_files:
            print(f"Found {len(markdown_files)} markdown files referencing {rkt_basename}")

        # If we couldn't find any specific files, but the rkt file is in a chapter directory,
        # rebuild markdown files in that directory
        if not markdown_files:
            rkt_dir = os.path.dirname(rkt_file)
            for root, dirs, files in os.walk(rkt_dir):
                # Skip directories starting with underscore
                dirs[:] = [d for d in dirs if not d.startswith('_')]

                for file in files:
                    if file.endswith('.md') and not file.startswith('_'):
                        md_path = os.path.join(root, file)
                        if build.should_process_file(md_path):
                            markdown_files.append(md_path)

        # Build each relevant markdown file
        for md_file in markdown_files:
            self._handle_markdown_change(md_file)


def find_missing_outputs(src_dir=build.SRC_DIR):
    """Find Racket files that don't have corresponding .out files."""
    missing_outputs = []

    # Find all Racket files
    for root, dirs, files in os.walk(src_dir):
        # Skip directories starting with underscore
        dirs[:] = [d for d in dirs if not d.startswith('_')]

        for file in files:
            if file.endswith('.rkt') and not file.startswith('_'):
                rkt_path = os.path.join(root, file)
                out_path = os.path.splitext(rkt_path)[0] + ".out"

                # Check if .out file exists
                if not os.path.exists(out_path):
                    print(f"Missing output file: {rkt_path}")
                    missing_outputs.append(rkt_path)

    return missing_outputs

def generate_required_outputs(src_dir=build.SRC_DIR, html_dir=build.OUT_DIR):
    """Find and generate outputs for Racket files that are referenced by HTML files."""
    print("Checking for HTML files with missing or outdated Racket outputs...")
    generated_count = 0
    required_files = set()

    # First, find all HTML files
    for root, dirs, files in os.walk(html_dir):
        # Skip directories starting with underscore
        dirs[:] = [d for d in dirs if not d.startswith('_')]

        for file in files:
            if file.endswith('.html'):
                html_path = os.path.join(root, file)

                # Read the HTML file
                try:
                    with open(html_path, 'r', encoding='utf-8') as f:
                        content = f.read()

                    # Look for references to .rkt files
                    import re
                    rkt_refs = re.findall(r'(?:src|href)=["\']([^"\']+\.rkt)["\']', content)

                    # Map to src paths
                    for rkt_ref in rkt_refs:
                        html_dir_path = os.path.dirname(html_path)
                        rkt_path_in_html = os.path.normpath(os.path.join(html_dir_path, rkt_ref))

                        # Convert from html path to src path
                        if rkt_path_in_html.startswith(html_dir):
                            rel_path = os.path.relpath(rkt_path_in_html, html_dir)
                            rkt_path_in_src = os.path.join(src_dir, rel_path)
                            required_files.add(rkt_path_in_src)
                except Exception:
                    # If we can't read the file, skip it
                    pass

    # Find files that need rebuilding (missing .out or outdated)
    needs_rebuild = []
    for rkt_path in required_files:
        out_path = os.path.splitext(rkt_path)[0] + ".out"
        needs_rebuild_flag = False

        # Check if .out is missing
        if not os.path.exists(out_path) and os.path.exists(rkt_path):
            needs_rebuild_flag = True
        # Check if .out is outdated
        elif os.path.exists(rkt_path) and os.path.exists(out_path):
            rkt_mtime = os.path.getmtime(rkt_path)
            out_mtime = os.path.getmtime(out_path)
            if rkt_mtime > out_mtime:
                needs_rebuild_flag = True

        if needs_rebuild_flag:
            needs_rebuild.append(rkt_path)

    # Generate the missing or outdated outputs
    if needs_rebuild:
        print(f"Found {len(needs_rebuild)} Racket files referenced in HTML that need rebuilding.")
        print("Generating required outputs...")
        build.run_racket_files(file_list=needs_rebuild)
        generated_count = len(needs_rebuild)
    else:
        print("All required Racket outputs are up to date.")

    return generated_count

def find_racket_references(src_dir=build.SRC_DIR):
    """Find Racket files referenced in markdown files that need to be built or rebuilt."""
    needs_building = set()
    all_references = set()
    print("Scanning markdown files for Racket references...")

    # Find all markdown files
    for root, dirs, files in os.walk(src_dir):
        # Skip directories starting with underscore
        dirs[:] = [d for d in dirs if not d.startswith('_')]

        for file in files:
            if file.endswith('.md') and not file.startswith('_'):
                md_path = os.path.join(root, file)

                # Read the markdown file
                try:
                    with open(md_path, 'r', encoding='utf-8') as f:
                        content = f.read()

                    # Look for references to .rkt files - both in markdown links and code includes
                    import re

                    # Markdown link syntax: [text](file.rkt)
                    md_links = re.findall(r'\[.*?\]\((.*?\.rkt)(?:\s.*?)?\)', content)

                    # HTML-style links: src="file.rkt" or href="file.rkt"
                    html_links = re.findall(r'(?:src|href)=["\']([^"\']+\.rkt)["\']', content)

                    # Include syntax: <!--include: file.rkt-->
                    include_refs = re.findall(r'<!--\s*include:\s*(.*?\.rkt)\s*-->', content)

                    # Also look for just the filename mentioned
                    file_mentions = re.findall(r'(?:^|\s|\()([\w\-]+\.rkt)(?:\s|$|\))', content)

                    # Combine all references
                    all_refs = md_links + html_links + include_refs + file_mentions

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

                        # Check if the Racket file exists
                        if os.path.exists(rkt_path) and rkt_path.endswith('.rkt'):
                            # Check if it needs rebuilding
                            out_path = os.path.splitext(rkt_path)[0] + ".out"

                            # Add to list if:
                            # 1. .out file doesn't exist, or
                            # 2. .rkt file is newer than .out file
                            rebuild_needed = False
                            if not os.path.exists(out_path):
                                print(f"Found reference to {rkt_path} with missing .out file")
                                rebuild_needed = True
                            elif os.path.exists(out_path):
                                rkt_mtime = os.path.getmtime(rkt_path)
                                out_mtime = os.path.getmtime(out_path)
                                time_diff = rkt_mtime - out_mtime
                                if time_diff > 0:
                                    print(f"Found reference to {rkt_path} with outdated .out file ({time_diff:.2f} seconds older)")
                                    rebuild_needed = True

                            if rebuild_needed:
                                needs_building.add(rkt_path)
                except Exception as e:
                    # If we can't read the file, skip it
                    print(f"Error reading {md_path}: {str(e)}")
                    pass

    print(f"Found {len(all_references)} Racket references in markdown files")
    print(f"Of those, {len(needs_building)} need to be built or rebuilt")

    return list(needs_building)

def find_outdated_outputs(src_dir=build.SRC_DIR):
    """Find Racket files whose outputs are older than the source files."""
    outdated_files = []

    # Find all Racket files
    for root, dirs, files in os.walk(src_dir):
        # Skip directories starting with underscore
        dirs[:] = [d for d in dirs if not d.startswith('_')]

        for file in files:
            if file.endswith('.rkt') and not file.startswith('_'):
                rkt_path = os.path.join(root, file)
                out_path = os.path.splitext(rkt_path)[0] + ".out"

                # Skip if output doesn't exist (these are handled by find_missing_outputs)
                if not os.path.exists(out_path):
                    continue

                # Check if source is newer than output
                rkt_mtime = os.path.getmtime(rkt_path)
                out_mtime = os.path.getmtime(out_path)

                # Use a small buffer (1 second) to account for file system timestamp precision
                if rkt_mtime > out_mtime + 1:
                    # Get human-readable times for logging
                    from datetime import datetime
                    rkt_time = datetime.fromtimestamp(rkt_mtime).strftime('%Y-%m-%d %H:%M:%S')
                    out_time = datetime.fromtimestamp(out_mtime).strftime('%Y-%m-%d %H:%M:%S')
                    print(f"Outdated output for {rkt_path}: {rkt_time} vs {out_time}")
                    outdated_files.append(rkt_path)

    return outdated_files
def watch_directory(src_dir=build.SRC_DIR, out_dir=build.OUT_DIR, verbose=True, initial_build=True,
                   start_server=True, port=8000):
    """Watch the source directory for changes and rebuild as needed."""

    # Track what we need to clean up
    server_thread = None

    try:
        # Perform an initial build if requested
        if initial_build:
            print("Performing initial build...")

            # First, scan for all Racket files that need rebuilding
            print("\n==== Finding Racket Files Missing Outputs ====")
            missing_outputs = find_missing_outputs(src_dir)
            if missing_outputs:
                print(f"Found {len(missing_outputs)} Racket files without .out files")
                for path in missing_outputs[:5]:  # Show first 5
                    print(f"  {path}")
                if len(missing_outputs) > 5:
                    print(f"  ... and {len(missing_outputs) - 5} more")

            # Check for outdated Racket files
            print("\n==== Finding Outdated Racket Outputs ====")
            outdated_outputs = find_outdated_outputs(src_dir)
            if outdated_outputs:
                print(f"Found {len(outdated_outputs)} Racket files with outdated outputs")
                for path in outdated_outputs[:5]:  # Show first 5
                    print(f"  {path}")
                if len(outdated_outputs) > 5:
                    print(f"  ... and {len(outdated_outputs) - 5} more")

            # FIRST: Generate .out files for Racket files referenced in HTML or markdown
            # This ensures they exist before building markdown files
            print("\n==== Checking for Required Racket Files ====")
            required_files = find_racket_references(src_dir)

            # Combine all files that need processing
            all_needed_files = list(set(required_files + missing_outputs + outdated_outputs))

            if all_needed_files:
                print(f"\n==== Processing {len(all_needed_files)} Required Racket Files ====")
                build.run_racket_files(file_list=all_needed_files)
            else:
                print("No Racket files need processing.")

            # SECOND: Build the markdown files
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
        print("\n🛑 Stopping watcher and server...")
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
