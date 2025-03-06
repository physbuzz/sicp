# Claude 3.7 generated
# Simple Makefile that aliases commands to the Python build script
# This provides familiar make commands while using the Python script

# Python script path
BUILD_SCRIPT = ./build.py

# Default target - build everything
all:
	$(BUILD_SCRIPT) all

# Just build HTML
html:
	$(BUILD_SCRIPT) html

# Just run Racket files
racket:
	$(BUILD_SCRIPT) racket

# Clean all generated files
clean:
	$(BUILD_SCRIPT) clean

# Clean just the output files
clean_outputs:
	$(BUILD_SCRIPT) clean_outputs

# Force rebuild
rebuild:
	$(BUILD_SCRIPT) rebuild

# Help target
help:
	@echo "SICP Notes Build System"
	@echo "----------------------"
	@echo "Targets:"
	@echo "  all          - Build everything (default)"
	@echo "  html         - Build HTML only"
	@echo "  racket       - Run Racket files only"
	@echo "  clean        - Clean all generated files"
	@echo "  clean_outputs - Clean just the output files"
	@echo "  rebuild      - Force rebuild everything"
	@echo "  help         - Show this help message"

.PHONY: all html racket clean clean_outputs rebuild help
