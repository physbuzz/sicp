# Makefile for SICP notes project
# Converts markdown files to HTML in-place

# Define the Python interpreter and script
PYTHON = python3
MD2HTML = build/md2html.py

# Define the base directory for the project
BASE_DIR = .

# Find all markdown files in the project
MD_FILES := $(shell find $(BASE_DIR)/src -name "*.md")

# Generate the corresponding HTML file paths
HTML_FILES := $(MD_FILES:.md=.html)

# Default target
all: $(HTML_FILES)

# Pattern rule to convert .md to .html
%.html: %.md
	@echo "Converting $< to $@..."
	@$(PYTHON) $(MD2HTML) $< -o $@ -b $(dir $<)

# Build index separately
index: src/index.html

src/index.html: src/index.md
	@echo "Building main index..."
	@$(PYTHON) $(MD2HTML) $< -o $@ -b src/

# Clean generated HTML files
clean:
	@echo "Cleaning generated HTML files..."
	@find $(BASE_DIR)/src -name "*.html" -type f -delete

# Force rebuild all files
rebuild: clean all

# Build a specific chapter
ch1:
	@echo "Building Chapter 1..."
	@find $(BASE_DIR)/src/ch1 -name "*.md" -exec $(PYTHON) $(MD2HTML) {} -o {:.md=.html} -b $(dir {}) \;

# Build meeting notes
meetings:
	@echo "Building meeting notes..."
	@find $(BASE_DIR)/src/meetings -name "*.md" -exec $(PYTHON) $(MD2HTML) {} -o {:.md=.html} -b $(dir {}) \;

# Watch for changes and rebuild (requires inotifywait)
watch:
	@echo "Watching for changes in src directory..."
	@while true; do \
		inotifywait -r -e modify,create,delete $(BASE_DIR)/src; \
		$(MAKE) all; \
	done

# Show help
help:
	@echo "SICP Notes Makefile"
	@echo "-------------------"
	@echo "Targets:"
	@echo "  all      - Build all markdown files to HTML (default)"
	@echo "  index    - Only build the main index.html"
	@echo "  ch1      - Only build Chapter 1 files"
	@echo "  meetings - Only build meeting notes"
	@echo "  clean    - Remove all generated HTML files"
	@echo "  rebuild  - Force rebuild all files"
	@echo "  watch    - Watch for changes and rebuild (requires inotifywait)"
	@echo "  help     - Show this help message"

.PHONY: all clean rebuild index ch1 meetings watch help
