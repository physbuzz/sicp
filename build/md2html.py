#!/usr/bin/env python3
# Claude 3.7 generated file
import sys
import os
import re
import markdown
import argparse
from pygments.formatters import HtmlFormatter

# Import our custom extension
from composable_markdown import ComposableMarkdownExtension

def get_pygments_css():
    """Get the default Pygments CSS."""
    return HtmlFormatter().get_style_defs('.codehilite')

class TocPreprocessor(markdown.preprocessors.Preprocessor):
    """
    Preprocessor to handle @toc directive in markdown content.
    This processes the directive before conversion to HTML.
    """
    TOC_PATTERN = re.compile(r'@toc', re.MULTILINE)

    def __init__(self, md, max_depth=4):
        super().__init__(md)
        self.max_depth = max_depth
        self.toc_placeholder = '{::toc::}'

    def run(self, lines):
        # Check if @toc directive exists
        content = '\n'.join(lines)
        if not self.TOC_PATTERN.search(content):
            return lines

        # Replace @toc with placeholder for later processing
        content = self.TOC_PATTERN.sub(self.toc_placeholder, content)
        return content.split('\n')

class TocPostprocessor(markdown.postprocessors.Postprocessor):
    """
    Postprocessor to replace TOC placeholder with generated TOC.
    This runs after HTML conversion.
    """
    def __init__(self, md, max_depth=4):
        super().__init__(md)
        self.max_depth = max_depth
        self.toc_placeholder = '{::toc::}'

    def run(self, text):
        if self.toc_placeholder not in text:
            return text

        # Find all headers (h1, h2, h3, h4)
        header_pattern = re.compile(r'<h([1-4])>(.*?)<\/h\1>', re.DOTALL)
        headers = header_pattern.findall(text)

        if not headers:
            # Remove placeholder if no headers found
            return text.replace(self.toc_placeholder, '')

        # Create a list of (level, text, id) tuples
        toc_items = []
        for level, content in headers:
            level = int(level)
            if level > self.max_depth:
                continue

            # Extract text content (remove any HTML tags)
            header_text = re.sub(r'<.*?>', '', content)

            # Create slug for anchor
            slug = header_text.lower().strip()
            slug = re.sub(r'[^\w\s-]', '', slug)  # Remove special chars
            slug = re.sub(r'\s+', '-', slug)      # Replace spaces with hyphens

            toc_items.append((level, header_text, slug))

        # If no headers found within our max_depth, just remove the placeholder
        if not toc_items:
            return text.replace(self.toc_placeholder, '')

        # Add id attributes to the headers in the HTML
        modified_text = text
        for level, header_text, slug in toc_items:
            # Find the header and add id attribute if it doesn't already have one
            header_to_find = f'<h{level}>{header_text}</h{level}>'
            header_with_id = f'<h{level} id="{slug}">{header_text}</h{level}>'
            modified_text = modified_text.replace(header_to_find, header_with_id)

        # Collect exercise headings that follow "Exercises" section
        exercise_sections = {}
        in_exercises = False
        current_exercise_section = None

        # First pass to identify exercise sections
        for i, (level, header_text, slug) in enumerate(toc_items):
            # Check if this is an "Exercises" heading
            if header_text == "Exercises" and level == 3:
                in_exercises = True
                current_exercise_section = slug
                exercise_sections[current_exercise_section] = []
            # If we're in an exercises section and hit another h3 or higher level, we're out of the section
            elif in_exercises and level <= 3 and header_text != "Exercises":
                in_exercises = False
                current_exercise_section = None
            # If we're in an exercises section, add this header to that section's list
            elif in_exercises and current_exercise_section:
                exercise_sections[current_exercise_section].append((level, header_text, slug))

        # Build the TOC HTML
        toc_html = ['<div class="table-of-contents">',
                    '<h2>Directory</h2>',
                    '<ul class="toc-list">']

        current_level = 1
        i = 0
        while i < len(toc_items):
            level, header_text, slug = toc_items[i]

            # Handle indentation based on header level
            if level > current_level:
                # Open new sublists for each level difference
                for _ in range(level - current_level):
                    toc_html.append('<ul>')
            elif level < current_level:
                # Close sublists when going back up the hierarchy
                for _ in range(current_level - level):
                    toc_html.append('</ul>')

            current_level = level

            # Special handling for Exercises section
            if header_text == "Exercises" and level == 3 and slug in exercise_sections and exercise_sections[slug]:
                # Add the exercises heading with special styling
                toc_html.append(f'<li><a href="#{slug}" class="toc-exercises">{header_text}</a>')

                # Add the exercise items inline
                toc_html.append('<div class="exercise-container">(')
                toc_html.append('<span class="exercise-list">')

                for _, ex_header, ex_slug in exercise_sections[slug]:
                    toc_html.append(f'<span><a href="#{ex_slug}">{ex_header}</a></span>')

                toc_html.append('</span>)')
                toc_html.append('</div></li>')

                # Skip this section's items in the main loop since we've handled them
                i += 1
                while (i < len(toc_items) and
                       toc_items[i][0] > level and
                       (i+1 == len(toc_items) or toc_items[i+1][0] > level)):
                    i += 1
                continue
            else:
                # Regular TOC entry
                toc_html.append(f'<li><a href="#{slug}">{header_text}</a></li>')

            i += 1

        # Close any remaining open lists
        for _ in range(current_level - 1):  # -1 because we don't need to close the outermost level
            toc_html.append('</ul>')

        toc_html.append('</ul>')
        toc_html.append('</div>')

        toc_html_str = '\n'.join(toc_html)

        # Replace the placeholder with the generated TOC
        modified_text = modified_text.replace(self.toc_placeholder, toc_html_str)

        return modified_text

class TocExtension(markdown.Extension):
    """
    Extension for handling table of contents via @toc directive.
    """
    def __init__(self, **kwargs):
        self.config = {
            'max_depth': [4, 'Maximum heading level to include in TOC']
        }
        super().__init__(**kwargs)

    def extendMarkdown(self, md):
        md.preprocessors.register(TocPreprocessor(md, self.getConfig('max_depth')), 'toc_pre', 25)
        md.postprocessors.register(TocPostprocessor(md, self.getConfig('max_depth')), 'toc_post', 25)

def get_html_template(title, html_content, pygments_css):
    """
    Generate an enhanced HTML template with improved styling
    """
    # Import the CSS from markdown_styles
    from markdown_styles import get_base_css

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <!-- MathJax for LaTeX support -->
    <script src="https://polyfill.io/v3/polyfill.min.js?features=es6"></script>
    <script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
    <script>
        MathJax = {{
            tex: {{
                inlineMath: [['$', '$']],
                displayMath: [['$$', '$$']]
            }}
        }};
    </script>
    <style>
        /* Pygments Syntax Highlighting */
        {pygments_css}

        /* Base CSS from markdown_styles.py */
        {get_base_css()}
    </style>
</head>
<body>
    <div class="container">
        {html_content}
    </div>
</body>
</html>
"""

def convert_markdown_to_html(input_file, output_file=None, base_path=None, run_link=False,
                           show_output=True, toc_enabled=True, toc_depth=4):
    """
    Convert a markdown file to HTML with support for code blocks and raw HTML.

    Args:
        input_file (str): Path to input markdown file
        output_file (str, optional): Path to output HTML file. If None, derives from input name
        base_path (str, optional): Base path for source files. If None, uses input file's directory
        run_link (bool): Whether to add links to run the code in a sandbox
        show_output (bool): Whether to show output files
        toc_enabled (bool): Whether to generate a table of contents
        toc_depth (int): Maximum header depth to include in TOC
    """
    # If no output file specified, replace .md with .html
    if not output_file:
        output_file = input_file.rsplit('.', 1)[0] + '.html'

    # If no base path specified, use the input file's directory
    if not base_path:
        base_path = os.path.dirname(os.path.abspath(input_file))

    # Read markdown content
    with open(input_file, 'r', encoding='utf-8') as f:
        md_content = f.read()

    # Configure the Composable Markdown extension
    composable_extension = ComposableMarkdownExtension(
        base_path=base_path,
        run_link=run_link,
        show_filename=True,
        show_output=show_output,
        process_imports=True,
        sandbox_url='https://racket.run/'  # You can change this to your own sandbox URL later
    )

    # Set up extensions list
    extensions = [
        'fenced_code',
        'codehilite',
        'tables',
        composable_extension
    ]

    # Add TOC extension if enabled
    if toc_enabled:
        toc_extension = TocExtension(max_depth=toc_depth)
        extensions.append(toc_extension)

    # Convert to HTML using Python-Markdown with our custom extensions
    html_content = markdown.markdown(
        md_content,
        extensions=extensions
    )

    # Get Pygments CSS
    pygments_css = get_pygments_css()

    # Generate HTML from template
    title = os.path.basename(input_file)
    html_template = get_html_template(title, html_content, pygments_css)

    # Create output directories if they don't exist
    os.makedirs(os.path.dirname(os.path.abspath(output_file)), exist_ok=True)

    # Write the HTML file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_template)

    return output_file

def main():
    parser = argparse.ArgumentParser(description='Convert Markdown files to HTML with enhanced styling')
    parser.add_argument('input', help='Input markdown file')
    parser.add_argument('-o', '--output', help='Output HTML file (optional)')
    parser.add_argument('-b', '--base-path', help='Base path for source files (optional)')
    parser.add_argument('-r', '--run-link', action='store_true', help='Add links to run code in a sandbox')
    parser.add_argument('--no-output', action='store_true', help='Do not include output files')
    parser.add_argument('--no-toc', action='store_true', help='Do not generate table of contents')
    parser.add_argument('--toc-depth', type=int, default=4, help='Max header depth to include in TOC (default: 4)')
    args = parser.parse_args()

    output_file = convert_markdown_to_html(
        args.input,
        args.output,
        args.base_path,
        args.run_link,
        not args.no_output,
        not args.no_toc,
        args.toc_depth
    )
    print(f"Converted {args.input} to {output_file}")

if __name__ == '__main__':
    main()
