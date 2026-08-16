import pytest

from backend.app.services.cattle_service import CattleService
from backend.app.services.exceptions import NotFoundError, ValidationError
from backend.app.services.farmer_service import FarmerService
from backend.app.services.milk_record_service import MilkRecordService
from backend.app.services.feed_record_service import FeedRecordService
from backend.app.services.expense_service import ExpenseService
from backend.app.services.revenue_service import RevenueService


def test_farmer_service_get_all():
    farmers = FarmerService.get_all()

    assert isinstance(farmers, list)
    assert len(farmers) >= 1


def test_farmer_service_get_by_id():
    farmer = FarmerService.get_by_id(5)

    assert farmer["farmer_id"] == 5
    assert farmer["full_name"] == "Rajesh Patel"


def test_farmer_service_invalid_id():
    with pytest.raises(ValidationError):
        FarmerService.get_by_id(0)


def test_farmer_service_missing_farmer():
    with pytest.raises(NotFoundError):
        FarmerService.get_by_id(999999)


def test_cattle_service_get_all():
    cattle = CattleService.get_all()

    assert isinstance(cattle, list)
    assert len(cattle) >= 1


def test_cattle_service_get_by_id():
    cattle = CattleService.get_by_id(8)

    assert cattle["cattle_id"] == 8
    assert cattle["tag_number"] == "GJ-RP-001"


def test_cattle_service_invalid_id():
    with pytest.raises(ValidationError):
        CattleService.get_by_id(0)


def test_cattle_service_missing_cattle():
    with pytest.raises(NotFoundError):
        CattleService.get_by_id(999999)


def test_cattle_service_get_by_farmer_id():
    cattle = CattleService.get_by_farmer_id(5)

    assert isinstance(cattle, list)
    assert len(cattle) >= 1
    assert all(item["farmer_id"] == 5 for item in cattle)


def test_milk_record_service_get_all():
    records = MilkRecordService.get_all()

    assert isinstance(records, list)
    assert len(records) >= 1


def test_milk_record_service_get_by_id():
    record = MilkRecordService.get_by_id(13)

    assert record["milk_record_id"] == 13
    assert record["cattle_id"] == 8


def test_milk_record_service_invalid_id():
    with pytest.raises(ValidationError):
        MilkRecordService.get_by_id(0)


def test_milk_record_service_missing_record():
    with pytest.raises(NotFoundError):
        MilkRecordService.get_by_id(999999)


def test_milk_record_service_get_by_cattle_id():
    records = MilkRecordService.get_by_cattle_id(8)

    assert isinstance(records, list)
    assert len(records) >= 1
    assert all(record["cattle_id"] == 8 for record in records)

def test_feed_record_service_get_all():
    records = FeedRecordService.get_all()

    assert isinstance(records, list)
    assert len(records) >= 1


def test_feed_record_service_get_by_id():
    record = FeedRecordService.get_by_id(7)

    assert record["feed_record_id"] == 7
    assert record["farmer_id"] == 5


def test_feed_record_service_invalid_id():
    with pytest.raises(ValidationError):
        FeedRecordService.get_by_id(0)


def test_feed_record_service_missing_record():
    with pytest.raises(NotFoundError):
        FeedRecordService.get_by_id(999999)


def test_feed_record_service_get_by_farmer_id():
    records = FeedRecordService.get_by_farmer_id(5)

    assert isinstance(records, list)
    assert len(records) >= 1
    assert all(record["farmer_id"] == 5 for record in records)

def test_expense_service_get_all():
    expenses = ExpenseService.get_all()

    assert isinstance(expenses, list)
    assert len(expenses) >= 1


def test_expense_service_get_by_id():
    expense = ExpenseService.get_by_id(7)

    assert expense["expense_id"] == 7
    assert expense["farmer_id"] == 5
    assert expense["category"] == "Feed"


def test_expense_service_invalid_id():
    with pytest.raises(ValidationError):
        ExpenseService.get_by_id(0)


def test_expense_service_missing_record():
    with pytest.raises(NotFoundError):
        ExpenseService.get_by_id(999999)


def test_expense_service_get_by_farmer_id():
    expenses = ExpenseService.get_by_farmer_id(5)

    assert isinstance(expenses, list)

def test_revenue_service_get_all():
    revenues = RevenueService.get_all()

    assert isinstance(revenues, list)
    assert len(revenues) >= 1


def test_revenue_service_get_by_id():
    revenues = RevenueService.get_all()

    assert len(revenues) >= 1

    revenue_id = revenues[0]["revenue_id"]
    revenue = RevenueService.get_by_id(revenue_id)

    assert revenue["revenue_id"] == revenue_id


def test_revenue_service_invalid_id():
    with pytest.raises(ValidationError):
        RevenueService.get_by_id(0)


def test_revenue_service_missing_record():
    with pytest.raises(NotFoundError):
        RevenueService.get_by_id(999999)


def test_revenue_service_get_by_farmer_id():
    revenues = RevenueService.get_by_farmer_id(5)

    assert isinstance(revenues, list)