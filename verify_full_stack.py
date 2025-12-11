import requests
import sys

def verify():
    print("Verifying MD2TeX API...")
    
    # Test Content with all features
    content = """
# 第一章 测试章节

> **定理 (测试)**
> 这是一个定理框。
> $$ E = mc^2 $$

> **问题**
> 这是一个问题框。

1. 列表项
"""

    try:
        response = requests.post(
            "http://localhost:8000/api/convert",
            json={
                "content": content,
                "template_type": "article",
                "author": "Verifier"
            }
        )
        
        if response.status_code != 200:
            print(f"❌ API Failed with status {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
        json_resp = response.json()
        latex = json_resp.get("latex_code", "")
        
        print("--- Received LaTeX ---")
        print(latex[:500] + "...") # Print first 500 chars
        print("----------------------")
        
        # Check for key features
        checks = {
            "Chinese Support": "{ctexart}",
            "Theorem Box": "\\begin{kbox}",
            "Question Box": "\\begin{qbox}",
            "Math Formula": "E = mc^2",
            "Jinja2 Template": "\\title{ Converted Document }"
        }
        
        all_passed = True
        for name, key in checks.items():
            if key in latex:
                print(f"✅ {name}: Verified")
            else:
                print(f"❌ {name}: NOT FOUND")
                all_passed = False
                
        if all_passed:
            print("\n🎉 ALL CHECKS PASSED!")
            return True
        else:
            print("\n⚠️ SOME CHECKS FAILED.")
            return False
            
    except Exception as e:
        print(f"❌ Connection Error: {e}")
        return False

if __name__ == "__main__":
    verify()
