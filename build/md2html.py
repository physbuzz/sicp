#!/usr/bin/env python3
# Claude 3.7 generated file
import sys
import os
import markdown
import argparse
from pygments.formatters import HtmlFormatter

# Import our custom extension
from composable_markdown import ComposableMarkdownExtension

def get_pygments_css():
    """Get the default Pygments CSS."""
    return HtmlFormatter().get_style_defs('.codehilite')

def convert_markdown_to_html(input_file, output_file=None, base_path=None, run_link=False):
    """
    Convert a markdown file to HTML with support for code blocks and raw HTML.

    Args:
        input_file (str): Path to input markdown file
        output_file (str, optional): Path to output HTML file. If None, derives from input name
        base_path (str, optional): Base path for Racket source files. If None, uses input file's directory
        run_link (bool): Whether to add links to run the code in a sandbox
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
        show_filename=False,
        process_imports=True,
        sandbox_url='https://racket.run/'  # You can change this to your own sandbox URL later
    )

    # Convert to HTML using Python-Markdown with our custom extension
    html_content = markdown.markdown(
        md_content,
        extensions=[
            'fenced_code', 
            'codehilite', 
            'tables',
            composable_extension
        ]
    )

    # Get Pygments CSS
    pygments_css = get_pygments_css()

    # Basic HTML template with styling
    html_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{os.path.basename(input_file)}</title>
    <style>
        /* Pygments Syntax Highlighting */
        {pygments_css}

        /* Basic reset and fonts */
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            padding: 2rem 1rem;
            background-color: #f8f9fa;
        }}

        /* Center column layout */
        .container {{
            max-width: 800px;
            margin: 0 auto;
            background-color: white;
            padding: 2rem 3rem;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}

        /* Typography */
        h1 {{
            font-size: 2.2rem;
            margin-bottom: 1.5rem;
            color: #2c3e50;
            border-bottom: 2px solid #eee;
            padding-bottom: 0.5rem;
        }}

        h2 {{
            font-size: 1.8rem;
            margin: 2rem 0 1rem;
            color: #34495e;
        }}

        p {{
            margin-bottom: 1rem;
        }}

        /* Code blocks */
        .codehilite {{
            background-color: #f6f8fa;
            border-radius: 6px;
            padding: 1rem;
            overflow-x: auto;
            margin: 1rem 0;
            border: 1px solid #e1e4e8;
        }}

        code {{
            font-family: SFMono-Regular, Consolas, "Liberation Mono", Menlo, monospace;
            font-size: 0.9em;
            padding: 0.2em 0.4em;
            background-color: #f6f8fa;
            border-radius: 3px;
        }}

        .codehilite code {{
            padding: 0;
            background-color: transparent;
        }}

        /* Links */
        a {{
            color: #0366d6;
            text-decoration: none;
        }}

        a:hover {{
            text-decoration: underline;
        }}
        
        /* Run button */
        .run-racket {{
            display: inline-block;
            margin-top: 0.5rem;
            padding: 0.4rem 0.8rem;
            background-color: #3c8dbc;
            color: white;
            border-radius: 4px;
            text-decoration: none;
            font-size: 0.85rem;
        }}
        
        .run-racket:hover {{
            background-color: #367fa9;
            text-decoration: none;
        }}
    </style>
</head>
<body>
    <div class="container">
        {html_content}
    </div>
</body>
</html>
"""

    # Write the HTML file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_template)

    return output_file

def main():
    parser = argparse.ArgumentParser(description='Convert Markdown files to HTML with Racket code support')
    parser.add_argument('input', help='Input markdown file')
    parser.add_argument('-o', '--output', help='Output HTML file (optional)')
    parser.add_argument('-b', '--base-path', help='Base path for Racket source files (optional)')
    parser.add_argument('-r', '--run-link', action='store_true', help='Add links to run code in a sandbox')
    args = parser.parse_args()

    output_file = convert_markdown_to_html(
        args.input, 
        args.output, 
        args.base_path, 
        args.run_link
    )
    print(f"Converted {args.input} to {output_file}")

if __name__ == '__main__':
    main()
