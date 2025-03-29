# Claude 3.7 generated
# Simple Makefile that aliases commands to the Python build script
# This provides familiar make commands while using the Python script

# Python script path
BUILD_SCRIPT = ./build.py

# Default port for server
PORT = 8000

# Default target - build everything
all:
	$(BUILD_SCRIPT) all

# Just build HTML
html:
	$(BUILD_SCRIPT) html

# Just run Racket files
racket:
	$(BUILD_SCRIPT) racket

# Run specific Racket files
racket-files:
	$(BUILD_SCRIPT) racket --files $(FILES)

# Clean all generated files
clean:
	$(BUILD_SCRIPT) clean

# Clean just the output files
clean_outputs:
	$(BUILD_SCRIPT) clean_outputs

# Force rebuild (markdown only, not Racket)
rebuild:
	$(BUILD_SCRIPT) rebuild

# Watch for file changes and rebuild as needed with server
watch:
	$(BUILD_SCRIPT) watch --port $(PORT)

# Watch for file changes without initial build
watch-only:
	$(BUILD_SCRIPT) watch --no-initial-build --port $(PORT)

# Just serve the files without watching
serve:
	$(BUILD_SCRIPT) serve --port $(PORT)

# Scan for missing Racket outputs
scan-missing:
	$(BUILD_SCRIPT) scan-missing

# Generate all missing Racket outputs
generate-missing:
	$(BUILD_SCRIPT) scan-missing --generate-missing
