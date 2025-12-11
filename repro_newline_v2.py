from backend.renderer import LaTeXRenderer
import mistune

def test():
    renderer = LaTeXRenderer()
    markdown = mistune.create_markdown(renderer=renderer)
    
    print("--- Double Newline Test ---")
    source_1 = """
* 

**Text**
"""
    print(markdown(source_1))
    
    print("--- Bullet then Numbered ---")
    source_2 = """
* 
1. **Text**
"""
    print(markdown(source_2))

if __name__ == "__main__":
    test()
