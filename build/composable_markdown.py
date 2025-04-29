# Claude 3.7 +Gemini generated file
import os
import re
import html  # Import the html module for escaping
from markdown.extensions import Extension
from markdown.preprocessors import Preprocessor

class ComposableMarkdownExtension(Extension):
    def __init__(self, **kwargs):
        self.config = {
            'base_path': ['.', 'Base path for all imported files'],
            'run_link': [False, 'Add a link to run Racket code in a sandbox'],
            'sandbox_url': ['https://racket.run/', 'URL to the Racket sandbox'],
            'show_filename': [True, 'Show the filename above code blocks'],
            'process_imports': [True, 'Process nested imports in imported markdown files'],
            'show_output': [True, 'Show output from Racket files if available']
        }
        super(ComposableMarkdownExtension, self).__init__(**kwargs)

    def extendMarkdown(self, md):
        md.registerExtension(self)

        # Register our processor before other processors
        md.preprocessors.register(ComposableMarkdownPreprocessor(md, self.getConfigs()),
                                'composable_markdown',
                                175)  # Priority higher than fenced_code

class ComposableMarkdownPreprocessor(Preprocessor):
    # Legacy pattern for compatibility
    RACKET_PATTERN = re.compile(r'{{% racket src="([\w\-\./]+\.rkt)" %}}')

    # New unified patterns
    # Updated SRC_PATTERN to capture optional second argument (collapsible/collapsed)
    SRC_PATTERN = re.compile(r'@src\(([\w\-\./]+\.\w+)(?:,\s*(\w+))?\)')
    IMPORT_PATTERN = re.compile(r'@import\(([\w\-\./]+\.md)\)')

    # Track imported files to prevent circular imports
    imported_files = set()

    def __init__(self, md, config):
        super(ComposableMarkdownPreprocessor, self).__init__(md)
        self.base_path = config['base_path']
        self.run_link = config['run_link']
        self.sandbox_url = config['sandbox_url']
        self.show_filename = config['show_filename']
        self.process_imports = config['process_imports']
        self.show_output = config['show_output']
        self.md = md

    def run(self, lines):
        # Reset imported files for each new document
        ComposableMarkdownPreprocessor.imported_files = set()
        return self._process_lines(lines)

    def _process_lines(self, lines, current_path=None):
        new_lines = []
        i = 0
        while i < len(lines):
            line = lines[i]

            # Check for {{% racket src="file.rkt" %}} pattern (legacy)
            match_legacy = self.RACKET_PATTERN.search(line)
            # Check for @src(file.ext, arg) pattern
            match_src = self.SRC_PATTERN.search(line)

            if match_legacy:
                file_path = match_legacy.group(1)
                # Legacy doesn't support collapse state
                processed_lines = self._process_code_file(file_path, "racket", current_path, collapse_state=None)
                new_lines.extend(processed_lines)

            elif match_src:
                file_path = match_src.group(1)
                collapse_arg = match_src.group(2) # Capture the second argument (collapsible/collapsed or None)

                # Validate collapse_arg
                valid_collapse_states = ['collapsible', 'collapsed']
                collapse_state = collapse_arg if collapse_arg in valid_collapse_states else None

                # Determine the language based on file extension
                ext = os.path.splitext(file_path)[1].lower()
                lang = "racket" if ext == ".rkt" else ext[1:]  # Remove the dot

                processed_lines = self._process_code_file(file_path, lang, current_path, collapse_state)
                new_lines.extend(processed_lines)

            # Check for @import(file.md) pattern
            elif self.IMPORT_PATTERN.search(line):
                match = self.IMPORT_PATTERN.search(line)
                file_path = match.group(1)

                # Process the markdown import
                imported_lines = self._import_markdown(file_path, current_path or self.base_path)
                new_lines.extend(imported_lines)

            else:
                new_lines.append(line)

            i += 1

        return new_lines

    def _process_code_file(self, file_path, language, current_dir=None, collapse_state=None):
        """Process a code file and return lines with a code block, potentially collapsible."""
        if current_dir and not os.path.isabs(file_path):
            current_base = current_dir
        else:
            current_base = self.base_path

        full_path = os.path.join(current_base, file_path)
        result = []
        error_occurred = False

        try:
            with open(full_path, 'r', encoding='utf-8') as f:
                code = f.read()
        except FileNotFoundError:
            result.append(f"> ⚠️ Error: File not found: `{file_path}`")
            error_occurred = True
        except Exception as e:
            result.append(f"> ⚠️ Error loading file: `{file_path}`: {str(e)}")
            error_occurred = True

        if error_occurred:
            return result

        # --- Start code block generation ---
        result.append('<div class="code-box">')

        # --- Prepare inner content (code, output, run link) ---
        inner_content = []

        # Create markdown code block
        inner_content.append(f"```{language}")
        inner_content.extend(code.splitlines())
        inner_content.append("```")

        # Check for output file
        output_content = []
        if self.show_output and (language == "racket" or language == "rkt"):
            output_path = os.path.splitext(full_path)[0] + ".out"
            if os.path.exists(output_path):
                with open(output_path, 'r', encoding='utf-8') as f:
                    output = f.read()
                # Use raw HTML for output block to ensure it's inside details if needed
                output_content.append('<div class="code-output">')
                output_content.append('<span>Output:</span>')
                # Escape HTML characters in the output to prevent XSS
                output_content.append(f'<pre>{html.escape(output)}</pre>')
                output_content.append('</div>')
        inner_content.extend(output_content) # Add output after code block markdown

        # Add run link if configured and it's a Racket file
        run_link_html = ""
        if self.run_link and (language == "racket" or language == "rkt"):
            run_url = f"{self.sandbox_url.rstrip('/')}/?code={file_path}"
            run_link_html = f"<a href='{run_url}' class='run-racket' target='_blank'>▶ Run code</a>"
            # Append raw HTML for the run link
            inner_content.append(run_link_html)

        # --- Wrap content based on collapse_state ---
        if collapse_state:
            # Use <details> and <summary>
            open_attribute = " open" if collapse_state == 'collapsible' else ""
            result.append(f'<details class="collapsible-code"{open_attribute}>')

            # Create summary (acts like the header)
            summary_content = "Code" # Default text
            if self.show_filename:
                url_path = file_path
                summary_content = f'<a href="{url_path}">{file_path}</a>'
            result.append(f'<summary class="code-summary">{summary_content}</summary>')

            # Add the inner content (code markdown, output html, run link html)
            result.extend(inner_content)

            result.append('</details>')
        else:
            # Standard non-collapsible block
            # Add code header with filename and link (if not collapsible)
            if self.show_filename:
                url_path = file_path
                code_header = f'<div class="code-header"><a href="{url_path}">{file_path}</a></div>'
                result.append(code_header)

            # Add the inner content directly
            result.extend(inner_content)

        # Close code box
        result.append('</div>')

        return result


    def _import_markdown(self, file_path, current_dir):
        """Import a markdown file and process its contents."""
        # Normalize the path
        if not os.path.isabs(file_path) and current_dir != self.base_path:
            # If the import is in an already imported file, resolve path relative to that file
            full_path = os.path.normpath(os.path.join(current_dir, file_path))
        else:
            # Otherwise resolve relative to base path
            full_path = os.path.normpath(os.path.join(self.base_path, file_path))

        # Check for circular imports
        if full_path in ComposableMarkdownPreprocessor.imported_files:
            return [f"> ⚠️ Circular import detected: `{file_path}`"]

        # Add to imported files set
        ComposableMarkdownPreprocessor.imported_files.add(full_path)

        try:
            with open(full_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Split into lines
            md_lines = content.splitlines()

            # Process nested imports if configured
            if self.process_imports:
                import_dir = os.path.dirname(full_path)
                md_lines = self._process_lines(md_lines, import_dir)

            # Add a comment to show where the import starts
            result = [f"<!-- Begin import: {file_path} -->"]
            result.extend(md_lines)
            result.append(f"<!-- End import: {file_path} -->")

            # Remove file from set after processing to allow re-import in different branches
            ComposableMarkdownPreprocessor.imported_files.remove(full_path)

            return result

        except FileNotFoundError:
            # Remove file from set if not found, otherwise it blocks subsequent attempts
            if full_path in ComposableMarkdownPreprocessor.imported_files:
                 ComposableMarkdownPreprocessor.imported_files.remove(full_path)
            return [f"> ⚠️ Error: Markdown file not found: `{file_path}`"]
        except Exception as e:
             # Remove file from set on error
            if full_path in ComposableMarkdownPreprocessor.imported_files:
                 ComposableMarkdownPreprocessor.imported_files.remove(full_path)
            return [f"> ⚠️ Error importing markdown file: `{file_path}`: {str(e)}"]

def makeExtension(**kwargs):
    return ComposableMarkdownExtension(**kwargs)
