"""
Test Report Generator.

Generates HTML and text reports from pytest test results.
"""

import subprocess
import json
import os
import sys
from datetime import datetime
from pathlib import Path

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


def run_tests_with_json_output(output_file: str = "test_results.json"):
    """
    Run pytest with JSON output.
    """
    cmd = [
        sys.executable, "-m", "pytest",
        "tests/regression/",
        "-v",
        "--tb=short",
        f"--json-report",
        f"--json-report-file={output_file}",
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.returncode


def generate_html_report(json_file: str, output_file: str = "test_report.html"):
    """
    Generate an HTML report from pytest JSON output.
    """
    if not os.path.exists(json_file):
        print(f"Error: {json_file} not found")
        return False
    
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Extract summary
    summary = data.get('summary', {})
    tests = data.get('tests', [])
    
    passed = summary.get('passed', 0)
    failed = summary.get('failed', 0)
    xfailed = summary.get('xfailed', 0)
    skipped = summary.get('skipped', 0)
    total = summary.get('total', 0)
    duration = summary.get('duration', 0)
    
    # Group tests by file
    tests_by_file = {}
    for test in tests:
        file_path = test.get('nodeid', '').split('::')[0]
        if file_path not in tests_by_file:
            tests_by_file[file_path] = []
        tests_by_file[file_path].append(test)
    
    # Generate HTML
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>OAS Generation Tool - Test Report</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ 
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
            background: #0f1419;
            color: #e7e9ea;
            line-height: 1.6;
            padding: 2rem;
        }}
        .container {{ max-width: 1200px; margin: 0 auto; }}
        h1 {{ 
            font-size: 2rem; 
            margin-bottom: 1rem;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}
        .timestamp {{ color: #71767b; margin-bottom: 2rem; }}
        .summary {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 1rem;
            margin-bottom: 2rem;
        }}
        .summary-card {{
            background: #1e2732;
            border-radius: 12px;
            padding: 1.5rem;
            text-align: center;
            border: 1px solid #38444d;
        }}
        .summary-card.passed {{ border-color: #00ba7c; }}
        .summary-card.failed {{ border-color: #f4212e; }}
        .summary-card.xfailed {{ border-color: #ffd400; }}
        .summary-card .number {{
            font-size: 2.5rem;
            font-weight: bold;
        }}
        .summary-card.passed .number {{ color: #00ba7c; }}
        .summary-card.failed .number {{ color: #f4212e; }}
        .summary-card.xfailed .number {{ color: #ffd400; }}
        .summary-card .label {{ color: #71767b; }}
        
        .test-file {{
            background: #1e2732;
            border-radius: 12px;
            margin-bottom: 1rem;
            overflow: hidden;
            border: 1px solid #38444d;
        }}
        .test-file-header {{
            padding: 1rem 1.5rem;
            background: #253341;
            font-weight: 600;
            cursor: pointer;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        .test-file-header:hover {{ background: #2d3f50; }}
        .test-list {{ padding: 0.5rem 0; }}
        .test-item {{
            padding: 0.75rem 1.5rem;
            display: flex;
            align-items: center;
            gap: 1rem;
            border-bottom: 1px solid #38444d;
        }}
        .test-item:last-child {{ border-bottom: none; }}
        .test-status {{
            padding: 0.25rem 0.75rem;
            border-radius: 9999px;
            font-size: 0.75rem;
            font-weight: 600;
            text-transform: uppercase;
        }}
        .test-status.passed {{ background: rgba(0, 186, 124, 0.2); color: #00ba7c; }}
        .test-status.failed {{ background: rgba(244, 33, 46, 0.2); color: #f4212e; }}
        .test-status.xfailed {{ background: rgba(255, 212, 0, 0.2); color: #ffd400; }}
        .test-status.skipped {{ background: rgba(113, 118, 123, 0.2); color: #71767b; }}
        .test-name {{ flex: 1; }}
        .test-duration {{ color: #71767b; font-size: 0.875rem; }}
        
        .footer {{
            margin-top: 2rem;
            text-align: center;
            color: #71767b;
            font-size: 0.875rem;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>OAS Generation Tool - Test Report</h1>
        <p class="timestamp">Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        
        <div class="summary">
            <div class="summary-card passed">
                <div class="number">{passed}</div>
                <div class="label">Passed</div>
            </div>
            <div class="summary-card failed">
                <div class="number">{failed}</div>
                <div class="label">Failed</div>
            </div>
            <div class="summary-card xfailed">
                <div class="number">{xfailed}</div>
                <div class="label">XFailed</div>
            </div>
            <div class="summary-card">
                <div class="number">{total}</div>
                <div class="label">Total</div>
            </div>
            <div class="summary-card">
                <div class="number">{duration:.1f}s</div>
                <div class="label">Duration</div>
            </div>
        </div>
"""
    
    # Add test files
    for file_path, file_tests in tests_by_file.items():
        file_passed = sum(1 for t in file_tests if t.get('outcome') == 'passed')
        file_total = len(file_tests)
        
        html += f"""
        <div class="test-file">
            <div class="test-file-header">
                <span>{file_path}</span>
                <span>{file_passed}/{file_total} passed</span>
            </div>
            <div class="test-list">
"""
        
        for test in file_tests:
            nodeid = test.get('nodeid', '')
            test_name = nodeid.split('::')[-1] if '::' in nodeid else nodeid
            outcome = test.get('outcome', 'unknown')
            test_duration = test.get('call', {}).get('duration', 0)
            
            html += f"""
                <div class="test-item">
                    <span class="test-status {outcome}">{outcome}</span>
                    <span class="test-name">{test_name}</span>
                    <span class="test-duration">{test_duration:.2f}s</span>
                </div>
"""
        
        html += """
            </div>
        </div>
"""
    
    html += """
        <div class="footer">
            <p>OAS Generation Tool - Non-Regression Test Suite</p>
        </div>
    </div>
</body>
</html>
"""
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"Report generated: {output_file}")
    return True


def generate_text_report(json_file: str, output_file: str = "test_report.txt"):
    """
    Generate a text report from pytest JSON output.
    """
    if not os.path.exists(json_file):
        print(f"Error: {json_file} not found")
        return False
    
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    summary = data.get('summary', {})
    tests = data.get('tests', [])
    
    lines = [
        "=" * 70,
        "OAS GENERATION TOOL - TEST REPORT",
        "=" * 70,
        f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "",
        "SUMMARY",
        "-" * 40,
        f"  Passed:  {summary.get('passed', 0)}",
        f"  Failed:  {summary.get('failed', 0)}",
        f"  XFailed: {summary.get('xfailed', 0)}",
        f"  Skipped: {summary.get('skipped', 0)}",
        f"  Total:   {summary.get('total', 0)}",
        f"  Duration: {summary.get('duration', 0):.2f}s",
        "",
        "DETAILED RESULTS",
        "-" * 40,
    ]
    
    # Group by outcome
    for outcome in ['passed', 'failed', 'xfailed', 'skipped']:
        outcome_tests = [t for t in tests if t.get('outcome') == outcome]
        if outcome_tests:
            lines.append(f"\n[{outcome.upper()}]")
            for test in outcome_tests:
                nodeid = test.get('nodeid', '')
                lines.append(f"  - {nodeid}")
    
    lines.append("")
    lines.append("=" * 70)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    
    print(f"Report generated: {output_file}")
    return True


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Generate test reports")
    parser.add_argument("--format", choices=["html", "text", "both"], default="both")
    parser.add_argument("--json-file", default="test_results.json")
    parser.add_argument("--output-dir", default="reports")
    args = parser.parse_args()
    
    os.makedirs(args.output_dir, exist_ok=True)
    
    # First, try to install pytest-json-report if not present
    try:
        import pytest_jsonreport
    except ImportError:
        print("Installing pytest-json-report...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pytest-json-report", "-q"])
    
    # Run tests
    print("Running tests...")
    run_tests_with_json_output(os.path.join(args.output_dir, args.json_file))
    
    # Generate reports
    json_path = os.path.join(args.output_dir, args.json_file)
    
    if args.format in ["html", "both"]:
        generate_html_report(json_path, os.path.join(args.output_dir, "test_report.html"))
    
    if args.format in ["text", "both"]:
        generate_text_report(json_path, os.path.join(args.output_dir, "test_report.txt"))
