# Claude 3.7 generated
# Simple Makefile for SICP build system
# Aliases commands to the Python build script

# Python script path
BUILD_SCRIPT = ./build.py
SERVER_SCRIPT = ./server.py

# Default port for server
PORT = 8001

# Default target - build everything (both Racket and HTML)
all:
	$(BUILD_SCRIPT) all

# Just build HTML files (not racket)
html:
	$(BUILD_SCRIPT) html

# Just run Racket files
racket:
	$(BUILD_SCRIPT) racket

# Run specific Racket files (usage: make racket-files FILES="file1.rkt file2.rkt")
racket-files:
	$(BUILD_SCRIPT) racket --files $(FILES)

# Clean all generated files (both docs/ and .out files)
clean:
	$(BUILD_SCRIPT) clean

# Clean just the output files (.out files only)
clean-outputs:
	$(BUILD_SCRIPT) clean_outputs

# Build everything without serving or watching
build:
	$(BUILD_SCRIPT) all

# Force rebuild of everything from scratch
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

# Clean up lingering server ports
cleanup-ports:
	python3 $(SERVER_SCRIPT) --cleanup

# Help target
help:
	@echo "SICP Build System"
	@echo "-------------------"
	@echo "make                   - Build everything (Racket files and HTML)"
	@echo "make build             - Same as 'make'"
	@echo "make html              - Build only HTML files"
	@echo "make racket            - Run all Racket files"
	@echo "make racket-files FILES=\"file1.rkt file2.rkt\" - Run specific Racket files"
	@echo "make clean             - Remove all generated files (docs/ and .out files)"
	@echo "make clean-outputs     - Remove only .out files"
	@echo "make rebuild           - Clean and rebuild everything from scratch"
	@echo "make watch             - Watch for changes and start server (port $(PORT))"
	@echo "make watch PORT=8080   - Watch with custom port"
	@echo "make watch-only        - Watch without initial build"
	@echo "make serve             - Start server without watching"
	@echo "make scan-missing      - Find Racket files without outputs"
	@echo "make generate-missing  - Generate all missing outputs"
	@echo "make cleanup-ports     - Kill any lingering processes using server ports"

.PHONY: all html racket racket-files clean clean-outputs build rebuild watch watch-only serve scan-missing generate-missing cleanup-ports help
