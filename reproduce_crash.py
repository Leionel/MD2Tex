import requests

def reproduce():
    content = """#### **5.2 Lindeberg-Feller**

**. 定理 5.2 (Lindeberg-Feller):** 设 $\\{X_n\\}$ 相互独立...

$$ g_n(\\epsilon) := \\frac{1}{s_n^2} \\sum $$

**. 物理含义:** Lindeberg ...
"""
    try:
        resp = requests.post("http://localhost:8000/api/convert", json={
            "content": content,
            "template_type": "article"
        })
        print(f"Status: {resp.status_code}")
        print(resp.text[:500])
    except Exception as e:
        print(f"Crash: {e}")

if __name__ == "__main__":
    reproduce()
