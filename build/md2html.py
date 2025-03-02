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

def get_html_template(title, html_content, pygments_css):
    """
    Generate an enhanced HTML template with improved styling
    """
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
            padding: 0;
            background-color: #f8f9fa;
        }}

        /* Navigation bar */
        .navbar {{
            background-color: #2c3e50;
            color: white;
            padding: 1rem;
            position: sticky;
            top: 0;
            z-index: 1000;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }}

        .navbar-content {{
            max-width: 1000px;
            margin: 0 auto;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}

        .navbar a {{
            color: white;
            text-decoration: none;
            margin-left: 1.5rem;
            font-weight: 500;
        }}

        .navbar a:hover {{
            text-decoration: underline;
        }}

        .navbar .logo {{
            font-weight: bold;
            font-size: 1.2rem;
            margin-left: 0;
        }}

        /* Center column layout */
        .container {{
            max-width: 800px;
            margin: 2rem auto;
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

        h3 {{
            font-size: 1.5rem;
            margin: 1.8rem 0 1rem;
            color: #34495e;
        }}

        h4 {{
            font-size: 1.3rem;
            margin: 1.5rem 0 0.8rem;
            color: #34495e;
        }}

        h5 {{
            font-size: 1.1rem;
            margin: 1.2rem 0 0.8rem;
            color: #34495e;
        }}

        /* Solution styling */
        h5:has(+p:contains("Solution")) {{
            margin-bottom: 0;
        }}

        h5:has(+p:contains("Solution")) + p {{
            font-weight: bold;
            color: #3c8dbc;
            border-left: 3px solid #3c8dbc;
            padding-left: 0.8rem;
            margin: 0.5rem 0 1rem;
        }}

        p {{
            margin-bottom: 1rem;
        }}

        /* List styling */
        ul, ol {{
            margin-bottom: 1rem;
            padding-left: 2.5rem;
        }}

        ul li, ol li {{
            margin-bottom: 0.5rem;
        }}

        /* Code blocks */
        .codehilite {{
            background-color: #f6f8fa;
            border-radius: 6px;
            overflow-x: auto;
            margin: 1rem 0 1.5rem;
            border: 1px solid #e1e4e8;
        }}

        .code-header {{
            font-family: SFMono-Regular, Consolas, "Liberation Mono", Menlo, monospace;
            font-size: 9pt;
            color: #6a737d;
            padding: 0.5rem 1rem;
            border-bottom: 1px solid #e1e4e8;
            background-color: #fafbfc;
            border-top-left-radius: 6px;
            border-top-right-radius: 6px;
        }}

        .code-header a {{
            color: #6a737d;
            text-decoration: none;
        }}

        .code-header a:hover {{
            text-decoration: underline;
            color: #0366d6;
        }}

        .code-output {{
            font-family: SFMono-Regular, Consolas, "Liberation Mono", Menlo, monospace;
            font-size: 9pt;
            color: #6a737d;
            padding: 0.5rem 1rem;
            border-top: 1px solid #e1e4e8;
            background-color: #fafbfc;
            white-space: pre-wrap;
        }}

        .codehilite pre {{
            padding: 1rem;
            overflow-x: auto;
            margin: 0;
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
            margin-bottom: 1rem;
            padding: 0.4rem 0.8rem;
            background-color: #3c8dbc;
            color: white;
            border-radius: 4px;
            text-decoration: none;
            font-size: 0.85rem;
            font-weight: 500;
        }}

        .run-racket:hover {{
            background-color: #367fa9;
            text-decoration: none;
        }}

        /* Make LaTeX display nicely */
        .MathJax {{
            overflow-x: auto;
            overflow-y: hidden;
        }}
    </style>
</head>
<body>
    <!-- Navigation Bar -->
    <div class="navbar">
        <div class="navbar-content">
            <a href="/index.html" class="logo">SICP Notes</a>
            <div>
                <a href="/ch1/notes-ch1-1.html">Chapter 1</a>
                <a href="/meetings/index.html">Meetings</a>
                <a href="https://github.com/yourusername/sicp-notes" target="_blank">GitHub</a>
            </div>
        </div>
    </div>

    <div class="container">
        {html_content}
    </div>
</body>
</html>
"""

def convert_markdown_to_html(input_file, output_file=None, base_path=None, run_link=False, show_output=True):
    """
    Convert a markdown file to HTML with support for code blocks and raw HTML.

    Args:
        input_file (str): Path to input markdown file
        output_file (str, optional): Path to output HTML file. If None, derives from input name
        base_path (str, optional): Base path for source files. If None, uses input file's directory
        run_link (bool): Whether to add links to run the code in a sandbox
        show_output (bool): Whether to show output files
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
    args = parser.parse_args()

    output_file = convert_markdown_to_html(
        args.input,
        args.output,
        args.base_path,
        args.run_link,
        not args.no_output
    )
    print(f"Converted {args.input} to {output_file}")

if __name__ == '__main__':
    main()
