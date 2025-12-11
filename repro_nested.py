from backend.renderer import LaTeXRenderer
import mistune

def test():
    renderer = LaTeXRenderer()
    markdown = mistune.create_markdown(renderer=renderer)
    
    print("--- Start Nested Test ---")
    # Using raw strings to avoid escape warnings
    source = r"""
* Item 1
    * Subitem A
    * Subitem B
* Item 2
"""
    output = markdown(source)
    print(output)
    print("--- End Nested Test ---")

if __name__ == "__main__":
    test()
