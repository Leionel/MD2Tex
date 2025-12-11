from backend.renderer import LaTeXRenderer
import mistune

def test():
    renderer = LaTeXRenderer()
    markdown = mistune.create_markdown(renderer=renderer)
    
    print("--- Start Test ---")
    output = markdown("* **Bold**: Text")
    print(output)
    print("--- End Test ---")

if __name__ == "__main__":
    test()
