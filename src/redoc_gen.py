import os
import sys

class RedocGenerator:
    def __init__(self, resource_dir=None):
        if resource_dir is None:
            if getattr(sys, 'frozen', False):
                self.resource_dir = os.path.join(sys._MEIPASS, 'src', 'resources')
            else:
                self.resource_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'resources')
        else:
            self.resource_dir = resource_dir

        self.js_path = os.path.join(self.resource_dir, 'redoc.standalone.js')

    def get_html_content(self, oas_content_yaml):
        """
        Generates a self-contained HTML string with embedded OAS spec and Redoc JS.
        Works completely offline.
        """
        # Read the bundled Redoc JS
        js_content = ""
        try:
            with open(self.js_path, 'r', encoding='utf-8') as f:
                js_content = f.read()
        except FileNotFoundError:
            return "<html><body><h1>Error: redoc.standalone.js not found</h1></body></html>"
        
        # Escape closing script tags in YAML to prevent breaking HTML
        safe_yaml = oas_content_yaml.replace('</script>', '<\\/script>')
        
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
        
        html_template = f'''<!DOCTYPE html>
<html>
<head>
    <title>API Documentation</title>
    <meta charset="utf-8"/>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body {{ margin: 0; padding: 0; font-family: sans-serif; }}
        #loading {{ padding: 40px; text-align: center; color: #666; }}
    </style>
</head>
<body>
    <div id="loading">Loading documentation...</div>
    <redoc id="redoc-container"></redoc>
    
    <script>
        // Spec as parsed JSON object (not string)
        var apiSpec = {spec_json};
    </script>
    
    <script>
{js_content}
    </script>
    
    <script>
        document.addEventListener('DOMContentLoaded', function() {{
            try {{
                var container = document.getElementById('redoc-container');
                document.getElementById('loading').style.display = 'none';
                
                // Pass the parsed object directly to Redoc
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
'''
        return html_template

