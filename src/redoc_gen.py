import os
import sys


class RedocGenerator:
    def __init__(self, resource_dir=None):
        if resource_dir is None:
            if getattr(sys, "frozen", False):
                self.resource_dir = os.path.join(sys._MEIPASS, "src", "resources")
            else:
                self.resource_dir = os.path.join(
                    os.path.dirname(os.path.abspath(__file__)), "resources"
                )
        else:
            self.resource_dir = resource_dir

        self.js_path = os.path.join(self.resource_dir, "redoc.standalone.js")

    def get_html_content(self, oas_content_yaml):
        """
        Generates a self-contained HTML string with embedded OAS spec and Redoc JS.
        Works completely offline.
        """
        # Read the bundled Redoc JS
        js_content = ""
        try:
            with open(self.js_path, "r", encoding="utf-8") as f:
                js_content = f.read()
        except FileNotFoundError:
            return "<html><body><h1>Error: redoc.standalone.js not found</h1></body></html>"

        # Escape closing script tags in YAML to prevent breaking HTML
        safe_yaml = oas_content_yaml.replace("</script>", "<\\/script>")

        # Parse YAML to JSON in Python and embed as JSON
        # This avoids Redoc treating string as file path
        import yaml
        import json
        from datetime import datetime, date

        # Custom encoder to handle datetime objects
        class DateTimeEncoder(json.JSONEncoder):
            def default(self, obj):
                if isinstance(obj, (datetime, date)):
                    return obj.isoformat()
                return super().default(obj)

        try:
            spec_obj = yaml.safe_load(oas_content_yaml)
            spec_json = json.dumps(spec_obj, cls=DateTimeEncoder)
        except Exception as e:
            return f"<html><body><h1>Error parsing YAML: {e}</h1></body></html>"

        html_template = f"""<!DOCTYPE html>
<html>
<head>
    <title>API Documentation</title>
    <meta charset="utf-8"/>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body {{ margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif; }}
        #loading {{ padding: 40px; text-align: center; color: #666; }}
        
        /* Toolbar - matches CustomTkinter dark theme */
        #doc-toolbar {{
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            height: 44px;
            background: #2B2B2B;
            display: flex;
            align-items: center;
            padding: 0 12px;
            z-index: 10000;
            box-shadow: 0 1px 3px rgba(0,0,0,0.4);
            gap: 8px;
        }}
        
        /* Button base - matches OASIS Petrol Blue */
        #doc-toolbar button {{
            background: #0A809E;
            color: white;
            border: none;
            padding: 7px 16px;
            border-radius: 6px;
            cursor: pointer;
            font-size: 13px;
            font-weight: 500;
            display: flex;
            align-items: center;
            gap: 6px;
            transition: background 0.15s ease;
        }}
        
        #doc-toolbar button:hover {{
            background: #076075;
        }}
        
        /* Snap button when unsnapped */
        #doc-toolbar button.unsnapped {{
            background: #5A5A5A;
        }}
        
        #doc-toolbar button.unsnapped:hover {{
            background: #4A4A4A;
        }}
        
        #doc-toolbar .spacer {{
            flex: 1;
        }}
        
        #doc-toolbar .title {{
            color: #DCE4EE;
            font-size: 13px;
            font-weight: 500;
        }}
        
        /* Offset Redoc content for toolbar */
        redoc {{
            display: block;
            padding-top: 48px;
        }}
        
        @media print {{
            #doc-toolbar {{ display: none !important; }}
            redoc {{ padding-top: 0 !important; }}
        }}
    </style>
</head>
<body>
    <!-- Toolbar with pywebview API integration -->
    <div id="doc-toolbar">
        <button id="btn-snap" onclick="toggleSnap()" title="Dock viewer to main window">
            📌 Undock
        </button>
        <button id="btn-sync-editor" onclick="syncToEditor()" title="Find this section in YAML editor">
            📍 Find in YAML
        </button>
        <button onclick="printDoc()" title="Print documentation">
            🖨️ Print
        </button>
        <button onclick="saveAsHtml()" title="Save as HTML file">
            💾 Save HTML
        </button>
        <div class="spacer"></div>
        <span class="title">API Documentation</span>
    </div>
    
    <div id="loading">Loading documentation...</div>
    <redoc id="redoc-container"></redoc>
    
    <script>
        // Spec as parsed JSON object
        var apiSpec = {spec_json};
        
        // Snap state (synced with Python via pywebview API)
        var isSnapped = true;
        
        function updateSnapButton() {{
            var btn = document.getElementById('btn-snap');
            if (!btn) return;
            if (isSnapped) {{
                btn.textContent = '📌 Undock';
                btn.className = '';
            }} else {{
                btn.textContent = '🔗 Dock';
                btn.className = 'unsnapped';
            }}
        }}

        // Expose function for Python to call globally
        window.setSnapState = function(state) {{
            console.log('setSnapState called from Python:', state);
            if (isSnapped !== state) {{
                isSnapped = state;
                updateSnapButton();
            }}
        }};
        
        function toggleSnap() {{
            // Call Python API via pywebview
            if (window.pywebview && window.pywebview.api) {{
                window.pywebview.api.toggle_snap().then(function(newState) {{
                    isSnapped = newState;
                    updateSnapButton();
                }});
            }} else {{
                // Fallback if pywebview API not available
                isSnapped = !isSnapped;
                updateSnapButton();
            }}
        }}
        
        function printDoc() {{
            window.print();
        }}
        
        function syncToEditor() {{
            // Extract section info from Redoc's active menu item
            var operationId = "";
            var pathHash = "";
            var debugInfo = "";
            
            // Strategy 1: Try .menu-item.active (older Redoc)
            var activeEl = document.querySelector('.menu-item.active');
            debugInfo += "S1(.menu-item.active): " + (activeEl ? "found" : "null") + "; ";
            
            // Strategy 2: Try [class*="active"] in the sidebar/menu area
            if (!activeEl) {{
                activeEl = document.querySelector('[class*="menu"] [class*="active"]');
                debugInfo += "S2([class*=active]): " + (activeEl ? "found" : "null") + "; ";
            }}
            
            // Strategy 3: Try data-item-id attributes
            if (!activeEl) {{
                activeEl = document.querySelector('[data-item-id].-active, [data-item-id].active');
                debugInfo += "S3(data-item-id): " + (activeEl ? "found" : "null") + "; ";
            }}
            
            // If we found an active element, try to extract the operationId
            if (activeEl) {{
                // Look for any link inside or on the element
                var link = activeEl.querySelector('a[href^="#"]') || 
                           activeEl.closest('a[href^="#"]') ||
                           activeEl;
                
                var href = link.getAttribute ? link.getAttribute('href') : "";
                if (href && href.startsWith('#')) {{
                    pathHash = href;
                    if (href.includes('/operations/')) {{
                        operationId = href.split('/operations/')[1];
                    }} else if (href.includes('/paths/')) {{
                        // Extract path for paths like #/paths/~1accounts/get
                        var pathPart = href.split('/paths/')[1];
                        if (pathPart) {{
                            operationId = pathPart.replace(/~1/g, '/');
                        }}
                    }}
                }}
                
                // Also check data-item-id attribute
                if (!operationId) {{
                    var dataId = activeEl.getAttribute('data-item-id') || 
                                 activeEl.getAttribute('data-id') ||
                                 activeEl.id;
                    if (dataId) {{
                        operationId = dataId;
                    }}
                }}
                
                debugInfo += "href: " + (href || "none") + "; ";
            }}
            
            // Strategy 4: Fallback to current URL hash
            if (!pathHash && window.location.hash) {{
                pathHash = window.location.hash;
                // Handle both /operations/ (plural) and /operation/ (singular) patterns
                if (pathHash.includes('/operation/')) {{
                    // Format: #tag/TagName/operation/operationId
                    operationId = pathHash.split('/operation/')[1];
                }} else if (pathHash.includes('/operations/')) {{
                    operationId = pathHash.split('/operations/')[1];
                }}
                debugInfo += "S4(location.hash): " + pathHash + "; opId: " + operationId + "; ";
            }}
            
            // Send to Python with debug info
            if (window.pywebview && window.pywebview.api) {{
                window.pywebview.api.sync_editor({{
                    hash: pathHash,
                    operationId: operationId,
                    sectionTitle: activeEl ? activeEl.textContent.trim().substring(0, 80) : "",
                    debug: debugInfo
                }}).then(function(res) {{
                    console.log('Sync result:', res);
                }});
            }}
        }}
        
        // Expose function for Python to scroll Redoc
        window.scrollToPath = function(path) {{
            console.log('scrollToPath called from Python:', path);
            window.focus();
            
            // Extract operationId from path (could be #/operations/xyz or just xyz)
            var operationId = path;
            if (path.includes('/operations/')) {{
                operationId = path.split('/operations/')[1];
            }} else if (path.includes('/operation/')) {{
                operationId = path.split('/operation/')[1];
            }} else if (path.startsWith('#')) {{
                operationId = path.substring(1);
            }}
            
            console.log('Looking for operationId:', operationId);
            
            // Strategy 1: Find menu item with href containing the operationId and click it
            var menuLinks = document.querySelectorAll('a[href*="' + operationId + '"]');
            for (var i = 0; i < menuLinks.length; i++) {{
                var link = menuLinks[i];
                console.log('Found link:', link.href);
                link.click();
                return;
            }}
            
            // Strategy 2: Try setting hash with /operation/ format (singular)
            var newHash = '#tag/---/operation/' + operationId;
            // First, find any link to extract the correct tag
            var allLinks = document.querySelectorAll('a[href*="/operation/"]');
            for (var j = 0; j < allLinks.length; j++) {{
                if (allLinks[j].href.includes(operationId)) {{
                    window.location.hash = allLinks[j].getAttribute('href');
                    return;
                }}
            }}
            
            // Strategy 3: Fallback - just set the hash directly
            console.log('Fallback: setting hash directly');
            window.location.hash = path;
        }};
        
        function saveAsHtml() {{
            // Clone the document to modify without affecting the view
            var clonedDoc = document.documentElement.cloneNode(true);
            
            // Remove toolbar from clone
            var toolbar = clonedDoc.querySelector('#doc-toolbar');
            if (toolbar) {{
                toolbar.parentNode.removeChild(toolbar);
            }}
            
            // Remove toolbar padding from redoc in clone
            var redocEl = clonedDoc.querySelector('redoc');
            if (redocEl) {{
                redocEl.style.paddingTop = '0';
            }}
            
            // Remove toolbar-related JS (optional but cleaner)
            var scripts = clonedDoc.querySelectorAll('script');
            // Keep only the Redoc script
            
            var htmlContent = '<!DOCTYPE html>\\n' + clonedDoc.outerHTML;
            var blob = new Blob([htmlContent], {{ type: 'text/html' }});
            var url = URL.createObjectURL(blob);
            var a = document.createElement('a');
            a.href = url;
            a.download = 'api_documentation.html';
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            URL.revokeObjectURL(url);
        }}
        
        // Initialize snap state from Python
        document.addEventListener('DOMContentLoaded', function() {{
            updateSnapButton(); // Initial render
            if (window.pywebview && window.pywebview.api) {{
                window.pywebview.api.get_snap_state().then(function(state) {{
                    isSnapped = state;
                    updateSnapButton();
                }});
            }}
        }});
    </script>
    
    <script>
{js_content}
    </script>
    
    <script>
        document.addEventListener('DOMContentLoaded', function() {{
            try {{
                var container = document.getElementById('redoc-container');
                document.getElementById('loading').style.display = 'none';
                
                Redoc.init(apiSpec, {{
                    scrollYOffset: 50,
                    hideDownloadButton: false,
                    expandResponses: "200,201"
                }}, container);
            }} catch(e) {{
                document.getElementById('loading').innerHTML = 
                    '<h2 style="color:red;">Error loading documentation</h2><p>' + e.message + '</p>';
            }}
        }});
    </script>
</body>
</html>
"""
        return html_template
