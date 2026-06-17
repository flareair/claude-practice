---
name: docx
description: Convert a file (Markdown, HTML, or plain text) to .docx using pandoc. Use whenever the user asks to convert a file to Word/docx format, export a proposal or report as a Word document, or save output as .docx.
---

# Convert to DOCX

## Steps

1. **Identify the source file** from the user's request or the most recently referenced output file.

2. **Determine the output path** — same directory and base name as the source, with the extension changed to `.docx`. If the user specifies a different output path, use that instead.

3. **Check pandoc is available:**
   ```bash
   which pandoc
   ```
   If not found, tell the user to install it: `brew install pandoc` (macOS) or `sudo apt install pandoc` (Linux).

4. **Run the conversion:**
   ```bash
   pandoc "<source_file>" -o "<output_file>.docx"
   ```

5. **Verify the output** with `ls -lh <output_file>.docx` and confirm the file size is non-zero.

6. **Report back** with the output path and file size.

## Notes

- For Markdown inputs, pandoc preserves headings, tables, bold/italic, and code blocks.
- If the user wants a custom Word template applied, use `--reference-doc=<template.docx>`.
- No extra flags are needed for standard Markdown → DOCX conversions.
