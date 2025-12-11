from backend.renderer import LaTeXRenderer
import mistune
from mistune.plugins.table import table as table_plugin

def test():
    renderer = LaTeXRenderer()
    markdown = mistune.create_markdown(
        renderer=renderer, 
        plugins=[table_plugin]
    )
    
    print("--- Standard Table ---")
    source_1 = """
| Header 1 | Header 2 |
| -------- | -------- |
| Cell 1   | Cell 2   |
"""
    print(markdown(source_1))
    
    print("--- Compact Table (No surrounding newlines) ---")
    source_2 = "Text\n| H1 | H2 |\n|--|--|\n| C1 | C2 |"
    print(markdown(source_2))

    print("--- Malformed Table? ---")
    source_3 = """
| H1 | H2 |
|--|--|
| C1 | C2
"""
    print(markdown(source_3))

if __name__ == "__main__":
    test()
