import numpy as np
from typing import Any
from abc import ABC, abstractmethod

from backend.app.repositories.milk_record_repository import MilkRecordRepository
from backend.app.repositories.expense_repository import ExpenseRepository
from backend.app.repositories.revenue_repository import RevenueRepository
from backend.app.repositories.feed_record_repository import FeedRecordRepository


class BaseAnalytics(ABC):
    """
    Abstract Base Class for Analytics.
    Demonstrates Abstraction and Inheritance.
    """

    @abstractmethod
    def fetch_data(self) -> list[dict[str, Any]]:
        """Fetch raw data from the appropriate repository."""
        pass

    @abstractmethod
    def calculate_metrics(self) -> dict[str, Any]:
        """Process data using NumPy and return structured metrics."""
        pass

    def calculate_time_series(self) -> dict[str, float]:
        """Process data to return time-series metrics if applicable."""
        return {}
        
    def calculate_categorical(self) -> dict[str, float]:
        """Process data to return categorical metrics if applicable."""
        return {}

    def run(self) -> dict[str, Any]:
        """Template method for running the analytics pipeline."""
        return self.calculate_metrics()


class MilkProductionAnalytics(BaseAnalytics):
    """Analytics for Milk Production using NumPy."""

    def fetch_data(self) -> list[dict[str, Any]]:
        return MilkRecordRepository.get_all()

    def calculate_metrics(self) -> dict[str, Any]:
        records = self.fetch_data()
        
        if not records:
            return {
                "total_production": 0.0,
                "average_production": 0.0,
                "min_production": 0.0,
                "max_production": 0.0,
                "std_deviation": 0.0,
                "record_count": 0
            }

        # Extract quantities as a NumPy array for fast numerical operations
        quantities = np.array([float(r["quantity_litres"]) for r in records if r["quantity_litres"] is not None])

        if quantities.size == 0:
            return {
                "total_production": 0.0,
                "average_production": 0.0,
                "min_production": 0.0,
                "max_production": 0.0,
                "std_deviation": 0.0,
                "record_count": 0
            }

        return {
            "total_production": round(float(np.sum(quantities)), 2),
            "average_production": round(float(np.mean(quantities)), 2),
            "min_production": round(float(np.min(quantities)), 2),
            "max_production": round(float(np.max(quantities)), 2),
            "std_deviation": round(float(np.std(quantities)), 2),
            "record_count": int(quantities.size)
        }

    def calculate_time_series(self) -> dict[str, float]:
        records = self.fetch_data()
        daily_totals = {}
        for r in records:
            if r["record_date"] and r["quantity_litres"] is not None:
                date_str = str(r["record_date"])
                if date_str not in daily_totals:
                    daily_totals[date_str] = []
                daily_totals[date_str].append(float(r["quantity_litres"]))
                
        # Use NumPy to aggregate the daily totals
        return {
            date: round(float(np.sum(np.array(quants))), 2)
            for date, quants in sorted(daily_totals.items())
        }


class ExpenseAnalytics(BaseAnalytics):
    """Analytics for Expenses using NumPy."""

    def fetch_data(self) -> list[dict[str, Any]]:
        return ExpenseRepository.get_all()

    def calculate_metrics(self) -> dict[str, Any]:
        records = self.fetch_data()
        
        if not records:
            return {
                "total_expense": 0.0,
                "average_expense": 0.0,
                "min_expense": 0.0,
                "max_expense": 0.0,
                "record_count": 0
            }

        amounts = np.array([float(r["amount"]) for r in records if r["amount"] is not None])

        if amounts.size == 0:
            return {
                "total_expense": 0.0,
                "average_expense": 0.0,
                "min_expense": 0.0,
                "max_expense": 0.0,
                "record_count": 0
            }

        return {
            "total_expense": round(float(np.sum(amounts)), 2),
            "average_expense": round(float(np.mean(amounts)), 2),
            "min_expense": round(float(np.min(amounts)), 2),
            "max_expense": round(float(np.max(amounts)), 2),
            "record_count": int(amounts.size)
        }

    def calculate_categorical(self) -> dict[str, float]:
        records = self.fetch_data()
        category_totals = {}
        for r in records:
            if r["category"] and r["amount"] is not None:
                cat = str(r["category"])
                if cat not in category_totals:
                    category_totals[cat] = []
                category_totals[cat].append(float(r["amount"]))
                
        # Use NumPy to aggregate the categorical totals
        return {
            cat: round(float(np.sum(np.array(amts))), 2)
            for cat, amts in category_totals.items()
        }


class RevenueAnalytics(BaseAnalytics):
    """Analytics for Revenue using NumPy."""

    def fetch_data(self) -> list[dict[str, Any]]:
        return RevenueRepository.get_all()

    def calculate_metrics(self) -> dict[str, Any]:
        records = self.fetch_data()
        
        if not records:
            return {
                "total_revenue": 0.0,
                "average_revenue": 0.0,
                "record_count": 0
            }

        # Calculate revenue = quantity * price
        revenues = np.array([
            float(r["quantity_litres"]) * float(r["price_per_litre"])
            for r in records
            if r["quantity_litres"] is not None and r["price_per_litre"] is not None
        ])

        if revenues.size == 0:
            return {
                "total_revenue": 0.0,
                "average_revenue": 0.0,
                "record_count": 0
            }

        return {
            "total_revenue": round(float(np.sum(revenues)), 2),
            "average_revenue": round(float(np.mean(revenues)), 2),
            "record_count": int(revenues.size)
        }


class AnalyticsOrchestrator:
    """
    Coordinates various analytics strategies to provide a comprehensive summary.
    Demonstrates Composition and Strategy-like usage.
    """
    
    def __init__(self):
        self.milk_analytics = MilkProductionAnalytics()
        self.expense_analytics = ExpenseAnalytics()
        self.revenue_analytics = RevenueAnalytics()

    def get_summary(self) -> dict[str, Any]:
        """Aggregate analytics across different domains."""
        milk_metrics = self.milk_analytics.run()
        expense_metrics = self.expense_analytics.run()
        revenue_metrics = self.revenue_analytics.run()

        net_profit = round(revenue_metrics["total_revenue"] - expense_metrics["total_expense"], 2)

        return {
            "milk_production": milk_metrics,
            "expenses": expense_metrics,
            "revenue": revenue_metrics,
            "financial_summary": {
                "net_profit": net_profit,
                "is_profitable": net_profit > 0
            }
        }

    def get_detailed_metrics(self) -> dict[str, Any]:
        """Aggregate detailed time-series and categorical data for dashboards."""
        return {
            "milk_production_time_series": self.milk_analytics.calculate_time_series(),
            "expense_categorical": self.expense_analytics.calculate_categorical(),
        }
