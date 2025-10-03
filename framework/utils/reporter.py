"""
Test Reporter

Generate test reports in various formats
"""

from typing import List, Dict, Any
from pathlib import Path
from datetime import datetime
import json
from loguru import logger


class TestReporter:
    """
    Base test reporter
    
    Collects and formats test results
    """
    
    def __init__(self):
        self.results: List[Dict[str, Any]] = []
        self.start_time = None
        self.end_time = None
    
    def start(self):
        """Start reporting"""
        self.start_time = datetime.now()
        logger.info("Test reporting started")
    
    def add_result(self, result: Dict[str, Any]):
        """Add test result"""
        self.results.append(result)
    
    def end(self):
        """End reporting"""
        self.end_time = datetime.now()
        logger.info("Test reporting ended")
    
    def get_summary(self) -> Dict[str, Any]:
        """Get test summary"""
        total = len(self.results)
        passed = sum(1 for r in self.results if r.get('status') == 'passed')
        failed = sum(1 for r in self.results if r.get('status') == 'failed')
        skipped = sum(1 for r in self.results if r.get('status') == 'skipped')
        
        duration = None
        if self.start_time and self.end_time:
            duration = (self.end_time - self.start_time).total_seconds()
        
        return {
            'total': total,
            'passed': passed,
            'failed': failed,
            'skipped': skipped,
            'pass_rate': passed / total * 100 if total > 0 else 0,
            'duration': duration,
            'start_time': self.start_time.isoformat() if self.start_time else None,
            'end_time': self.end_time.isoformat() if self.end_time else None
        }
    
    def save_json(self, filepath: str):
        """Save report as JSON"""
        report = {
            'summary': self.get_summary(),
            'results': self.results
        }
        
        path = Path(filepath)
        path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(path, 'w') as f:
            json.dump(report, f, indent=2, default=str)
        
        logger.info(f"JSON report saved: {filepath}")


class HTMLReporter(TestReporter):
    """
    HTML test reporter
    
    Generates HTML test reports
    """
    
    def save_html(self, filepath: str):
        """Save report as HTML"""
        summary = self.get_summary()
        
        html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Test Report</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 20px;
            background-color: #f5f5f5;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #333;
            border-bottom: 2px solid #007bff;
            padding-bottom: 10px;
        }}
        .summary {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin: 20px 0;
        }}
        .metric {{
            background: #f8f9fa;
            padding: 15px;
            border-radius: 5px;
            text-align: center;
        }}
        .metric-value {{
            font-size: 2em;
            font-weight: bold;
            margin: 10px 0;
        }}
        .metric-label {{
            color: #666;
            font-size: 0.9em;
        }}
        .passed {{ color: #28a745; }}
        .failed {{ color: #dc3545; }}
        .skipped {{ color: #ffc107; }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }}
        th, td {{
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }}
        th {{
            background-color: #007bff;
            color: white;
        }}
        tr:hover {{
            background-color: #f5f5f5;
        }}
        .status-badge {{
            padding: 5px 10px;
            border-radius: 3px;
            font-weight: bold;
            font-size: 0.85em;
        }}
        .status-passed {{
            background-color: #d4edda;
            color: #155724;
        }}
        .status-failed {{
            background-color: #f8d7da;
            color: #721c24;
        }}
        .status-skipped {{
            background-color: #fff3cd;
            color: #856404;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Test Execution Report</h1>
        
        <div class="summary">
            <div class="metric">
                <div class="metric-label">Total Tests</div>
                <div class="metric-value">{summary['total']}</div>
            </div>
            <div class="metric">
                <div class="metric-label">Passed</div>
                <div class="metric-value passed">{summary['passed']}</div>
            </div>
            <div class="metric">
                <div class="metric-label">Failed</div>
                <div class="metric-value failed">{summary['failed']}</div>
            </div>
            <div class="metric">
                <div class="metric-label">Skipped</div>
                <div class="metric-value skipped">{summary['skipped']}</div>
            </div>
            <div class="metric">
                <div class="metric-label">Pass Rate</div>
                <div class="metric-value">{summary['pass_rate']:.1f}%</div>
            </div>
            <div class="metric">
                <div class="metric-label">Duration</div>
                <div class="metric-value">{summary.get('duration', 0):.2f}s</div>
            </div>
        </div>
        
        <h2>Test Results</h2>
        <table>
            <thead>
                <tr>
                    <th>Test Name</th>
                    <th>Status</th>
                    <th>Duration (s)</th>
                    <th>Message</th>
                </tr>
            </thead>
            <tbody>
"""
        
        for result in self.results:
            status = result.get('status', 'unknown')
            status_class = f"status-{status}"
            
            html += f"""
                <tr>
                    <td>{result.get('name', 'Unknown')}</td>
                    <td><span class="status-badge {status_class}">{status.upper()}</span></td>
                    <td>{result.get('duration', 0):.2f}</td>
                    <td>{result.get('message', '')}</td>
                </tr>
"""
        
        html += """
            </tbody>
        </table>
        
        <p style="color: #666; font-size: 0.9em; margin-top: 30px; text-align: center;">
            Generated at {timestamp}
        </p>
    </div>
</body>
</html>
""".format(timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        
        path = Path(filepath)
        path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(path, 'w') as f:
            f.write(html)
        
        logger.info(f"HTML report saved: {filepath}")
