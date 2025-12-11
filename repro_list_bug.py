from backend.renderer import LaTeXRenderer
import mistune
from mistune.plugins.table import table as table_plugin

def test_list_rendering():
    renderer = LaTeXRenderer()
    # Disable plugins to check for interference
    markdown = mistune.create_markdown(
        renderer=renderer, 
        plugins=[] # table_plugin removed
    )
    
    # Text case 1: Simple list with bold
    source_1 = """
* **Bold Text**: Normal text
"""
    print("--- Test 1 (Simple) ---")
    print(markdown(source_1))
    
    # Test case 2: List with Math (inline and block potential)
    source_2 = """
* **Math Case**: $E=mc^2$ inside list
* $$ \sum $$ Block math in list
"""
    print("--- Test 2 (Math) ---")
    print(markdown(source_2))

    # Test case 3: Nested indent style from user screenshot
    # Check if weird indentation causes empty items
    source_3 = """
* Item 1
  * Subitem 1
  * Subitem 2
"""
    print("--- Test 3 (Nested) ---")
    print(markdown(source_3))

    # Test case 4: User specific content approximation
    source_4 = """
* **判定收敛性**: $ \sum P(A_n) $
* **(1)** $ \alpha > 1 $: ** $ \sum P(A_n) < \infty $
"""
    print("--- Test 4 (User Case) ---")
    print(markdown(source_4))

if __name__ == "__main__":
    test_list_rendering()
