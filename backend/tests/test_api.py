import json
import threading
import time
import urllib.request
from http.server import HTTPServer
from unittest.mock import patch

from backend.app.main import DairyFarmAPIHandler

PORT = 18080

class TestAPI:
    @classmethod
    def setup_class(cls):
        # Start server in a thread
        cls.server = HTTPServer(('localhost', PORT), DairyFarmAPIHandler)
        cls.server_thread = threading.Thread(target=cls.server.serve_forever)
        cls.server_thread.daemon = True
        cls.server_thread.start()
        time.sleep(0.5)

    @classmethod
    def teardown_class(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.server_thread.join()

    @patch('backend.app.main.MilkRecordApplication.get_all')
    def test_get_milk_records(self, mock_get_all):
        mock_get_all.return_value = [{"id": 1, "session": "Morning", "quantity_litres": 10.5}]
        
        req = urllib.request.Request(f"http://localhost:{PORT}/api/milk-records")
        with urllib.request.urlopen(req) as response:
            assert response.status == 200
            data = json.loads(response.read().decode('utf-8'))
            assert "data" in data
            assert len(data["data"]) == 1
            assert data["data"][0]["session"] == "Morning"
            
    @patch('backend.app.main.MilkRecordApplication.create')
    def test_create_milk_record(self, mock_create):
        mock_create.return_value = {"id": 1, "session": "Evening"}
        
        payload = json.dumps({"cattle_id": 1, "record_date": "2026-08-18", "session": "Evening", "quantity_litres": 12.0}).encode('utf-8')
        req = urllib.request.Request(f"http://localhost:{PORT}/api/milk-records", data=payload, method='POST')
        req.add_header('Content-Type', 'application/json')
        
        with urllib.request.urlopen(req) as response:
            assert response.status == 201
            data = json.loads(response.read().decode('utf-8'))
            assert data["id"] == 1
            assert data["session"] == "Evening"

    def test_not_found(self):
        req = urllib.request.Request(f"http://localhost:{PORT}/api/non-existent-route")
        try:
            urllib.request.urlopen(req)
        except urllib.error.HTTPError as e:
            assert e.code == 404
