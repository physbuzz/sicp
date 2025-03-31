#!/usr/bin/env python3
# Claude 3.7 generated
"""
SICP Build Script - Improved Version
Replaces the Makefile with a Python-based build system.
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
    """Check if a file should be processed (not starting with underscore or dot)."""
    basename = os.path.basename(path)
    if basename.startswith('.') or basename.startswith('_'):
        return False

    path_parts = Path(path).parts
    for part in path_parts:
        if part.startswith('_') or part.startswith('.'):
            return False

    return True

def run_racket_files(src_dir=SRC_DIR, file_list=None):
    """Run all Racket files in the source directory and generate output files."""
    if file_list:
        print(f"Running {len(file_list)} specified Racket files...")
        racket_files = file_list
    else:
        racket_files = []
        for root, dirs, files in os.walk(src_dir):
            dirs[:] = [d for d in dirs if not d.startswith('_') and not d.startswith('.')]
            for file in files:
                if file.endswith('.rkt') and not file.startswith('_') and not file.startswith('.'):
                    racket_files.append(os.path.join(root, file))
        print(f"Running {len(racket_files)} Racket files...")

    success_count = 0
    error_count = 0

    for racket_file in racket_files:
        print(f"Running {racket_file}...")
        out_file = os.path.splitext(racket_file)[0] + ".out"

        try:
            # Create the output directory if it doesn't exist
            os.makedirs(os.path.dirname(out_file), exist_ok=True)

            result = subprocess.run(
                ['racket', racket_file],
                capture_output=True,
                text=True,
                check=False
            )

            # Write output to file
            with open(out_file, 'w', encoding='utf-8') as f:
                f.write(result.stdout)
                if result.returncode != 0:
                    f.write(f"\nError (exit code {result.returncode}):\n{result.stderr}")
                    print(f"  Error running {racket_file}")
                    error_count += 1
                else:
                    success_count += 1
        except Exception as e:
            print(f"  Error processing {racket_file}: {str(e)}")
            error_count += 1
            # Create an error output file to prevent repeated failures
            try:
                with open(out_file, 'w', encoding='utf-8') as f:
                    f.write(f"Error running {os.path.basename(racket_file)}:\n{str(e)}")
            except:
                pass

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
            check=True,
            capture_output=True
        )
        print(f"  Successfully converted {src_path}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"  Error converting {src_path}: {e.stderr.decode('utf-8')}")
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
        # Skip directories starting with underscore or dot
        dirs[:] = [d for d in dirs if not d.startswith('_') and not d.startswith('.')]

        # Process each file
        for file in files:
            src_path = os.path.join(root, file)

            # Skip files in directories starting with underscore/dot or files starting with underscore/dot
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
            # Copy all other files (except .out files, which are generated)
            elif not file.endswith('.out'):
                print(f"Copying {src_path} to {out_path}")
                shutil.copy2(src_path, out_path)
                file_counts['copied'] += 1

    print(f"\nProcessed files:")
    print(f"  Built {file_counts['markdown']} markdown files")
    print(f"  Copied {file_counts['copied']} files")
    print(f"  Skipped {file_counts['skipped']} files (underscore/dot prefix)")

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
        # Recreate the directory to avoid issues
        os.makedirs(out_dir, exist_ok=True)
        print(f"Created empty output directory: {out_dir}")

    # Clean .out files
    clean_outputs(src_dir)

    return True

def watch_and_serve(no_initial_build=False, port=8000):
    """Watch for file changes and serve the files."""
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
    missing_files = []
    outdated_files = []

    for root, dirs, files in os.walk(SRC_DIR):
        dirs[:] = [d for d in dirs if not d.startswith('_') and not d.startswith('.')]
        for file in files:
            if file.endswith('.rkt') and not file.startswith('_') and not file.startswith('.'):
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
        print("Performing full rebuild...")
        clean_all()
        print("\nRunning all Racket files...")
        run_racket_files()  # Run all Racket files first
        print("\nProcessing all files...")
        process_directory()  # Then process all files
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
