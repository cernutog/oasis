"""
Documentation Viewer - Standalone subprocess for displaying API documentation.
This script is launched as a separate process to avoid COM threading conflicts with Tkinter.
"""
import sys
import os

def main():
    if len(sys.argv) < 2:
        print("Usage: doc_viewer.py <html_file_path> [title]")
        sys.exit(1)
    
    html_path = sys.argv[1]
    title = sys.argv[2] if len(sys.argv) > 2 else "API Documentation"
    
    if not os.path.exists(html_path):
        print(f"Error: File not found: {html_path}")
        sys.exit(1)
    
    try:
        import webview
        window = webview.create_window(
            title,
            html_path,
            width=1200,
            height=800,
            min_size=(800, 600)
        )
        webview.start()
    except ImportError as e:
        print(f"Error: pywebview not available: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error starting viewer: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
