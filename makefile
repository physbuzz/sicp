# Claude 3.7 revised makefile
# Makefile for SICP notes project
# Converts markdown files to HTML and copies all other files

# Define the Python interpreter and script
PYTHON = python3
MD2HTML = build/md2html.py

# Define the source and output directories
SRC_DIR = src
OUT_DIR = html

# Find all markdown files in the source directory
MD_FILES := $(shell find $(SRC_DIR) -name "*.md")

# Find all non-markdown files in the source directory (to be copied directly)
NON_MD_FILES := $(shell find $(SRC_DIR) -type f -not -name "*.md")

# Generate the corresponding HTML file paths in the output directory
HTML_FILES := $(patsubst $(SRC_DIR)/%,$(OUT_DIR)/%,$(MD_FILES:.md=.html))

# Generate the target paths for non-markdown files
COPIED_FILES := $(patsubst $(SRC_DIR)/%,$(OUT_DIR)/%,$(NON_MD_FILES))

# Default target - print diagnostics and build
all: html_files copy_files

# Create HTML files from markdown
html_files:
	@echo "Building all markdown files..."
	@mkdir -p $(OUT_DIR)
	@for md_file in $(MD_FILES); do \
		html_file=$${md_file%.md}.html; \
		out_file=$(OUT_DIR)/$${html_file#$(SRC_DIR)/}; \
		dir_name=$$(dirname $$out_file); \
		mkdir -p $$dir_name; \
		echo "Converting $$md_file to $$out_file..."; \
		$(PYTHON) $(MD2HTML) $$md_file -o $$out_file -b $$(dirname $$md_file); \
	done

# Copy all non-markdown files to output directory
copy_files:
	@echo "Copying non-markdown files..."
	@for file in $(NON_MD_FILES); do \
		dest_file=$(OUT_DIR)/$${file#$(SRC_DIR)/}; \
		dest_dir=$$(dirname $$dest_file); \
		mkdir -p $$dest_dir; \
		echo "Copying $$file to $$dest_file"; \
		cp -f $$file $$dest_file; \
	done

# Build index separately
index:
	@echo "Building main index..."
	@mkdir -p $(OUT_DIR)
	@$(PYTHON) $(MD2HTML) $(SRC_DIR)/index.md -o $(OUT_DIR)/index.html -b $(SRC_DIR)

# Clean generated files in output directory
clean:
	@echo "Cleaning generated files..."
	@rm -rf $(OUT_DIR)

# Force rebuild all files
rebuild: clean all

# Build a specific chapter
ch1:
	@echo "Building Chapter 1..."
	@mkdir -p $(OUT_DIR)/ch1
	@find $(SRC_DIR)/ch1 -name "*.md" | while read file; do \
		out_file=$(OUT_DIR)/$${file#$(SRC_DIR)/}; \
		out_file=$${out_file%.md}.html; \
		dir_name=$$(dirname $$out_file); \
		mkdir -p $$dir_name; \
		echo "Converting $$file to $$out_file..."; \
		$(PYTHON) $(MD2HTML) $$file -o $$out_file -b $$(dirname $$file); \
	done
	@echo "Copying Chapter 1 non-markdown files..."
	@find $(SRC_DIR)/ch1 -type f -not -name "*.md" | while read file; do \
		dest_file=$(OUT_DIR)/$${file#$(SRC_DIR)/}; \
		dest_dir=$$(dirname $$dest_file); \
		mkdir -p $$dest_dir; \
		echo "Copying $$file to $$dest_file"; \
		cp -f $$file $$dest_file; \
	done

# Build meeting notes
meetings:
	@echo "Building meeting notes..."
	@mkdir -p $(OUT_DIR)/meetings
	@find $(SRC_DIR)/meetings -name "*.md" | while read file; do \
		out_file=$(OUT_DIR)/$${file#$(SRC_DIR)/}; \
		out_file=$${out_file%.md}.html; \
		dir_name=$$(dirname $$out_file); \
		mkdir -p $$dir_name; \
		echo "Converting $$file to $$out_file..."; \
		$(PYTHON) $(MD2HTML) $$file -o $$out_file -b $$(dirname $$file); \
	done
	@echo "Copying meeting non-markdown files..."
	@find $(SRC_DIR)/meetings -type f -not -name "*.md" | while read file; do \
		dest_file=$(OUT_DIR)/$${file#$(SRC_DIR)/}; \
		dest_dir=$$(dirname $$dest_file); \
		mkdir -p $$dest_dir; \
		echo "Copying $$file to $$dest_file"; \
		cp -f $$file $$dest_file; \
	done

# Copy static assets (if any)
assets:
	@echo "Copying static assets..."
	@if [ -d "$(SRC_DIR)/assets" ]; then \
		mkdir -p $(OUT_DIR)/assets; \
		cp -r $(SRC_DIR)/assets/* $(OUT_DIR)/assets/; \
	fi

# Build everything including assets
full: all assets

# Watch for changes and rebuild (requires inotifywait)
watch:
	@echo "Watching for changes in src directory..."
	@while true; do \
		inotifywait -r -e modify,create,delete $(SRC_DIR); \
		$(MAKE) all; \
	done

# Show help
help:
	@echo "SICP Notes Makefile for GitHub Pages"
	@echo "-----------------------------------"
	@echo "Targets:"
	@echo "  all      - Build all markdown files to HTML and copy non-markdown files (default)"
	@echo "  html_files - Only build markdown files to HTML"
	@echo "  copy_files - Only copy non-markdown files"
	@echo "  index    - Only build the main index.html"
	@echo "  ch1      - Only build Chapter 1 files"
	@echo "  meetings - Only build meeting notes"
	@echo "  assets   - Copy static assets to output directory"
	@echo "  full     - Build all HTML files and copy assets"
	@echo "  clean    - Remove all generated files"
	@echo "  rebuild  - Force rebuild all files"
	@echo "  watch    - Watch for changes and rebuild (requires inotifywait)"
	@echo "  help     - Show this help message"

# Add a debug target to print file paths
debug:
	@echo "Markdown Files:"
	@for file in $(MD_FILES); do echo "  $$file"; done
	@echo "HTML Files (would be):"
	@for md_file in $(MD_FILES); do \
		html_file=$${md_file%.md}.html; \
		out_file=$(OUT_DIR)/$${html_file#$(SRC_DIR)/}; \
		echo "  $$out_file"; \
	done
	@echo "Non-Markdown Files:"
	@for file in $(NON_MD_FILES); do echo "  $$file"; done
	@echo "Copied Files (would be):"
	@for file in $(NON_MD_FILES); do \
		dest_file=$(OUT_DIR)/$${file#$(SRC_DIR)/}; \
		echo "  $$dest_file"; \
	done

.PHONY: all html_files copy_files clean rebuild index ch1 meetings assets full watch help debug
