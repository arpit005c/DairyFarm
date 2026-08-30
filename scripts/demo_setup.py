"""
DairyFarm Demo Data Setup Script
=================================
- Removes explicitly identified QA test records (by ID)
- Re-inserts missing demo feed record
- Generates 60 days (June 27 - Aug 25, 2026) of realistic milk production data
- Adds realistic weekly feed, monthly expenses, bi-weekly revenue
- All within a single transaction — rolls back on any error
- Prints final record counts after commit
"""

import os
import sys
import random
from datetime import date, timedelta
from decimal import Decimal

# Ensure project root is in path
project_root = os.path.abspath(os.path.dirname(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from dotenv import load_dotenv
load_dotenv()

import psycopg

# --- Connection ---
conn_params = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT", 5432)),
    "dbname": os.getenv("DB_NAME", "DairyFarmDB"),
    "user": os.getenv("DB_USER", "postgres"),
    "password": os.getenv("DB_PASSWORD", ""),
}

# --- Explicit QA farmer IDs confirmed by audit ---
QA_FARMER_IDS = (9, 10, 12, 14, 18, 20, 22, 24, 26, 28, 30, 32, 34, 36, 38, 40, 42, 44)
QA_CATTLE_IDS  = (22, 24, 26, 28, 30, 32, 34, 36, 38, 40, 42, 44, 46)

# --- Demo constants ---
SEED_FARMERS = {
    5: {"name": "Rajesh Patel",     "phone": "9876500001", "buyer": "Ahmedabad Dairy Cooperative"},
    6: {"name": "Mahesh Parmar",    "phone": "9876500002", "buyer": "Kheda Milk Collection Center"},
    7: {"name": "Suresh Chaudhary","phone": "9876500003", "buyer": "Mehsana Dairy Cooperative"},
}

# Female cattle and their realistic daily yield ranges (morning_pct, min_daily, max_daily)
DEMO_CATTLE = {
    8:  {"tag": "GJ-RP-001", "name": "Gauri",    "breed": "Gir",               "farmer_id": 5, "morning_pct": 0.55, "min_day": 14.0, "max_day": 18.5},
    9:  {"tag": "GJ-RP-002", "name": "Lakshmi",  "breed": "Sahiwal",           "farmer_id": 5, "morning_pct": 0.56, "min_day": 13.0, "max_day": 17.0},
    10: {"tag": "GJ-MP-001", "name": "Kamdhenu", "breed": "Gir",               "farmer_id": 6, "morning_pct": 0.54, "min_day": 15.5, "max_day": 19.5},
    12: {"tag": "GJ-SC-001", "name": "Radha",    "breed": "Holstein Friesian", "farmer_id": 7, "morning_pct": 0.53, "min_day": 18.0, "max_day": 22.5},
    13: {"tag": "GJ-SC-002", "name": "Ganga",    "breed": "Gir",               "farmer_id": 7, "morning_pct": 0.55, "min_day": 12.0, "max_day": 15.5},
}
# Moti (cattle_id=11) is male, no milk records added

START_DATE = date(2026, 6, 27)   # 60 days inclusive
END_DATE   = date(2026, 8, 25)

# Existing seed date — already has morning/evening for all cattle, keep as-is
EXISTING_SEED_DATE = date(2026, 8, 10)

random.seed(42)  # Reproducible

def clamp(val, lo, hi):
    return max(lo, min(hi, val))

def gen_milk_records():
    """Generate daily morning/evening milk records for 60 days, skipping existing Aug-10 records."""
    records = []
    d = START_DATE
    while d <= END_DATE:
        if d == EXISTING_SEED_DATE:
            d += timedelta(days=1)
            continue
        for cid, info in DEMO_CATTLE.items():
            # Gentle sinusoidal trend: slight peak mid-period
            day_n = (d - START_DATE).days
            trend = 1.0 + 0.08 * (day_n / 60.0) * (1 - day_n / 60.0) * 4  # peaks at midpoint
            daily = round(clamp(
                random.gauss(
                    (info["min_day"] + info["max_day"]) / 2 * trend,
                    (info["max_day"] - info["min_day"]) / 6
                ),
                info["min_day"] * 0.85,
                info["max_day"] * 1.05
            ), 2)
            morning = round(daily * info["morning_pct"], 2)
            evening = round(daily - morning, 2)
            records.append((cid, d, "morning", morning))
            records.append((cid, d, "evening", evening))
        d += timedelta(days=1)
    return records

def gen_feed_records():
    """Weekly feed records across 8+ weeks for all 6 cattle."""
    records = []
    feed_types = {
        8:  [("Green Fodder", 18, 15), ("Cattle Feed", 4, 45)],
        9:  [("Green Fodder", 16, 15), ("Cattle Feed", 4, 45)],
        10: [("Green Fodder", 20, 15), ("Silage", 6, 55)],
        11: [("Dry Fodder", 10, 18)],   # Moti (male)
        12: [("Cattle Feed", 9, 40),   ("Green Fodder", 20, 15)],
        13: [("Green Fodder", 16, 15), ("Mineral Mix", 2, 80)],
    }
    farmer_map = {8: 5, 9: 5, 10: 6, 11: 6, 12: 7, 13: 7}
    week_start = START_DATE
    while week_start <= END_DATE:
        for cid, feeds in feed_types.items():
            fid = farmer_map[cid]
            for feed_type, qty_kg, cost_per_kg in feeds:
                # Add slight weekly variation
                qty = round(qty_kg * random.uniform(0.9, 1.1), 1)
                cost = round(qty * cost_per_kg * random.uniform(0.95, 1.05), 2)
                records.append((fid, cid, week_start, feed_type, qty, cost))
        week_start += timedelta(days=7)
    return records

def gen_expenses():
    """Realistic monthly/bi-monthly expenses per farmer across the demo period."""
    records = []
    # (farmer_id, date_offset, category, description, amount_range)
    templates = [
        # Rajesh Patel (farmer 5)
        (5, 0,  "Feed",        "Monthly green fodder and cattle feed",     (1800, 2200)),
        (5, 14, "Veterinary",  "Routine vaccination and health check",      (600,  900)),
        (5, 28, "Feed",        "Concentrate feed replenishment",            (900, 1200)),
        (5, 0,  "Utilities",   "Electricity and water for farm",            (350,  500)),
        (5, 30, "Maintenance", "Milking equipment servicing",               (800, 1100)),
        (5, 45, "Feed",        "End-month fodder restock",                  (1500, 1900)),
        (5, 52, "Labor",       "Monthly farm labor wages",                  (5000, 6000)),
        # Mahesh Parmar (farmer 6)
        (6, 0,  "Feed",        "Green fodder and silage purchase",          (2000, 2500)),
        (6, 10, "Veterinary",  "Veterinary consultation and medicines",     (750,  950)),
        (6, 28, "Feed",        "Cattle feed concentrate",                   (950, 1250)),
        (6, 7,  "Maintenance", "Cattle shed repair and maintenance",        (1200, 1600)),
        (6, 42, "Utilities",   "Pump and motor electricity",                (400,  600)),
        (6, 49, "Labor",       "Hired labor for harvesting fodder",         (2500, 3000)),
        (6, 55, "Transport",   "Milk transport to collection center",       (500,  700)),
        # Suresh Chaudhary (farmer 7)
        (7, 0,  "Feed",        "Green fodder, cattle feed and mineral mix", (2200, 2700)),
        (7, 15, "Veterinary",  "Monthly veterinary visit",                  (800, 1100)),
        (7, 29, "Feed",        "Supplemental cattle feed",                  (1000, 1400)),
        (7, 5,  "Transport",   "Weekly milk transport to cooperative",      (600,  800)),
        (7, 35, "Maintenance", "Feed storage and barn maintenance",         (900, 1300)),
        (7, 50, "Labor",       "Farm worker monthly wages",                 (5500, 6500)),
        (7, 55, "Utilities",   "Water pump and electricity bills",          (450,  600)),
    ]
    for fid, offset, category, desc, (lo, hi) in templates:
        expense_date = START_DATE + timedelta(days=offset)
        if expense_date > END_DATE:
            expense_date = END_DATE
        amount = round(random.uniform(lo, hi), 2)
        records.append((fid, expense_date, category, desc, amount))
    return records

def gen_revenue():
    """Bi-weekly milk sales per farmer across the 60-day period."""
    records = []
    # Cooperative milk prices (realistic INR/litre)
    cooperatives = {
        5: ("Ahmedabad Dairy Cooperative", 58.00),
        6: ("Kheda Milk Collection Center", 57.50),
        7: ("Mehsana Dairy Cooperative", 60.00),
    }
    # Approx total daily production per farmer
    farmer_daily = {
        5: 32.5,   # Gauri + Lakshmi
        6: 18.0,   # Kamdhenu (Moti male, no milk)
        7: 31.5,   # Radha + Ganga
    }
    # Bi-weekly sales (every 14 days)
    sale_offsets = [0, 14, 28, 42, 56]
    for fid, (buyer, price) in cooperatives.items():
        for offset in sale_offsets:
            sale_date = START_DATE + timedelta(days=offset)
            if sale_date > END_DATE:
                continue
            # 13 days of production sold (bi-weekly accumulation), with some variation
            qty = round(farmer_daily[fid] * 13 * random.uniform(0.92, 1.05), 1)
            records.append((fid, sale_date, qty, price, buyer))
    return records


def main():
    print("=" * 60)
    print("DairyFarm Demo Setup — Starting")
    print("=" * 60)

    with psycopg.connect(**conn_params) as conn:
        with conn.cursor() as cur:

            # === STEP 1: Verify local database ===
            cur.execute("SELECT current_database(), inet_server_addr(), inet_server_port()")
            db_name, host, port = cur.fetchone()
            print(f"\n[DB] Connected to: {db_name} @ {host or 'localhost'}:{port}")
            if "prod" in db_name.lower() or "cloud" in db_name.lower():
                print("ERROR: Refusing to modify what looks like a production database.")
                sys.exit(1)

            print("\n[AUDIT] Pre-cleanup counts:")
            for tbl in ("farmers","cattle","milk_records","feed_records","expenses","revenue"):
                cur.execute(f"SELECT COUNT(*) FROM {tbl}")
                print(f"  {tbl:<15}: {cur.fetchone()[0]}")

            print("\n[CLEANUP] Beginning transaction...")

            # === STEP 2: Delete QA records in FK-safe order ===

            # Revenue owned by test farmers
            cur.execute("DELETE FROM revenue WHERE farmer_id = ANY(%s)", (list(QA_FARMER_IDS),))
            print(f"  Deleted revenue rows: {cur.rowcount}")

            # Expenses owned by test farmers
            cur.execute("DELETE FROM expenses WHERE farmer_id = ANY(%s)", (list(QA_FARMER_IDS),))
            print(f"  Deleted expense rows: {cur.rowcount}")

            # Feed records owned by test farmers
            cur.execute("DELETE FROM feed_records WHERE farmer_id = ANY(%s)", (list(QA_FARMER_IDS),))
            print(f"  Deleted feed_record rows: {cur.rowcount}")

            # Milk records for test cattle
            cur.execute("DELETE FROM milk_records WHERE cattle_id = ANY(%s)", (list(QA_CATTLE_IDS),))
            print(f"  Deleted milk_record rows: {cur.rowcount}")

            # Test cattle
            cur.execute("DELETE FROM cattle WHERE cattle_id = ANY(%s)", (list(QA_CATTLE_IDS),))
            print(f"  Deleted cattle rows: {cur.rowcount}")

            # Test farmers (explicit IDs only)
            cur.execute("DELETE FROM farmers WHERE farmer_id = ANY(%s)", (list(QA_FARMER_IDS),))
            print(f"  Deleted farmer rows: {cur.rowcount}")

            # === STEP 3: Re-insert missing demo feed record ===
            # feed_record for Moti (cattle_id=11, farmer_id=6) was deleted during QA
            cur.execute("SELECT COUNT(*) FROM feed_records WHERE farmer_id=6 AND cattle_id=11")
            if cur.fetchone()[0] == 0:
                cur.execute("""
                    INSERT INTO feed_records (farmer_id, cattle_id, record_date, feed_type, quantity_kg, cost)
                    VALUES (6, 11, '2026-08-10', 'Dry Fodder', 10.00, 180.00)
                """)
                print("  Re-inserted missing Moti (GJ-MP-002) feed record.")

            # === STEP 4: Generate 60-day milk records (skip existing Aug-10) ===
            milk_data = gen_milk_records()
            cur.executemany(
                "INSERT INTO milk_records (cattle_id, record_date, session, quantity_litres) VALUES (%s,%s,%s,%s)",
                milk_data
            )
            print(f"  Inserted {len(milk_data)} milk records (60-day history, excl. Aug-10 seed).")

            # === STEP 5: Generate 8-week feed records ===
            feed_data = gen_feed_records()
            cur.executemany(
                "INSERT INTO feed_records (farmer_id, cattle_id, record_date, feed_type, quantity_kg, cost) VALUES (%s,%s,%s,%s,%s,%s)",
                feed_data
            )
            print(f"  Inserted {len(feed_data)} feed records.")

            # === STEP 6: Generate realistic expenses ===
            expense_data = gen_expenses()
            cur.executemany(
                "INSERT INTO expenses (farmer_id, expense_date, category, description, amount) VALUES (%s,%s,%s,%s,%s)",
                expense_data
            )
            print(f"  Inserted {len(expense_data)} expense records.")

            # === STEP 7: Generate bi-weekly revenue ===
            revenue_data = gen_revenue()
            cur.executemany(
                "INSERT INTO revenue (farmer_id, sale_date, quantity_litres, price_per_litre, buyer_name) VALUES (%s,%s,%s,%s,%s)",
                revenue_data
            )
            print(f"  Inserted {len(revenue_data)} revenue records.")

            # === STEP 8: FK / constraint sanity checks ===
            print("\n[VERIFY] Checking constraints...")

            # Orphan cattle
            cur.execute("SELECT COUNT(*) FROM cattle c LEFT JOIN farmers f ON c.farmer_id=f.farmer_id WHERE f.farmer_id IS NULL")
            orphan_cattle = cur.fetchone()[0]
            assert orphan_cattle == 0, f"Orphan cattle found: {orphan_cattle}"

            # Orphan milk
            cur.execute("SELECT COUNT(*) FROM milk_records m LEFT JOIN cattle c ON m.cattle_id=c.cattle_id WHERE c.cattle_id IS NULL")
            orphan_milk = cur.fetchone()[0]
            assert orphan_milk == 0, f"Orphan milk records found: {orphan_milk}"

            # Orphan feed
            cur.execute("SELECT COUNT(*) FROM feed_records f LEFT JOIN farmers fa ON f.farmer_id=fa.farmer_id WHERE fa.farmer_id IS NULL")
            orphan_feed = cur.fetchone()[0]
            assert orphan_feed == 0, f"Orphan feed records found: {orphan_feed}"

            # Negative quantities
            cur.execute("SELECT COUNT(*) FROM milk_records WHERE quantity_litres < 0")
            assert cur.fetchone()[0] == 0, "Negative milk quantities found"
            cur.execute("SELECT COUNT(*) FROM feed_records WHERE quantity_kg < 0 OR cost < 0")
            assert cur.fetchone()[0] == 0, "Negative feed values found"
            cur.execute("SELECT COUNT(*) FROM expenses WHERE amount < 0")
            assert cur.fetchone()[0] == 0, "Negative expense amounts found"
            cur.execute("SELECT COUNT(*) FROM revenue WHERE quantity_litres < 0 OR price_per_litre < 0")
            assert cur.fetchone()[0] == 0, "Negative revenue values found"

            # Duplicate milk (cattle+date+session)
            cur.execute("""
                SELECT COUNT(*) FROM (
                    SELECT cattle_id, record_date, session, COUNT(*) 
                    FROM milk_records 
                    GROUP BY cattle_id, record_date, session 
                    HAVING COUNT(*) > 1
                ) x
            """)
            assert cur.fetchone()[0] == 0, "Duplicate milk session records found"

            # Duplicate farmer phone
            cur.execute("SELECT COUNT(*) FROM (SELECT phone, COUNT(*) FROM farmers GROUP BY phone HAVING COUNT(*)>1) x")
            assert cur.fetchone()[0] == 0, "Duplicate farmer phones found"

            print("  OK No orphan records")
            print("  OK No negative values")
            print("  OK No duplicate milk sessions")
            print("  OK No duplicate farmer phones")

            # === COMMIT ===
            conn.commit()
            print("\n[OK] Transaction committed.")

            # === STEP 9: Final counts ===
            print("\n[FINAL] Database record counts:")
            for tbl in ("farmers","cattle","milk_records","feed_records","expenses","revenue"):
                cur.execute(f"SELECT COUNT(*) FROM {tbl}")
                print(f"  {tbl:<15}: {cur.fetchone()[0]}")

            # === STEP 10: Analytics spot-check ===
            print("\n[ANALYTICS] Spot-checking milk_records for time-series richness:")
            cur.execute("SELECT MIN(record_date), MAX(record_date), COUNT(DISTINCT record_date) FROM milk_records")
            r = cur.fetchone()
            print(f"  Date range: {r[0]} -> {r[1]}  ({r[2]} distinct dates)")
            cur.execute("SELECT SUM(quantity_litres), AVG(quantity_litres), COUNT(*) FROM milk_records")
            r = cur.fetchone()
            print(f"  Total: {float(r[0]):.1f} L | Avg per session: {float(r[1]):.2f} L | Records: {r[2]}")

            cur.execute("SELECT SUM(amount) FROM expenses")
            print(f"  Total expenses: ₹{float(cur.fetchone()[0]):,.2f}")
            cur.execute("SELECT SUM(quantity_litres * price_per_litre) FROM revenue")
            print(f"  Total revenue:  ₹{float(cur.fetchone()[0]):,.2f}")

    print("\n" + "=" * 60)
    print("Demo setup COMPLETE — database is demo-ready.")
    print("=" * 60)


if __name__ == "__main__":
    main()
