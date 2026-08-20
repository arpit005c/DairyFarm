from unittest.mock import patch
import numpy as np
import pytest

from backend.app.analytics.analytics_service import (
    MilkProductionAnalytics,
    ExpenseAnalytics,
    RevenueAnalytics,
    AnalyticsOrchestrator
)


class TestAnalyticsService:

    @patch('backend.app.analytics.analytics_service.MilkRecordRepository.get_all')
    def test_milk_production_analytics_with_data(self, mock_get_all):
        """Test milk production calculations with valid data."""
        mock_get_all.return_value = [
            {"quantity_litres": 10.5},
            {"quantity_litres": 9.0},
            {"quantity_litres": 12.0}
        ]
        
        analytics = MilkProductionAnalytics()
        metrics = analytics.run()
        
        assert metrics["total_production"] == 31.5
        assert metrics["average_production"] == 10.5
        assert metrics["min_production"] == 9.0
        assert metrics["max_production"] == 12.0
        assert metrics["record_count"] == 3
        # std dev of 10.5, 9.0, 12.0 is approx 1.22
        assert metrics["std_deviation"] == 1.22

    @patch('backend.app.analytics.analytics_service.MilkRecordRepository.get_all')
    def test_milk_production_time_series(self, mock_get_all):
        """Test milk production time series calculation."""
        from datetime import date
        mock_get_all.return_value = [
            {"quantity_litres": 10.5, "record_date": date(2026, 8, 1)},
            {"quantity_litres": 5.0, "record_date": date(2026, 8, 1)},
            {"quantity_litres": 12.0, "record_date": date(2026, 8, 2)}
        ]
        
        analytics = MilkProductionAnalytics()
        ts = analytics.calculate_time_series()
        
        assert ts["2026-08-01"] == 15.5
        assert ts["2026-08-02"] == 12.0

    @patch('backend.app.analytics.analytics_service.MilkRecordRepository.get_all')
    def test_milk_production_analytics_empty(self, mock_get_all):
        """Test milk production calculations with empty data."""
        mock_get_all.return_value = []
        
        analytics = MilkProductionAnalytics()
        metrics = analytics.run()
        
        assert metrics["total_production"] == 0.0
        assert metrics["average_production"] == 0.0
        assert metrics["record_count"] == 0

    @patch('backend.app.analytics.analytics_service.ExpenseRepository.get_all')
    def test_expense_analytics_with_data(self, mock_get_all):
        """Test expense calculations with valid data."""
        mock_get_all.return_value = [
            {"amount": 100.0},
            {"amount": 200.0}
        ]
        
        analytics = ExpenseAnalytics()
        metrics = analytics.run()
        
        assert metrics["total_expense"] == 300.0
        assert metrics["average_expense"] == 150.0
        assert metrics["max_expense"] == 200.0
        assert metrics["min_expense"] == 100.0
        assert metrics["record_count"] == 2

    @patch('backend.app.analytics.analytics_service.ExpenseRepository.get_all')
    def test_expense_categorical(self, mock_get_all):
        """Test expense categorical calculation."""
        mock_get_all.return_value = [
            {"amount": 100.0, "category": "Feed"},
            {"amount": 200.0, "category": "Medicine"},
            {"amount": 50.0, "category": "Feed"}
        ]
        
        analytics = ExpenseAnalytics()
        cats = analytics.calculate_categorical()
        
        assert cats["Feed"] == 150.0
        assert cats["Medicine"] == 200.0

    @patch('backend.app.analytics.analytics_service.RevenueRepository.get_all')
    def test_revenue_analytics_with_data(self, mock_get_all):
        """Test revenue calculations with valid data."""
        mock_get_all.return_value = [
            {"quantity_litres": 10.0, "price_per_litre": 50.0}, # 500
            {"quantity_litres": 5.0, "price_per_litre": 60.0}   # 300
        ]
        
        analytics = RevenueAnalytics()
        metrics = analytics.run()
        
        assert metrics["total_revenue"] == 800.0
        assert metrics["average_revenue"] == 400.0
        assert metrics["record_count"] == 2

    @patch('backend.app.analytics.analytics_service.RevenueAnalytics.run')
    @patch('backend.app.analytics.analytics_service.ExpenseAnalytics.run')
    @patch('backend.app.analytics.analytics_service.MilkProductionAnalytics.run')
    def test_analytics_orchestrator(self, mock_milk, mock_expense, mock_revenue):
        """Test orchestrator combines metrics correctly and calculates profit."""
        mock_milk.return_value = {"total_production": 100.0}
        mock_expense.return_value = {"total_expense": 400.0}
        mock_revenue.return_value = {"total_revenue": 1000.0}
        
        orchestrator = AnalyticsOrchestrator()
        summary = orchestrator.get_summary()
        
        assert summary["milk_production"]["total_production"] == 100.0
        assert summary["financial_summary"]["net_profit"] == 600.0
        assert summary["financial_summary"]["is_profitable"] is True

    @patch('backend.app.analytics.analytics_service.ExpenseAnalytics.calculate_categorical')
    @patch('backend.app.analytics.analytics_service.MilkProductionAnalytics.calculate_time_series')
    def test_analytics_orchestrator_detailed(self, mock_milk_ts, mock_expense_cat):
        """Test orchestrator provides detailed metrics."""
        mock_milk_ts.return_value = {"2026-08-01": 15.5}
        mock_expense_cat.return_value = {"Feed": 150.0}
        
        orchestrator = AnalyticsOrchestrator()
        detailed = orchestrator.get_detailed_metrics()
        
        assert detailed["milk_production_time_series"]["2026-08-01"] == 15.5
        assert detailed["expense_categorical"]["Feed"] == 150.0
