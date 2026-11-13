import sys

print("Python Version:", sys.version)
print("-" * 40)

libraries = [
    "streamlit",
    "cv2",
    "PIL",
    "numpy",
    "pandas",
    "matplotlib",
    "sklearn",
    "ta",
]

for lib in libraries:
    try:
        __import__(lib)
        print(f"[✓] {lib} is installed successfully.")
    except ImportError:
        print(f"[X] {lib} is NOT installed.")

print("-" * 40)
print("Audit check completed!")