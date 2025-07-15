# Claude Generated
# Add these CSS rules to the get_base_css function, find the section with
# "--- Styles for Collapsible Code Blocks ---" and modify it

def get_base_css():
    """Return the base CSS for markdown HTML pages."""
    return """
        /* Basic reset and fonts */
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            padding: 0;
            background-color: #f8f9fa;
        }

        /* Navigation styling */
        .nav {
            display: flex;
            justify-content: space-between;
            margin-bottom: 2rem;
            padding-bottom: 0.8rem;
            border-bottom: 1px solid #e1e4e8;
        }

        .nav span {
            padding: 0.4rem 0.8rem;
            border-radius: 4px;
            font-weight: 500;
            font-size: 0.9rem;
        }

        .nav .activenav {
            background-color: #f1f8ff;
        }

        .nav .activenav a {
            color: #0366d6;
            text-decoration: none;
        }

        .nav .activenav a:hover {
            text-decoration: underline;
        }

        .nav .inactivenav {
            color: #959da5;
            background-color: #f6f8fa;
        }

        /* Center column layout */
        .container {
            max-width: 800px;
            margin: 2rem auto;
            background-color: white;
            padding: 2rem 3rem;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }

        /* Typography */
        h1 {
            font-size: 2.2rem;
            margin-bottom: 1.5rem;
            color: #2c3e50;
            border-bottom: 2px solid #eee;
            padding-bottom: 0.5rem;
        }

        h2 {
            font-size: 1.8rem;
            margin: 2rem 0 1rem;
            color: #34495e;
        }

        h3 {
            font-size: 1.5rem;
            margin: 1.8rem 0 1rem;
            color: #34495e;
        }

        h4 {
            font-size: 1.3rem;
            margin: 1.5rem 0 0.8rem;
            color: #34495e;
        }

        h5 {
            font-size: 1.1rem;
            margin: 1.2rem 0 0.8rem;
            color: #34495e;
        }

        /* Table of Contents styling */
        .table-of-contents {
            margin: 0 0 0;
            line-height: 1;
        }

        .toc-list {
            margin: 0;
            padding-left: 20px;
        }

        .toc-list li {
            margin-bottom: 2px;
        }
        .toc-list ul {
            margin-bottom: 2px;
        }

        .exercise-list {
            margin: 0;
            padding-left: 0;
            font-size: 0.95em;
            display: inline;
        }

        .exercise-container {
            display: inline-block;
            margin-top: 2px;
            line-height: 1.2;
        }

        .toc-exercises {
            font-style: italic;
            color: #555;
        }

        .exercise-list a {
            text-decoration: none;
            color: #2070b0;
            margin-right: 0;
        }

        .exercise-list a:hover {
            text-decoration: underline;
        }

        .exercise-list span:not(:last-child):after {
            content: ", ";
            color: #777;
            margin-right: 0;
        }

        /* Blockquote styling */
        blockquote {
            border-left: 4px solid #dfe2e5;
            color: #6a737d;
            padding: 0 1rem;
            margin: 1rem 0 1.5rem;
            background-color: #f6f8fa;
            border-radius: 0 3px 3px 0;
        }

        blockquote p {
            padding: 0.8rem 0;
        }

        blockquote p:first-child {
            margin-top: 0;
        }

        blockquote p:last-child {
            margin-bottom: 0;
        }

        /* Solution styling */
        h5:has(+p:contains("Solution")) {
            margin-bottom: 0;
        }

        h5:has(+p:contains("Solution")) + p {
            font-weight: bold;
            color: #3c8dbc;
            border-left: 3px solid #3c8dbc;
            padding-left: 0.8rem;
            margin: 0.5rem 0 1rem;
        }

        p {
            margin-bottom: 1rem;
        }

        /* List styling */
        ul, ol {
            margin-bottom: 1rem;
            padding-left: 2.5rem;
        }

        ul li, ol li {
            margin-bottom: 0.5rem;
        }

        /* Code blocks */
        .code-box {
            background-color: #f6f8fa;
            border-radius: 6px;
            overflow: hidden;
            margin: 1rem 0 1.5rem;
            border: 1px solid #e1e4e8;
        }

        .code-header {
            font-family: SFMono-Regular, Consolas, "Liberation Mono", Menlo, monospace;
            font-size: 0.75rem;
            color: #6a737d;
            padding: 0.3rem 0 0rem 0.3rem;
            border-bottom: 1px solid #e1e4e8;
            background-color: #fafbfc;
        }

        .code-header a {
            color: #6a737d;
            text-decoration: none;
        }

        .code-header a:hover {
            text-decoration: underline;
            color: #0366d6;
        }

        /* Standalone code blocks (triple backticks) */
        .codehilite {
            background-color: #f6f8fa;
            border-radius: 6px;
            overflow-x: auto;
            margin: 1rem 0 1.5rem;
            border: 1px solid #e1e4e8;
        }

        /* When inside a code-box, remove default styling */
        .code-box .codehilite {
            margin: 0;
            padding: 0;
            border: none;
            border-radius: 0;
        }

        /* Adjust padding for code blocks inside code-box */
        .code-box .codehilite pre {
            padding: 0.2rem 0 0.3rem 0.3rem;
            overflow-x: auto;
            margin: 0;
        }

        /* Normal padding for standalone code blocks */
        .codehilite pre {
            padding: 1rem;
            overflow-x: auto;
            margin: 0;
        }

        .code-output {
            font-family: SFMono-Regular, Consolas, "Liberation Mono", Menlo, monospace;
            font-size: 0.75rem;
            color: #6a737d;
            padding: 0.2rem 0 0.3rem 0.3rem;
            border-top: 1px solid #e1e4e8;
            background-color: #fafbfc;
        }
        .code-output span {
            color: #de37cc;
        }

        .code-output pre {
            margin: 0;
            white-space: pre-wrap;
            font-family: SFMono-Regular, Consolas, "Liberation Mono", Menlo, monospace;
        }
        /* --- Styles for Collapsible Code Blocks --- */
        .collapsible-code {
            border: none; /* Remove default border from details */
            margin-top: 0; /* Adjust spacing if needed */
            margin-bottom: 0; /* Adjust spacing if needed */
        }

        .code-summary {
            font-family: SFMono-Regular, Consolas, "Liberation Mono", Menlo, monospace;
            font-size: 0.75rem;
            color: #6a737d;
            padding: 0.5rem 0.8rem; /* Adjusted padding */
            border-bottom: 1px solid #e1e4e8;
            background-color: #fafbfc;
            cursor: pointer;
            list-style: none; /* Hide default marker */
            display: block; /* Make it block level */
            border-radius: 6px 6px 0 0; /* Round top corners like header */
            position: relative; /* For positioning the marker */
            transition: background-color 0.1s ease-in-out;
        }

        .code-summary:hover {
            background-color: #f1f3f5; /* Slight hover effect */
        }

        /* Add custom marker */
        .code-summary::before {
            content: '►'; /* Collapsed marker */
            position: absolute;
            left: 0.8rem;
            top: 50%;
            transform: translateY(-50%);
            font-size: 0.6em;
            color: #6a737d;
            margin-right: 0.5rem;
            transition: transform 0.2s ease-in-out;
        }

        .collapsible-code[open] > .code-summary::before {
            transform: translateY(-50%) rotate(90deg); /* Expanded marker */
        }

        .collapsible-code[open] > .code-summary {
             border-bottom: 1px solid #e1e4e8; /* Ensure border shows when open */
             border-radius: 6px 6px 0 0; /* Keep top rounding when open */
        }

        /* Adjust summary content positioning relative to marker */
        .code-summary a {
            margin-left: 1.2rem; /* Space for the marker */
            color: #6a737d;
            text-decoration: none;
        }
        .code-summary a:hover {
            text-decoration: underline;
            color: #0366d6;
        }

        /* New style for the expand hint */
        .expand-hint {
            font-style: italic;
            font-size: 0.85em;
            color: #888;
            margin-left: 0.5rem;
        }

        /* Ensure content inside details has appropriate spacing/styling */
        .collapsible-code > .codehilite {
            margin: 0;
            border-radius: 0 0 6px 6px; /* Round bottom corners */
            border: none; /* Remove border from codehilite itself */
            border-top: none; /* Remove top border */
        }

        /* Since code output is now outside the details element,
           we need to adjust its styling */
        .collapsible-code + .code-output {
            border-radius: 0 0 6px 6px; /* Round bottom corners */
            margin-top: 0; /* Remove gap */
            border-top: 1px solid #e1e4e8;
        }

        /* Ensure code output has proper border when outside details */
        .code-box > .code-output {
            border-top: 1px solid #e1e4e8;
        }

        .collapsible-code > .run-racket {
             margin-left: 1rem; /* Indent run button */
             margin-bottom: 1rem; /* Add bottom margin */
        }
        /* --- End Collapsible Styles --- */

        code {
            font-family: SFMono-Regular, Consolas, "Liberation Mono", Menlo, monospace;
            font-size: 0.9em;
            padding: 0.2em 0.4em;
            background-color: #f6f8fa;
            border-radius: 3px;
        }

        .codehilite code {
            padding: 0;
            background-color: transparent;
        }

        /* Links */
        a {
            color: #0366d6;
            text-decoration: none;
        }

        a:hover {
            text-decoration: underline;
        }

        /* Run button */
        .run-racket {
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
        }

        .run-racket:hover {
            background-color: #367fa9;
            text-decoration: none;
        }

        /* Make LaTeX display nicely */
        .MathJax {
            overflow-x: auto;
            overflow-y: hidden;
        }
    """
