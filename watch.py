#!/usr/bin/env python3
"""
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
            # Process Racket files
            if rkt_files:
                for rkt_file in rkt_files:
                    self._handle_racket_change(rkt_file)

            # Process markdown files
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


def watch_directory(src_dir=build.SRC_DIR, out_dir=build.OUT_DIR, verbose=True, initial_build=True):
    """Watch the source directory for changes and rebuild as needed."""

    # Perform an initial build if requested
    if initial_build:
        print("Performing initial build...")
        build.run_racket_files()
        build.process_directory()

    print(f"Watching directory {src_dir} for changes...")
    print("Press Ctrl+C to stop watching.")

    # Create an observer and event handler
    observer = Observer()
    event_handler = ChangeHandler(src_dir, out_dir, verbose)

    # Schedule the observer to watch the source directory recursively
    observer.schedule(event_handler, src_dir, recursive=True)

    # Start the observer
    observer.start()

    try:
        # Keep the main thread running and check for batched changes
        while True:
            time.sleep(0.5)
            # Process any pending changes
            event_handler._process_batch()
    except KeyboardInterrupt:
        # Stop the observer on keyboard interrupt
        observer.stop()
        print("\nStopped watching.")

    # Wait for the observer to complete
    observer.join()

    return True


if __name__ == '__main__':
    # If the script is run directly, watch the source directory
    watch_directory()
