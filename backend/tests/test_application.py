import pytest

from backend.app.services.exceptions import NotFoundError, ValidationError
from backend.app.application.farmer_application import FarmerApplication
from backend.app.application.cattle_application import CattleApplication
from backend.app.application.milk_record_application import MilkRecordApplication
from backend.app.application.feed_record_application import FeedRecordApplication


def test_farmer_application_get_all():
    farmers = FarmerApplication.get_all()

    assert isinstance(farmers, list)
    assert len(farmers) >= 1


def test_farmer_application_get_by_id():
    farmer = FarmerApplication.get_by_id(5)

    assert farmer["farmer_id"] == 5
    assert farmer["full_name"] == "Rajesh Patel"


def test_farmer_application_invalid_id():
    with pytest.raises(ValidationError):
        FarmerApplication.get_by_id(0)


def test_farmer_application_missing_farmer():
    with pytest.raises(NotFoundError):
        FarmerApplication.get_by_id(999999)

def test_cattle_application_get_all():
    cattle = CattleApplication.get_all()

    assert isinstance(cattle, list)
    assert len(cattle) >= 1


def test_cattle_application_get_by_id():
    cattle = CattleApplication.get_by_id(8)

    assert cattle["cattle_id"] == 8
    assert cattle["tag_number"] == "GJ-RP-001"


def test_cattle_application_invalid_id():
    with pytest.raises(ValidationError):
        CattleApplication.get_by_id(0)


def test_cattle_application_missing_cattle():
    with pytest.raises(NotFoundError):
        CattleApplication.get_by_id(999999)

def test_milk_record_application_get_all():
    records = MilkRecordApplication.get_all()

    assert isinstance(records, list)
    assert len(records) >= 1


def test_milk_record_application_get_by_id():
    record = MilkRecordApplication.get_by_id(13)

    assert record["milk_record_id"] == 13
    assert record["cattle_id"] == 8


def test_milk_record_application_invalid_id():
    with pytest.raises(ValidationError):
        MilkRecordApplication.get_by_id(0)


def test_milk_record_application_missing_record():
    with pytest.raises(NotFoundError):
        MilkRecordApplication.get_by_id(999999)

def test_feed_record_application_get_all():
    records = FeedRecordApplication.get_all()

    assert isinstance(records, list)
    assert len(records) >= 1


def test_feed_record_application_get_by_id():
    record = FeedRecordApplication.get_by_id(7)

    assert record["feed_record_id"] == 7
    assert record["farmer_id"] == 5


def test_feed_record_application_invalid_id():
    with pytest.raises(ValidationError):
        FeedRecordApplication.get_by_id(0)


def test_feed_record_application_missing_record():
    with pytest.raises(NotFoundError):
        FeedRecordApplication.get_by_id(999999)

def test_expense_application_get_all():
    from backend.app.application.expense_application import ExpenseApplication

    expenses = ExpenseApplication.get_all()

    assert isinstance(expenses, list)


def test_expense_application_get_by_id():
    from backend.app.application.expense_application import ExpenseApplication

    expenses = ExpenseApplication.get_all()

    if expenses:
        expense = ExpenseApplication.get_by_id(expenses[0]["expense_id"])

        assert expense["expense_id"] == expenses[0]["expense_id"]


def test_expense_application_invalid_id():
    import pytest

    from backend.app.application.expense_application import ExpenseApplication
    from backend.app.services.exceptions import ValidationError

    with pytest.raises(ValidationError):
        ExpenseApplication.get_by_id(0)


def test_expense_application_missing_expense():
    import pytest

    from backend.app.application.expense_application import ExpenseApplication
    from backend.app.services.exceptions import NotFoundError

    with pytest.raises(NotFoundError):
        ExpenseApplication.get_by_id(999999)

def test_revenue_application_get_all():
    from backend.app.application.revenue_application import RevenueApplication

    revenues = RevenueApplication.get_all()

    assert isinstance(revenues, list)


def test_revenue_application_get_by_id():
    from backend.app.application.revenue_application import RevenueApplication

    revenues = RevenueApplication.get_all()

    if revenues:
        revenue = RevenueApplication.get_by_id(revenues[0]["revenue_id"])
        assert revenue["revenue_id"] == revenues[0]["revenue_id"]


def test_revenue_application_invalid_id():
    from backend.app.application.revenue_application import RevenueApplication
    from backend.app.services.exceptions import ValidationError

    try:
        RevenueApplication.get_by_id(0)
        assert False
    except ValidationError:
        assert True


def test_revenue_application_missing_revenue():
    from backend.app.application.revenue_application import RevenueApplication
    from backend.app.services.exceptions import NotFoundError

    try:
        RevenueApplication.get_by_id(999999)
        assert False
    except NotFoundError:
        assert True