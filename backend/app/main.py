import json
import logging
from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse
from datetime import date
import numpy as np

from backend.app.application.cattle_application import CattleApplication
from backend.app.application.expense_application import ExpenseApplication
from backend.app.application.farmer_application import FarmerApplication
from backend.app.application.feed_record_application import FeedRecordApplication
from backend.app.application.milk_record_application import MilkRecordApplication
from backend.app.application.revenue_application import RevenueApplication
from backend.app.services.exceptions import ValidationError, NotFoundError, ConflictError
from backend.app.analytics.analytics_service import AnalyticsOrchestrator

logger = logging.getLogger(__name__)

from decimal import Decimal

class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, date):
            return obj.isoformat()
        if isinstance(obj, Decimal):
            return float(obj)
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super().default(obj)

class DairyFarmAPIHandler(BaseHTTPRequestHandler):
    """
    HTTP handler acting as the API boundary.
    Parses requests, routes to Application layer, and formats JSON responses.
    """

    def send_json_response(self, status_code: int, data: dict):
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data, cls=DateTimeEncoder).encode('utf-8'))

    def send_error_response(self, status_code: int, message: str):
        self.send_json_response(status_code, {"error": message})

    def do_OPTIONS(self):
        """Handle CORS preflight requests."""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def get_json_body(self) -> dict:
        content_length = int(self.headers.get('Content-Length', 0))
        if content_length == 0:
            return {}
        post_data = self.rfile.read(content_length)
        return json.loads(post_data.decode('utf-8'))

    def route_request(self):
        """Basic routing mechanism."""
        parsed_path = urllib.parse.urlparse(self.path)
        path = parsed_path.path
        method = self.command

        try:
            # --- CATTLE ---
            if path == '/api/cattle' and method == 'GET':
                return self.send_json_response(200, {"data": CattleApplication.get_all()})
            if path == '/api/cattle' and method == 'POST':
                body = self.get_json_body()
                res = CattleApplication.create(**body)
                return self.send_json_response(201, res)
            
            # --- MILK RECORDS ---
            if path == '/api/milk-records' and method == 'GET':
                return self.send_json_response(200, {"data": MilkRecordApplication.get_all()})
            if path == '/api/milk-records' and method == 'POST':
                body = self.get_json_body()
                res = MilkRecordApplication.create(**body)
                return self.send_json_response(201, res)
                
            # --- FEED RECORDS ---
            if path == '/api/feed-records' and method == 'GET':
                return self.send_json_response(200, {"data": FeedRecordApplication.get_all()})
            if path == '/api/feed-records' and method == 'POST':
                body = self.get_json_body()
                res = FeedRecordApplication.create(**body)
                return self.send_json_response(201, res)

            # --- EXPENSES ---
            if path == '/api/expenses' and method == 'GET':
                return self.send_json_response(200, {"data": ExpenseApplication.get_all()})
            if path == '/api/expenses' and method == 'POST':
                body = self.get_json_body()
                res = ExpenseApplication.create(**body)
                return self.send_json_response(201, res)
                
            # --- REVENUE ---
            if path == '/api/revenue' and method == 'GET':
                return self.send_json_response(200, {"data": RevenueApplication.get_all()})
            if path == '/api/revenue' and method == 'POST':
                body = self.get_json_body()
                res = RevenueApplication.create(**body)
                return self.send_json_response(201, res)

            # --- FARMER ---
            if path == '/api/farmers' and method == 'GET':
                return self.send_json_response(200, {"data": FarmerApplication.get_all()})
            if path == '/api/farmers' and method == 'POST':
                body = self.get_json_body()
                res = FarmerApplication.create(**body)
                return self.send_json_response(201, res)

            # --- ANALYTICS ---
            if path == '/api/analytics' and method == 'GET':
                orchestrator = AnalyticsOrchestrator()
                summary = orchestrator.get_summary()
                detailed = orchestrator.get_detailed_metrics()
                return self.send_json_response(200, {
                    "summary": summary,
                    "detailed": detailed
                })

            # If no route matches
            return self.send_error_response(404, "Endpoint not found")

        except ValidationError as e:
            self.send_error_response(400, str(e))
        except NotFoundError as e:
            self.send_error_response(404, str(e))
        except ConflictError as e:
            self.send_error_response(409, str(e))
        except Exception as e:
            logger.exception("Error processing request")
            self.send_error_response(500, "Internal Server Error")

    def do_GET(self):
        self.route_request()

    def do_POST(self):
        self.route_request()

    def do_PUT(self):
        self.route_request()

    def do_DELETE(self):
        self.route_request()

def run(server_class=HTTPServer, handler_class=DairyFarmAPIHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Starting API server on port {port}...")
    httpd.serve_forever()

if __name__ == '__main__':
    run()
