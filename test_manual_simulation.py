import requests
import time
import json
import traceback

BASE_URL = "http://localhost:8000"

def post(endpoint, data):
    return requests.post(f"{BASE_URL}{endpoint}", json=data, headers={"Connection": "close"})

def get(endpoint):
    return requests.get(f"{BASE_URL}{endpoint}", headers={"Connection": "close"})

report = {
    "Farmer": {"Valid": "[ ]", "Invalid": "[ ]", "DB Verified": "[ ]", "Duplicate": "[ ]", "Status": "[ ]"},
    "Cattle": {"Valid": "[ ]", "Invalid": "[ ]", "DB Verified": "[ ]", "Duplicate": "[ ]", "Status": "[ ]"},
    "Milk": {"Valid": "[ ]", "Invalid": "[ ]", "DB Verified": "[ ]", "Duplicate": "[ ]", "Status": "[ ]"},
    "Feed": {"Valid": "[ ]", "Invalid": "[ ]", "DB Verified": "[ ]", "Duplicate": "[ ]", "Status": "[ ]"},
    "Expense": {"Valid": "[ ]", "Invalid": "[ ]", "DB Verified": "[ ]", "Duplicate": "[ ]", "Status": "[ ]"},
    "Revenue": {"Valid": "[ ]", "Invalid": "[ ]", "DB Verified": "[ ]", "Duplicate": "[ ]", "Status": "[ ]"},
}

def check(condition, message):
    if not condition:
        print(f"  [FAIL] {message}")
        return False
    print(f"  [PASS] {message}")
    return True

ts = int(time.time())

def check_backend():
    try:
        print("Checking backend availability...")
        res = get("/api/farmers")
        if res.status_code == 200:
            print("Backend is running.")
            return True
    except Exception as e:
        pass
    return False

if not check_backend():
    print(f"CRITICAL: Backend at {BASE_URL} is unreachable.")
    print("Please start the backend server before running this simulation.")
    import sys
    sys.exit(1)

print("Testing Farmer...")
try:
    farmer_data = {
        "full_name": f"Test Farmer {ts}",
        "phone": str(ts)[-10:],
        "email": f"farmer{ts}@example.com",
        "address": "123 Test Farm"
    }
    r = post("/api/farmers", farmer_data)
    valid_pass = check(r.status_code == 201, f"Valid farmer creation (Status {r.status_code})")
    
    r2 = get("/api/farmers")
    farmers_list = r2.json().get("data", []) if isinstance(r2.json(), dict) else r2.json()
    db_pass = check(any(f.get("email") == farmer_data["email"] for f in farmers_list), "Farmer in DB")
    
    r_dup = post("/api/farmers", farmer_data)
    dup_pass = check(r_dup.status_code in [400, 409], f"Duplicate farmer rejected gracefully (Status {r_dup.status_code})")
    
    inv_data = farmer_data.copy()
    inv_data["full_name"] = ""
    r_inv = post("/api/farmers", inv_data)
    inv_pass = check(r_inv.status_code in [400, 422], f"Invalid farmer rejected gracefully (Status {r_inv.status_code})")
    
    report["Farmer"]["Valid"] = "PASS" if valid_pass else "FAIL"
    report["Farmer"]["DB Verified"] = "PASS" if db_pass else "FAIL"
    report["Farmer"]["Duplicate"] = "PASS" if dup_pass else "FAIL"
    report["Farmer"]["Invalid"] = "PASS" if inv_pass else "FAIL"
    report["Farmer"]["Status"] = "PASS" if all([valid_pass, db_pass, dup_pass, inv_pass]) else "FAIL"
except Exception as e:
    print(f"Error: {e}")
    
farmer_id = 1
for f in farmers_list:
    if f.get("email") == farmer_data["email"]:
        farmer_id = f["farmer_id"]
        break

print("\nTesting Cattle...")
try:
    cattle_data = {
        "farmer_id": farmer_id,
        "tag_number": f"TAG-{ts}",
        "gender": "female",
        "name": "Bessie",
        "breed": "Holstein",
        "date_of_birth": "2023-01-01",
        "status": "active"
    }
    r = post("/api/cattle", cattle_data)
    valid_pass = check(r.status_code == 201, f"Valid cattle creation (Status {r.status_code})")
    
    r2 = get("/api/cattle")
    c_list = r2.json().get("data", []) if isinstance(r2.json(), dict) else r2.json()
    db_pass = check(any(c.get("tag_number") == cattle_data["tag_number"] for c in c_list), "Cattle in DB")
    
    r_dup = post("/api/cattle", cattle_data)
    dup_pass = check(r_dup.status_code in [400, 409], f"Duplicate cattle rejected gracefully (Status {r_dup.status_code})")
    
    inv_data = cattle_data.copy()
    inv_data["date_of_birth"] = ""
    r_inv = post("/api/cattle", inv_data)
    inv_pass = check(r_inv.status_code in [400, 422], f"Empty date cattle rejected gracefully (Status {r_inv.status_code})")
    
    report["Cattle"]["Valid"] = "PASS" if valid_pass else "FAIL"
    report["Cattle"]["DB Verified"] = "PASS" if db_pass else "FAIL"
    report["Cattle"]["Duplicate"] = "PASS" if dup_pass else "FAIL"
    report["Cattle"]["Invalid"] = "FAIL" if not inv_pass else "PASS"
    report["Cattle"]["Status"] = "PASS" if all([valid_pass, db_pass, dup_pass, inv_pass]) else "FAIL"
except Exception as e:
    print(f"Error: {e}")
    
cattle_id = 1
for c in c_list:
    if c.get("tag_number") == cattle_data["tag_number"]:
        cattle_id = c["cattle_id"]
        break

print("\nTesting Milk...")
try:
    milk_data = {
        "cattle_id": cattle_id,
        "record_date": "2026-01-01",
        "session": "morning",
        "quantity_litres": 12.5
    }
    r = post("/api/milk-records", milk_data)
    valid_pass = check(r.status_code == 201, f"Valid milk creation (Status {r.status_code})")
    
    r2 = get("/api/milk-records")
    m_list = r2.json().get("data", []) if isinstance(r2.json(), dict) else r2.json()
    db_pass = check(any(m.get("cattle_id") == cattle_id and m.get("quantity_litres") == 12.5 for m in m_list), "Milk in DB")
    
    r_dup = post("/api/milk-records", milk_data)
    dup_pass = check(r_dup.status_code in [400, 409], f"Duplicate milk rejected gracefully (Status {r_dup.status_code})")
    
    inv_data = milk_data.copy()
    inv_data["cattle_id"] = 999999
    r_inv = post("/api/milk-records", inv_data)
    inv_pass = check(r_inv.status_code in [400, 404, 422], f"Invalid cattle_id rejected gracefully (Status {r_inv.status_code})")
    
    report["Milk"]["Valid"] = "PASS" if valid_pass else "FAIL"
    report["Milk"]["DB Verified"] = "PASS" if db_pass else "FAIL"
    report["Milk"]["Duplicate"] = "PASS" if dup_pass else "FAIL"
    report["Milk"]["Invalid"] = "PASS" if inv_pass else "FAIL"
    report["Milk"]["Status"] = "PASS" if all([valid_pass, db_pass, dup_pass, inv_pass]) else "FAIL"
except Exception as e:
    print(f"Error: {e}")

print("\nTesting Feed...")
try:
    feed_data = {
        "farmer_id": farmer_id,
        "cattle_id": cattle_id,
        "record_date": "2026-01-01",
        "feed_type": "Corn",
        "quantity_kg": 5.0,
        "cost": 100.0
    }
    r = post("/api/feed-records", feed_data)
    valid_pass = check(r.status_code == 201, f"Valid feed creation (Status {r.status_code})")
    
    r2 = get("/api/feed-records")
    f_list = r2.json().get("data", []) if isinstance(r2.json(), dict) else r2.json()
    db_pass = check(any(f.get("cattle_id") == cattle_id and f.get("feed_type") == "Corn" for f in f_list), "Feed in DB")
    
    r_dup = post("/api/feed-records", feed_data)
    dup_pass = check(r_dup.status_code != 500, f"Duplicate feed handled gracefully (Status {r_dup.status_code})")
    
    inv_data = feed_data.copy()
    inv_data["quantity_kg"] = -5
    r_inv = post("/api/feed-records", inv_data)
    inv_pass = check(r_inv.status_code in [400, 422], f"Negative quantity rejected gracefully (Status {r_inv.status_code})")
    
    report["Feed"]["Valid"] = "PASS" if valid_pass else "FAIL"
    report["Feed"]["DB Verified"] = "PASS" if db_pass else "FAIL"
    report["Feed"]["Duplicate"] = "PASS" if dup_pass else "FAIL"
    report["Feed"]["Invalid"] = "PASS" if inv_pass else "FAIL"
    report["Feed"]["Status"] = "PASS" if all([valid_pass, db_pass, dup_pass, inv_pass]) else "FAIL"
except Exception as e:
    print(f"Error: {e}")

print("\nTesting Expense...")
try:
    expense_data = {
        "farmer_id": farmer_id,
        "expense_date": "2026-01-01",
        "category": "Maintenance",
        "amount": 200.0,
        "description": "Fixed fence"
    }
    r = post("/api/expenses", expense_data)
    valid_pass = check(r.status_code == 201, f"Valid expense creation (Status {r.status_code})")
    
    r2 = get("/api/expenses")
    e_list = r2.json().get("data", []) if isinstance(r2.json(), dict) else r2.json()
    db_pass = check(any(e.get("farmer_id") == farmer_id and e.get("category") == "Maintenance" for e in e_list), "Expense in DB")
    
    r_dup = post("/api/expenses", expense_data)
    dup_pass = check(r_dup.status_code != 500, f"Duplicate expense handled gracefully (Status {r_dup.status_code})")
    
    inv_data = expense_data.copy()
    inv_data["amount"] = -100
    r_inv = post("/api/expenses", inv_data)
    inv_pass = check(r_inv.status_code in [400, 422], f"Negative amount rejected gracefully (Status {r_inv.status_code})")
    
    report["Expense"]["Valid"] = "PASS" if valid_pass else "FAIL"
    report["Expense"]["DB Verified"] = "PASS" if db_pass else "FAIL"
    report["Expense"]["Duplicate"] = "PASS" if dup_pass else "FAIL"
    report["Expense"]["Invalid"] = "PASS" if inv_pass else "FAIL"
    report["Expense"]["Status"] = "PASS" if all([valid_pass, db_pass, dup_pass, inv_pass]) else "FAIL"
except Exception as e:
    print(f"Error: {e}")

print("\nTesting Revenue...")
try:
    rev_data = {
        "farmer_id": farmer_id,
        "sale_date": "2026-01-01",
        "quantity_litres": 50,
        "price_per_litre": 60,
        "buyer_name": "DairyCorp"
    }
    r = post("/api/revenue", rev_data)
    valid_pass = check(r.status_code == 201, f"Valid revenue creation (Status {r.status_code})")
    
    r2 = get("/api/revenue")
    r_list = r2.json().get("data", []) if isinstance(r2.json(), dict) else r2.json()
    db_pass = check(any(rev.get("farmer_id") == farmer_id and rev.get("buyer_name") == "DairyCorp" for rev in r_list), "Revenue in DB")
    
    r_dup = post("/api/revenue", rev_data)
    dup_pass = check(r_dup.status_code != 500, f"Duplicate revenue handled gracefully (Status {r_dup.status_code})")
    
    inv_data = rev_data.copy()
    inv_data["quantity_litres"] = -50
    r_inv = post("/api/revenue", inv_data)
    inv_pass = check(r_inv.status_code in [400, 422], f"Negative quantity rejected gracefully (Status {r_inv.status_code})")
    
    report["Revenue"]["Valid"] = "PASS" if valid_pass else "FAIL"
    report["Revenue"]["DB Verified"] = "PASS" if db_pass else "FAIL"
    report["Revenue"]["Duplicate"] = "PASS" if dup_pass else "FAIL"
    report["Revenue"]["Invalid"] = "PASS" if inv_pass else "FAIL"
    report["Revenue"]["Status"] = "PASS" if all([valid_pass, db_pass, dup_pass, inv_pass]) else "FAIL"
except Exception as e:
    print(f"Error: {e}")

print("\n--- FINAL REPORT ---")
print("Module\tValid\tInvalid\tDB Verified\tDuplicate\tStatus")
for mod, data in report.items():
    print(f"{mod}\t{data['Valid']}\t{data['Invalid']}\t{data['DB Verified']}\t\t{data['Duplicate']}\t\t{data['Status']}")
