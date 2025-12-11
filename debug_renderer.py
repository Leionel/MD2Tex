from backend.renderer import LaTeXRenderer
import mistune

def test_complex_content():
    content = """
    * **公式** (描述波长的改变量):
    ### 4. 玻尔氢原子理论
    1. **定态假设**
    2. **频率条件**
    $$ h \nu = E_m - E_n $$
    3. **角动量量子化**
    $$ L = mvr = n \hbar $$
    ---
    # 第22章 量子力学基础
    """
    
    try:
        renderer = LaTeXRenderer()
        markdown = mistune.create_markdown(renderer=renderer)
        output = markdown(content)
        print("--- Output ---")
        print(output)
        print("--- End Output ---")
    except Exception as e:
        print("CRASHED:", e)
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_complex_content()
