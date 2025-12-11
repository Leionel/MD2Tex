from backend.renderer import LaTeXRenderer
import mistune
from mistune.plugins.math import math as math_plugin
from mistune.plugins.table import table as table_plugin

def test_math():
    renderer = LaTeXRenderer()
    markdown = mistune.create_markdown(
        renderer=renderer, 
        plugins=[math_plugin, table_plugin] 
    )
    
    content = "$$ E = mc^2 $$"
    output = markdown(content)
    
    print("--- Input ---")
    print(content)
    print("--- Output ---")
    print(output)
    
    expected = "\\[ E = mc^2 \\]"
    if expected in output:
        print("✅ SUCCESS: Found \\[ ... \\]")
    else:
        print(f"❌ FAILURE: Expected {expected}, got something else.")

if __name__ == "__main__":
    test_math()
