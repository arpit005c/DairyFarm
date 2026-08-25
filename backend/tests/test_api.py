import json
import threading
import time
import urllib.request
import urllib.error
import pytest
from http.server import HTTPServer
from unittest.mock import patch

from backend.app.main import DairyFarmAPIHandler
from backend.app.services.exceptions import ValidationError, NotFoundError, ConflictError

PORT = 18080

class TestAPI:
    @classmethod
    def setup_class(cls):
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

    def make_request(self, path, method="GET", data=None):
        req = urllib.request.Request(f"http://localhost:{PORT}{path}", method=method)
        if data is not None:
            req.add_header('Content-Type', 'application/json')
            req.data = json.dumps(data).encode('utf-8')
        try:
            with urllib.request.urlopen(req) as response:
                return response.status, json.loads(response.read().decode('utf-8'))
        except urllib.error.HTTPError as e:
            return e.code, json.loads(e.read().decode('utf-8'))

    @pytest.mark.parametrize("route,app_mock", [
        ("/api/farmers", "backend.app.main.FarmerApplication"),
        ("/api/cattle", "backend.app.main.CattleApplication"),
        ("/api/milk-records", "backend.app.main.MilkRecordApplication"),
        ("/api/feed-records", "backend.app.main.FeedRecordApplication"),
        ("/api/expenses", "backend.app.main.ExpenseApplication"),
        ("/api/revenue", "backend.app.main.RevenueApplication"),
    ])
    def test_crud_matrix(self, route, app_mock):
        with patch(app_mock) as MockApp:
            # GET collection (200)
            MockApp.get_all.return_value = [{"id": 1}]
            status, data = self.make_request(route, method="GET")
            assert status == 200
            assert "data" in data
            assert data["data"][0]["id"] == 1

            # GET single (200)
            MockApp.get_by_id.return_value = {"id": 1}
            status, data = self.make_request(f"{route}/1", method="GET")
            assert status == 200
            assert data["data"]["id"] == 1

            # POST create (201)
            MockApp.create.return_value = {"id": 2, "created": True}
            status, data = self.make_request(route, method="POST", data={"key": "val"})
            assert status == 201
            assert data["id"] == 2

            # PUT update (200)
            MockApp.update.return_value = {"id": 1, "updated": True}
            status, data = self.make_request(f"{route}/1", method="PUT", data={"key": "newval"})
            assert status == 200
            assert data["updated"] is True

            # DELETE (200)
            MockApp.delete.return_value = None
            status, data = self.make_request(f"{route}/1", method="DELETE")
            assert status == 200
            assert data["success"] is True

    @patch("backend.app.main.FarmerApplication")
    def test_error_handling(self, MockApp):
        route = "/api/farmers"
        
        # 400 Validation Error
        MockApp.create.side_effect = ValidationError("Invalid data")
        status, data = self.make_request(route, method="POST", data={})
        assert status == 400
        assert "error" in data

        # 404 Not Found
        MockApp.get_by_id.side_effect = NotFoundError("Not found")
        status, data = self.make_request(f"{route}/99", method="GET")
        assert status == 404
        assert "error" in data

        # 409 Conflict
        MockApp.create.side_effect = ConflictError("Duplicate")
        status, data = self.make_request(route, method="POST", data={})
        assert status == 409
        assert "error" in data

        # 500 Unexpected
        MockApp.create.side_effect = Exception("Boom")
        status, data = self.make_request(route, method="POST", data={})
        assert status == 500
        assert "error" in data

    @patch("backend.app.main.AnalyticsOrchestrator")
    def test_analytics_contract(self, MockOrchestrator):
        instance = MockOrchestrator.return_value
        instance.get_summary.return_value = {"milk_production": 100}
        instance.get_detailed_metrics.return_value = {"time_series": []}
        
        status, data = self.make_request("/api/analytics", method="GET")
        assert status == 200
        assert "summary" in data
        assert "detailed" in data
        assert data["summary"]["milk_production"] == 100
