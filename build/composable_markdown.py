# Claude 3.7 generated file
import os
import re
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
    SRC_PATTERN = re.compile(r'@src\(([\w\-\./]+\.\w+)\)')
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
            match = self.RACKET_PATTERN.search(line)
            if match:
                file_path = match.group(1)
                processed_lines = self._process_code_file(file_path, "racket", current_path)
                new_lines.extend(processed_lines)

            # Check for @src(file.ext) pattern
            elif self.SRC_PATTERN.search(line):
                match = self.SRC_PATTERN.search(line)
                file_path = match.group(1)

                # Determine the language based on file extension
                ext = os.path.splitext(file_path)[1].lower()
                lang = "racket" if ext == ".rkt" else ext[1:]  # Remove the dot

                processed_lines = self._process_code_file(file_path, lang, current_path)
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

    def _process_code_file(self, file_path, language, current_dir=None):
        """Process a code file and return lines with a code block."""
        if current_dir and not os.path.isabs(file_path):
            # If we're processing an imported file, resolve path relative to that file
            current_base = current_dir
        else:
            current_base = self.base_path

        full_path = os.path.join(current_base, file_path)
        result = []

        try:
            with open(full_path, 'r', encoding='utf-8') as f:
                code = f.read()

            # Start code box
            result.append('<div class="code-box">')

            # Add code header with filename and link
            if self.show_filename:
                url_path = file_path
                code_header = f'<div class="code-header"><a href="{url_path}" download>{file_path}</a></div>'
                result.append(code_header)

            # Create markdown code block
            result.append(f"```{language}")
            result.extend(code.splitlines())
            result.append("```")

            # Check for output file
            if self.show_output and (language == "racket" or language == "rkt"):
                output_path = os.path.splitext(full_path)[0] + ".out"
                if os.path.exists(output_path):
                    with open(output_path, 'r', encoding='utf-8') as f:
                        output = f.read()

                    # Add output section
                    result.append('<div class="code-output">')
                    result.append('Output:')
                    result.append('```')
                    result.extend(output.splitlines())
                    result.append('```')
                    result.append('</div>')

            # Add run link if configured and it's a Racket file
            if self.run_link and (language == "racket" or language == "rkt"):
                run_url = f"{self.sandbox_url.rstrip('/')}/?code={file_path}"
                result.append(f"<a href='{run_url}' class='run-racket' target='_blank'>▶ Run code</a>")

            # Close code box - only once regardless of output
            result.append('</div>')

        except FileNotFoundError:
            result.append(f"> ⚠️ Error: File not found: `{file_path}`")
        except Exception as e:
            result.append(f"> ⚠️ Error loading file: `{file_path}`: {str(e)}")

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

            return result

        except FileNotFoundError:
            return [f"> ⚠️ Error: Markdown file not found: `{file_path}`"]
        except Exception as e:
            return [f"> ⚠️ Error importing markdown file: `{file_path}`: {str(e)}"]

def makeExtension(**kwargs):
    return ComposableMarkdownExtension(**kwargs)
