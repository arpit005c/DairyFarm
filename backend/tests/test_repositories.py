from backend.app.repositories.cattle_repository import CattleRepository
from backend.app.repositories.expense_repository import ExpenseRepository
from backend.app.repositories.farmer_repository import FarmerRepository
from backend.app.repositories.feed_record_repository import FeedRecordRepository
from backend.app.repositories.milk_record_repository import MilkRecordRepository
from backend.app.repositories.revenue_repository import RevenueRepository


def test_farmer_repository():
    farmers = FarmerRepository.get_all()

    assert isinstance(farmers, list)
    assert len(farmers) > 0
    assert "farmer_id" in farmers[0]
    assert "full_name" in farmers[0]


def test_cattle_repository():
    cattle = CattleRepository.get_all()

    assert isinstance(cattle, list)
    assert len(cattle) > 0
    assert "cattle_id" in cattle[0]
    assert "farmer_id" in cattle[0]
    assert "tag_number" in cattle[0]


def test_milk_record_repository():
    records = MilkRecordRepository.get_all()

    assert isinstance(records, list)
    assert len(records) > 0
    assert "milk_record_id" in records[0]
    assert "cattle_id" in records[0]
    assert "quantity_litres" in records[0]


def test_feed_record_repository():
    records = FeedRecordRepository.get_all()

    assert isinstance(records, list)
    assert len(records) > 0
    assert "feed_record_id" in records[0]
    assert "farmer_id" in records[0]
    assert "quantity_kg" in records[0]


def test_expense_repository():
    expenses = ExpenseRepository.get_all()

    assert isinstance(expenses, list)
    assert len(expenses) > 0
    assert "expense_id" in expenses[0]
    assert "farmer_id" in expenses[0]
    assert "amount" in expenses[0]


def test_revenue_repository():
    revenues = RevenueRepository.get_all()

    assert isinstance(revenues, list)
    assert len(revenues) > 0
    assert "revenue_id" in revenues[0]
    assert "farmer_id" in revenues[0]
    assert "quantity_litres" in revenues[0]