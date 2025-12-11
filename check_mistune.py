import mistune
try:
    print("Mistune version:", mistune.__version__)
    print("PLUGINS keys:", list(mistune.PLUGINS.keys()))
except Exception as e:
    print("Error checking keys:", e)

try:
    from mistune.plugins.math import math
    print("Math plugin imported successfully")
except ImportError:
    print("Could not import mistune.plugins.math")
