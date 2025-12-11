import re

def render_math_manual(text):
    # Pattern for Block Math: $$ ... $$
    # DOTALL to match newlines inside
    pattern_block = re.compile(r'\$\$(.*?)\$\$', re.DOTALL)
    
    def repl_block(match):
        content = match.group(1).strip()
        return f"\\[ {content} \\]"
    
    text = pattern_block.sub(repl_block, text)
    
    # Pattern for Inline Math: $ ... $
    # (Avoid matching $$ ... $$ which are already handled? No, already replaced)
    # Be careful not to match \[ ... \] as dollars? No, dollars are gone.
    # But wait, what if we have single $?
    
    # Simple regex for $...$
    pattern_inline = re.compile(r'\$(.*?)\$')
    
    def repl_inline(match):
        content = match.group(1).strip()
        return f"$ {content} $"
        
    text = pattern_inline.sub(repl_inline, text)
    
    return text

def test():
    samples = [
        "$$ E = mc^2 $$",
        "Hello $x$ World",
        "$$ 1+1=2 $$",
        "Double dollar at start $$ a $$ and end.",
        "Mixed: $ a $ and $$ b $$"
    ]
    
    for s in samples:
        print(f"Original: {s}")
        print(f"Rendered: {render_math_manual(s)}")
        print("-" * 20)

if __name__ == "__main__":
    test()
