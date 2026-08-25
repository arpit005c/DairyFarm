import json
import logging
import os
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

        import re
        try:
            # --- FARMER ---
            m_farmer = re.match(r'^/api/farmers(?:/(\d+))?/?$', path)
            if m_farmer:
                fid = m_farmer.group(1)
                if method == 'GET' and not fid:
                    return self.send_json_response(200, {"data": FarmerApplication.get_all()})
                elif method == 'GET' and fid:
                    return self.send_json_response(200, {"data": FarmerApplication.get_by_id(int(fid))})
                elif method == 'POST' and not fid:
                    body = self.get_json_body()
                    return self.send_json_response(201, FarmerApplication.create(**body))
                elif method == 'PUT' and fid:
                    body = self.get_json_body()
                    body.pop('farmer_id', None)
                    return self.send_json_response(200, FarmerApplication.update(farmer_id=int(fid), **body))
                elif method == 'DELETE' and fid:
                    FarmerApplication.delete(farmer_id=int(fid))
                    return self.send_json_response(200, {"success": True})

            # --- CATTLE ---
            m_cattle = re.match(r'^/api/cattle(?:/(\d+))?/?$', path)
            if m_cattle:
                cid = m_cattle.group(1)
                if method == 'GET' and not cid:
                    return self.send_json_response(200, {"data": CattleApplication.get_all()})
                elif method == 'GET' and cid:
                    return self.send_json_response(200, {"data": CattleApplication.get_by_id(int(cid))})
                elif method == 'POST' and not cid:
                    body = self.get_json_body()
                    return self.send_json_response(201, CattleApplication.create(**body))
                elif method == 'PUT' and cid:
                    body = self.get_json_body()
                    body.pop('cattle_id', None)
                    return self.send_json_response(200, CattleApplication.update(cattle_id=int(cid), **body))
                elif method == 'DELETE' and cid:
                    CattleApplication.delete(cattle_id=int(cid))
                    return self.send_json_response(200, {"success": True})
            
            # --- MILK RECORDS ---
            m_milk = re.match(r'^/api/milk-records(?:/(\d+))?/?$', path)
            if m_milk:
                mid = m_milk.group(1)
                if method == 'GET' and not mid:
                    return self.send_json_response(200, {"data": MilkRecordApplication.get_all()})
                elif method == 'GET' and mid:
                    return self.send_json_response(200, {"data": MilkRecordApplication.get_by_id(int(mid))})
                elif method == 'POST' and not mid:
                    body = self.get_json_body()
                    return self.send_json_response(201, MilkRecordApplication.create(**body))
                elif method == 'PUT' and mid:
                    body = self.get_json_body()
                    body.pop('milk_record_id', None)
                    return self.send_json_response(200, MilkRecordApplication.update(milk_record_id=int(mid), **body))
                elif method == 'DELETE' and mid:
                    MilkRecordApplication.delete(milk_record_id=int(mid))
                    return self.send_json_response(200, {"success": True})
                
            # --- FEED RECORDS ---
            m_feed = re.match(r'^/api/feed-records(?:/(\d+))?/?$', path)
            if m_feed:
                fid = m_feed.group(1)
                if method == 'GET' and not fid:
                    return self.send_json_response(200, {"data": FeedRecordApplication.get_all()})
                elif method == 'GET' and fid:
                    return self.send_json_response(200, {"data": FeedRecordApplication.get_by_id(int(fid))})
                elif method == 'POST' and not fid:
                    body = self.get_json_body()
                    return self.send_json_response(201, FeedRecordApplication.create(**body))
                elif method == 'PUT' and fid:
                    body = self.get_json_body()
                    body.pop('feed_record_id', None)
                    return self.send_json_response(200, FeedRecordApplication.update(feed_record_id=int(fid), **body))
                elif method == 'DELETE' and fid:
                    FeedRecordApplication.delete(feed_record_id=int(fid))
                    return self.send_json_response(200, {"success": True})

            # --- EXPENSES ---
            m_exp = re.match(r'^/api/expenses(?:/(\d+))?/?$', path)
            if m_exp:
                eid = m_exp.group(1)
                if method == 'GET' and not eid:
                    return self.send_json_response(200, {"data": ExpenseApplication.get_all()})
                elif method == 'GET' and eid:
                    return self.send_json_response(200, {"data": ExpenseApplication.get_by_id(int(eid))})
                elif method == 'POST' and not eid:
                    body = self.get_json_body()
                    return self.send_json_response(201, ExpenseApplication.create(**body))
                elif method == 'PUT' and eid:
                    body = self.get_json_body()
                    body.pop('expense_id', None)
                    return self.send_json_response(200, ExpenseApplication.update(expense_id=int(eid), **body))
                elif method == 'DELETE' and eid:
                    ExpenseApplication.delete(expense_id=int(eid))
                    return self.send_json_response(200, {"success": True})
                
            # --- REVENUE ---
            m_rev = re.match(r'^/api/revenue(?:/(\d+))?/?$', path)
            if m_rev:
                rid = m_rev.group(1)
                if method == 'GET' and not rid:
                    return self.send_json_response(200, {"data": RevenueApplication.get_all()})
                elif method == 'GET' and rid:
                    return self.send_json_response(200, {"data": RevenueApplication.get_by_id(int(rid))})
                elif method == 'POST' and not rid:
                    body = self.get_json_body()
                    return self.send_json_response(201, RevenueApplication.create(**body))
                elif method == 'PUT' and rid:
                    body = self.get_json_body()
                    body.pop('revenue_id', None)
                    return self.send_json_response(200, RevenueApplication.update(revenue_id=int(rid), **body))
                elif method == 'DELETE' and rid:
                    RevenueApplication.delete(revenue_id=int(rid))
                    return self.send_json_response(200, {"success": True})

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

def run(server_class=HTTPServer, handler_class=DairyFarmAPIHandler, port=None):
    if port is None:
        port = int(os.environ.get('PORT', 8000))
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Starting API server on port {port}...")
    httpd.serve_forever()

if __name__ == '__main__':
    run()
