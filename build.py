#!/usr/bin/env python3
# Claude 3.7 generated
"""
SICP Build Script

Replaces the Makefile with a more reliable Python-based build system.
This script:
1. Runs Racket files that don't begin with underscore (_)
2. Recursively copies all files from src/ to docs/
3. Compiles markdown files to HTML using build/md2html.py
4. Can watch for file changes and automatically rebuild (new)
5. Can start a development server for live preview
"""

import os
import sys
import shutil
import subprocess
import argparse
from pathlib import Path

# Configuration
SRC_DIR = "src"
OUT_DIR = "docs"
MD2HTML = "build/md2html.py"

def should_process_file(path):
    """Check if a file should be processed (not starting with underscore)."""
    path_parts = Path(path).parts
    # Skip any file or directory that starts with underscore
    for part in path_parts:
        if part.startswith('_'):
            return False
    return True

def run_racket_files(src_dir=SRC_DIR, file_list=None):
    """Run all Racket files in the source directory and generate output files.

    If file_list is provided, only process those specific files.
    """
    if file_list:
        print(f"Running {len(file_list)} specified Racket files...")
        racket_files = file_list
    else:
        print("Running all Racket files and generating output files...")
        racket_files = []

        # Find all Racket files
        for root, dirs, files in os.walk(src_dir):
            # Skip directories starting with underscore
            dirs[:] = [d for d in dirs if not d.startswith('_')]

            for file in files:
                if file.endswith('.rkt') and not file.startswith('_'):
                    racket_files.append(os.path.join(root, file))

    success_count = 0
    error_count = 0

    # Run each Racket file
    for racket_file in racket_files:
        print(f"Running {racket_file}...")
        out_file = os.path.splitext(racket_file)[0] + ".out"

        try:
            result = subprocess.run(
                ['racket', racket_file],
                capture_output=True,
                text=True,
                check=False
            )

            # Write output to file
            with open(out_file, 'w', encoding='utf-8') as f:
                if result.returncode != 0:
                    f.write(result.stdout)
                    f.write(f"\nError (exit code {result.returncode}):\n{result.stderr}")
                    print(f"  Error running {racket_file}")
                    error_count += 1
                else:
                    f.write(result.stdout)
                    success_count += 1
        except Exception as e:
            print(f"  Error: {str(e)}")
            error_count += 1

    print(f"\nProcessed {len(racket_files)} Racket files")
    print(f"  Success: {success_count}")
    print(f"  Errors: {error_count}")
    return success_count, error_count

def build_html(src_path, out_path):
    """Build HTML from markdown file."""
    base_path = os.path.dirname(src_path)
    print(f"Converting {src_path} to {out_path}...")

    # Ensure output directory exists
    os.makedirs(os.path.dirname(out_path), exist_ok=True)

    # Run md2html.py
    try:
        subprocess.run(
            ['python3', MD2HTML, src_path, '-o', out_path, '-b', base_path],
            check=True
        )
        print(f"  Successfully converted {src_path}")
        return True
    except subprocess.CalledProcessError:
        print(f"  Error converting {src_path}")
        return False

def process_directory(src_dir=SRC_DIR, out_dir=OUT_DIR):
    """Process all files in the directory."""
    print(f"Processing files from {src_dir} to {out_dir}...")

    # Ensure output directory exists
    os.makedirs(out_dir, exist_ok=True)

    file_counts = {
        'markdown': 0,
        'copied': 0,
        'skipped': 0
    }

    # Walk through the source directory
    for root, dirs, files in os.walk(src_dir):
        # Skip directories starting with underscore
        dirs[:] = [d for d in dirs if not d.startswith('_')]

        # Process each file
        for file in files:
            src_path = os.path.join(root, file)

            # Skip files in directories starting with underscore or files starting with underscore
            if not should_process_file(src_path):
                file_counts['skipped'] += 1
                continue

            # Create corresponding output path
            rel_path = os.path.relpath(src_path, src_dir)
            out_path = os.path.join(out_dir, rel_path)

            # Ensure output directory exists
            os.makedirs(os.path.dirname(out_path), exist_ok=True)

            # Process markdown files
            if file.endswith('.md'):
                out_html_path = os.path.splitext(out_path)[0] + '.html'
                build_html(src_path, out_html_path)
                file_counts['markdown'] += 1
            # Copy all other files
            elif not file.endswith('.out'):  # Skip .out files, they'll be generated again
                print(f"Copying {src_path} to {out_path}")
                shutil.copy2(src_path, out_path)
                file_counts['copied'] += 1

    print(f"\nProcessed files:")
    print(f"  Built {file_counts['markdown']} markdown files")
    print(f"  Copied {file_counts['copied']} files")
    print(f"  Skipped {file_counts['skipped']} files (underscore prefix)")

    return file_counts

def clean_outputs(src_dir=SRC_DIR):
    """Clean all .out files."""
    print(f"Cleaning output files from {src_dir}...")
    count = 0

    for root, _, files in os.walk(src_dir):
        for file in files:
            if file.endswith('.out'):
                file_path = os.path.join(root, file)
                os.remove(file_path)
                print(f"  Removed {file_path}")
                count += 1

    print(f"Removed {count} output files")
    return count

def clean_all(out_dir=OUT_DIR, src_dir=SRC_DIR):
    """Clean all generated files."""
    # Clean output directory
    if os.path.exists(out_dir):
        shutil.rmtree(out_dir)
        print(f"Removed output directory: {out_dir}")

    # Clean .out files
    clean_outputs(src_dir)

    return True

def watch_and_serve(no_initial_build=False, port=8000):
    """Watch for file changes and serve the files."""
    # Import the watch functionality
    try:
        from watch import watch_directory
        watch_directory(
            initial_build=not no_initial_build,
            start_server=True,
            port=port
        )
        return 0
    except ImportError as e:
        print(f"Error: {str(e)}")
        print("Please ensure watch.py is available and watchdog is installed with: pip install watchdog")
        return 1

def find_missing_outputs():
    """Find and report all Racket files without outputs or with outdated outputs."""
    print("Scanning for Racket files with missing or outdated outputs...")
    missing_files = []
    outdated_files = []

    # Find all Racket files
    for root, dirs, files in os.walk(SRC_DIR):
        # Skip directories starting with underscore
        dirs[:] = [d for d in dirs if not d.startswith('_')]

        for file in files:
            if file.endswith('.rkt') and not file.startswith('_'):
                rkt_path = os.path.join(root, file)
                out_path = os.path.splitext(rkt_path)[0] + ".out"

                # Check if .out file exists
                if not os.path.exists(out_path):
                    missing_files.append(rkt_path)
                else:
                    # Check if .rkt file is newer than .out file
                    rkt_mtime = os.path.getmtime(rkt_path)
                    out_mtime = os.path.getmtime(out_path)
                    if rkt_mtime > out_mtime:
                        outdated_files.append(rkt_path)

    if missing_files:
        print(f"Found {len(missing_files)} Racket files without outputs:")
        for file in missing_files[:10]:  # Show first 10 to avoid cluttering the console
            print(f"  {file}")
        if len(missing_files) > 10:
            print(f"  ... and {len(missing_files) - 10} more")

    if outdated_files:
        print(f"Found {len(outdated_files)} Racket files with outdated outputs:")
        for file in outdated_files[:10]:  # Show first 10 to avoid cluttering the console
            print(f"  {file}")
        if len(outdated_files) > 10:
            print(f"  ... and {len(outdated_files) - 10} more")

    if not missing_files and not outdated_files:
        print("All Racket files have up-to-date outputs.")

    return missing_files + outdated_files

def main():
    parser = argparse.ArgumentParser(description='SICP Build Script')
    parser.add_argument('action', nargs='?', default='all',
                      choices=['all', 'html', 'racket', 'clean', 'clean_outputs', 'rebuild',
                               'watch', 'serve', 'scan-missing'],
                      help='Build action (default: all)')
    parser.add_argument('--no-initial-build', action='store_true',
                      help='Skip initial build when watching (only with watch action)')
    parser.add_argument('--port', type=int, default=8000,
                      help='Port for the development server (default: 8000)')
    parser.add_argument('--files', nargs='+',
                      help='Specific files to process (for racket action only)')
    parser.add_argument('--generate-missing', action='store_true',
                      help='Generate outputs for all missing Racket files')
    args = parser.parse_args()

    if args.action == 'clean_outputs':
        clean_outputs()
    elif args.action == 'clean':
        clean_all()
    elif args.action == 'racket':
        run_racket_files(file_list=args.files)
    elif args.action == 'html':
        process_directory()
    elif args.action == 'rebuild':
        clean_all()
        process_directory()  # Skip running all Racket files by default
    elif args.action == 'scan-missing':
        missing_files = find_missing_outputs()
        if args.generate_missing and missing_files:
            print("\nGenerating missing outputs...")
            run_racket_files(file_list=missing_files)
    elif args.action == 'watch' or args.action == 'serve':
        return watch_and_serve(args.no_initial_build, args.port)
    else:  # 'all'
        run_racket_files()
        process_directory()

    return 0

if __name__ == '__main__':
    sys.exit(main())
