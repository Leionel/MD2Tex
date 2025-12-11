import mistune
from mistune import HTMLRenderer

class LaTeXRenderer(HTMLRenderer):
    NAME = 'latex'

    def __init__(self):
        super().__init__(escape=False)

    def paragraph(self, text):
        return f"{text}\n\n"

    def heading(self, text, level, **kwargs):
        cmds = {
            1: 'part',         # # -> Part
            2: 'section',      # ## -> Section
            3: 'subsection',   # ### -> Subsection
            4: 'subsubsection',# #### -> Subsubsection
            5: 'paragraph',    # ##### -> Paragraph
        }
        cmd = cmds.get(level, 'textbf')
        
        # Smart Label Generation
        # Generate label from text: "My Title 123" -> "sec:my_title_123"
        import re
        slug = re.sub(r'[^a-zA-Z0-9]+', '_', text.lower()).strip('_')
        label = f"sec:{slug}"
        
        return f"\\{cmd}{{{text}}}\\label{{{label}}}\n"

    def emphasis(self, text, **kwargs):
        return f"\\textit{{{text}}}"

    def strong(self, text, **kwargs):
        return f"\\textbf{{{text}}}"

    def list(self, body, ordered, **kwargs):
        env = 'enumerate' if ordered else 'itemize'
        return f"\\begin{{{env}}}\n{body}\\end{{{env}}}\n"

    def list_item(self, text, **kwargs):
        return f"  \\item {text}\n"

    def block_code(self, code, info=None):
        # Map languages to Listings 'language'
        lang = info if info else ''
        # Simple mapping or pass through
        if lang.lower() in ['py', 'python']:
            lang = 'Python'
        elif lang.lower() in ['c', 'cpp', 'c++']:
            lang = 'C++'
        
        lang_opt = f"[language={lang}, title={lang}]" if lang else ""
        return f"\\begin{{lstlisting}}{lang_opt}\n{code}\\end{{lstlisting}}\n"

    def codespan(self, text):
        return f"\\texttt{{{text}}}"

    def link(self, text, url, title=None, **kwargs):
        # Mistune 3.x: text, url, title
        if url.startswith('#'):
             # Internal link -> \ref
             # Slugify url content? usually url is "#slug"
             ref_name = url[1:] # remove #
             # If markdown was "#My Header", link might be "#my-header" (standard) 
             # But our label generator above converts "My Header" to "sec:my_header"
             # We need to guess the label name or trust the user.
             # Let's assume user writes [Link](#sec:my_header) if they want explicit control?
             # Or better: [Link](#my header) -> ref{sec:my_header}
             
             import re
             # Remove sec: prefix if present to avoid double prefixing? 
             # Or strictly follow our label convention.
             # Let's try to match the slug logic:
             slug = re.sub(r'[^a-zA-Z0-9]+', '_', ref_name.lower()).strip('_')
             
             # Heuristic: try adding prefixes?
             # For now, just output a generic ref and let user handle ID?
             # No, auto-slug is better.
             # If user links to a section, we prefix 'sec:'.
             label = f"sec:{slug}"
             return f"\\hyperref[{label}]{{{text}}}" # hyperref is safer than ref for text link
        
        return f"\\href{{{url}}}{{{text}}}"

    def image(self, text, url, title=None, **kwargs):
        # Mistune 3.x: text (alt), url (src), title
        src = url
        alt = text
        
        # Generate label from alt text
        import re
        slug = re.sub(r'[^a-zA-Z0-9]+', '_', alt.lower()).strip('_')
        label = f"fig:{slug}"
        
        return f"""
\\begin{{figure}}[h]
    \\centering
    \\includegraphics[width=0.8\\textwidth]{{{src}}}
    \\caption{{{alt}}}
    \\label{{{label}}}
\\end{{figure}}
"""

    def block_quote(self, text):
        # Heuristic: If text starts with specific keywords, use specific boxes
        # Otherwise use a generic quote box
        
        # Check for "定理", "定义", "Knowledge"
        if any(k in text[:20] for k in ["定理", "定义", "Definition", "Theorem"]):
            # Extract title if possible? For now just wrap
            return f"\\begin{{kbox}}[知识点/定理]\n{text}\\end{{kbox}}\n"
            
        # Check for "问题", "Example", "Question"
        if any(k in text[:20] for k in ["问题", "例题", "Question", "Example"]):
            return f"\\begin{{qbox}}[问题]\n{text}\\end{{qbox}}\n"
            
        # Default nice box
        return f"\\begin{{tcolorbox}}[colback=gray!5!white,colframe=gray!50!black,title=引用]\n{text}\\end{{tcolorbox}}\n"

    def block_math(self, text):
        return f"\\[ {text} \\]"

    def inline_math(self, text):
        # Mistune logic: 
        # If input is $a$, text='a' -> Output $ a $
        # If input is $$a$$, detected as inline math? 
        #   If so, Mistune usually passes 'a' with delimiter... wait.
        #   If Mistune math plugin handles $$, it calls block_math.
        #   If Mistune treats $$ as inline math delimiter (unlikely default), 
        #   OR if it treats $$a$$ as INLINE math with delimiter $, then text='$a$'.
        
        # Let's handle the case where text ITSELF contains starting/ending $
        # This happens if parsed as $ $a$ $?
        
        clean = text.strip()
        if clean.startswith('$') and clean.endswith('$'):
            return f"\\[ {clean[1:-1]} \\]"
            
        return f"$ {text} $"

    def table(self, text):
        # Heuristic: count columns based on first row
        # Text is sequence of rows.
        # Find first occurrence of \\
        first_row = text.split(r'\\', 1)[0]
        col_count = first_row.count('&') + 1
        
        # Build col spec: |l|l|l|...
        col_spec = "|" + "l|" * max(1, col_count)
        
        return f"""
\\begin{{table}}[h]
    \\centering
    \\begin{{tabular}}{{{col_spec}}}
    \\hline
{text}    \\end{{tabular}}
\\end{{table}}
"""

    def table_head(self, text):
        # Ensure header row ends properly
        content = text.strip()
        if not content.endswith(r'\\') and not content.endswith(r'\hline'):
             if content.endswith('&'):
                 content = content[:-1]
             content += r" \\ \hline"
        return f"{content}\n"

    def table_body(self, text):
        return text

    def table_row(self, text):
        content = text.strip()
        if content.endswith('&'):
            content = content[:-1]
        return f"    {content} \\\\\n    \\hline\n"

    def table_cell(self, text, align=None, head=False, **kwargs):
        content = text
        if head:
            content = f"\\textbf{{{content}}}"
        return f"{content} &"
    
    # NOTE: Mistune v3 table rendering is complex to get right without state 
    # (knowing when it is the last cell).
    # A robust implementation would join cells.
    # For now, let's skip Table methods and let Mistune math plugin do its thing,
    # or actually, we DISABLED math/table plugins in main.py step 311 
    # except 'table' plugin was kept enabled in step 320 replacement?
    # Wait, step 320 replacement showed: plugins=[table_plugin].
    # So Table plugin IS enabled.
    # Without methods, it outputs HTML.
    # Let's add basic methods.
    
    def text(self, text):
        import re
        
        # 1. Block Math $$ ... $$ -> \[ ... \]
        # Matches $$ ... $$
        pattern_block = re.compile(r'\$\$(.*?)\$\$', re.DOTALL)
        def repl_block(match):
            content = match.group(1).strip()
            return f"\\[ {content} \\]"
        text = pattern_block.sub(repl_block, text)
        
        # 2. Inline Math $ ... $ -> $ ... $
        # Use negative lookaround to ensure we don't match $$ as two $
        # Matches $...$ where $ is NOT preceded or followed by another $
        pattern_inline = re.compile(r'(?<!\$)\$(?!\$)(.*?)(?<!\$)\$(?!\$)')
        def repl_inline(match):
            content = match.group(1).strip()
            return f"$ {content} $"
        text = pattern_inline.sub(repl_inline, text)

        return text

    def thematic_break(self):
        return "\\noindent\\rule{\\textwidth}{0.5pt}\\n"
