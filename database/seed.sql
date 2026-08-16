-- ============================================================
-- DairyFarm Development Seed Data
-- PostgreSQL 18+
-- ============================================================

BEGIN;

-- ============================================================
-- 1. FARMERS
-- ============================================================

INSERT INTO farmers (full_name, phone, email, address)
VALUES
    ('Rajesh Patel', '9876500001', 'rajesh.patel@example.com', 'Ahmedabad, Gujarat'),
    ('Mahesh Parmar', '9876500002', 'mahesh.parmar@example.com', 'Kheda, Gujarat'),
    ('Suresh Chaudhary', '9876500003', 'suresh.chaudhary@example.com', 'Mehsana, Gujarat');

-- ============================================================
-- 2. CATTLE
-- ============================================================

INSERT INTO cattle
    (farmer_id, tag_number, name, breed, gender, date_of_birth, status)
VALUES
    (
        (SELECT farmer_id FROM farmers WHERE phone = '9876500001'),
        'GJ-RP-001',
        'Gauri',
        'Gir',
        'female',
        '2022-03-15',
        'active'
    ),
    (
        (SELECT farmer_id FROM farmers WHERE phone = '9876500001'),
        'GJ-RP-002',
        'Lakshmi',
        'Sahiwal',
        'female',
        '2021-08-20',
        'active'
    ),
    (
        (SELECT farmer_id FROM farmers WHERE phone = '9876500002'),
        'GJ-MP-001',
        'Kamdhenu',
        'Gir',
        'female',
        '2020-11-10',
        'active'
    ),
    (
        (SELECT farmer_id FROM farmers WHERE phone = '9876500002'),
        'GJ-MP-002',
        'Moti',
        'Jersey',
        'male',
        '2022-01-05',
        'active'
    ),
    (
        (SELECT farmer_id FROM farmers WHERE phone = '9876500003'),
        'GJ-SC-001',
        'Radha',
        'Holstein Friesian',
        'female',
        '2021-05-18',
        'active'
    ),
    (
        (SELECT farmer_id FROM farmers WHERE phone = '9876500003'),
        'GJ-SC-002',
        'Ganga',
        'Gir',
        'female',
        '2023-02-12',
        'active'
    );

-- ============================================================
-- 3. MILK RECORDS
-- ============================================================

INSERT INTO milk_records
    (cattle_id, record_date, session, quantity_litres)
VALUES
    ((SELECT cattle_id FROM cattle WHERE tag_number = 'GJ-RP-001'), '2026-08-10', 'morning', 8.50),
    ((SELECT cattle_id FROM cattle WHERE tag_number = 'GJ-RP-001'), '2026-08-10', 'evening', 7.20),
    ((SELECT cattle_id FROM cattle WHERE tag_number = 'GJ-RP-002'), '2026-08-10', 'morning', 7.80),
    ((SELECT cattle_id FROM cattle WHERE tag_number = 'GJ-RP-002'), '2026-08-10', 'evening', 6.90),

    ((SELECT cattle_id FROM cattle WHERE tag_number = 'GJ-MP-001'), '2026-08-10', 'morning', 9.10),
    ((SELECT cattle_id FROM cattle WHERE tag_number = 'GJ-MP-001'), '2026-08-10', 'evening', 8.00),
    ((SELECT cattle_id FROM cattle WHERE tag_number = 'GJ-MP-002'), '2026-08-10', 'morning', 0.00),
    ((SELECT cattle_id FROM cattle WHERE tag_number = 'GJ-MP-002'), '2026-08-10', 'evening', 0.00),

    ((SELECT cattle_id FROM cattle WHERE tag_number = 'GJ-SC-001'), '2026-08-10', 'morning', 10.20),
    ((SELECT cattle_id FROM cattle WHERE tag_number = 'GJ-SC-001'), '2026-08-10', 'evening', 9.30),
    ((SELECT cattle_id FROM cattle WHERE tag_number = 'GJ-SC-002'), '2026-08-10', 'morning', 6.70),
    ((SELECT cattle_id FROM cattle WHERE tag_number = 'GJ-SC-002'), '2026-08-10', 'evening', 5.80);

-- ============================================================
-- 4. FEED RECORDS
-- ============================================================

INSERT INTO feed_records
    (farmer_id, cattle_id, record_date, feed_type, quantity_kg, cost)
VALUES
    (
        (SELECT farmer_id FROM farmers WHERE phone = '9876500001'),
        (SELECT cattle_id FROM cattle WHERE tag_number = 'GJ-RP-001'),
        '2026-08-10',
        'Green Fodder',
        18.00,
        270.00
    ),
    (
        (SELECT farmer_id FROM farmers WHERE phone = '9876500001'),
        (SELECT cattle_id FROM cattle WHERE tag_number = 'GJ-RP-002'),
        '2026-08-10',
        'Cattle Feed',
        8.00,
        320.00
    ),
    (
        (SELECT farmer_id FROM farmers WHERE phone = '9876500002'),
        (SELECT cattle_id FROM cattle WHERE tag_number = 'GJ-MP-001'),
        '2026-08-10',
        'Green Fodder',
        20.00,
        300.00
    ),
    (
        (SELECT farmer_id FROM farmers WHERE phone = '9876500002'),
        (SELECT cattle_id FROM cattle WHERE tag_number = 'GJ-MP-002'),
        '2026-08-10',
        'Dry Fodder',
        10.00,
        180.00
    ),
    (
        (SELECT farmer_id FROM farmers WHERE phone = '9876500003'),
        (SELECT cattle_id FROM cattle WHERE tag_number = 'GJ-SC-001'),
        '2026-08-10',
        'Cattle Feed',
        9.00,
        360.00
    ),
    (
        (SELECT farmer_id FROM farmers WHERE phone = '9876500003'),
        (SELECT cattle_id FROM cattle WHERE tag_number = 'GJ-SC-002'),
        '2026-08-10',
        'Green Fodder',
        16.00,
        240.00
    );

-- ============================================================
-- 5. EXPENSES
-- ============================================================

INSERT INTO expenses
    (farmer_id, expense_date, category, description, amount)
VALUES
    (
        (SELECT farmer_id FROM farmers WHERE phone = '9876500001'),
        '2026-08-10',
        'Feed',
        'Weekly cattle feed purchase',
        590.00
    ),
    (
        (SELECT farmer_id FROM farmers WHERE phone = '9876500001'),
        '2026-08-09',
        'Medicine',
        'Routine veterinary medicine',
        450.00
    ),
    (
        (SELECT farmer_id FROM farmers WHERE phone = '9876500002'),
        '2026-08-10',
        'Feed',
        'Green and dry fodder',
        480.00
    ),
    (
        (SELECT farmer_id FROM farmers WHERE phone = '9876500002'),
        '2026-08-08',
        'Maintenance',
        'Cattle shed maintenance',
        1200.00
    ),
    (
        (SELECT farmer_id FROM farmers WHERE phone = '9876500003'),
        '2026-08-10',
        'Feed',
        'Cattle feed purchase',
        600.00
    ),
    (
        (SELECT farmer_id FROM farmers WHERE phone = '9876500003'),
        '2026-08-07',
        'Transport',
        'Milk transportation',
        350.00
    );

-- ============================================================
-- 6. REVENUE
-- ============================================================

INSERT INTO revenue
    (farmer_id, sale_date, quantity_litres, price_per_litre, buyer_name)
VALUES
    (
        (SELECT farmer_id FROM farmers WHERE phone = '9876500001'),
        '2026-08-10',
        30.40,
        58.00,
        'Ahmedabad Dairy Cooperative'
    ),
    (
        (SELECT farmer_id FROM farmers WHERE phone = '9876500002'),
        '2026-08-10',
        17.10,
        58.00,
        'Kheda Milk Collection Center'
    ),
    (
        (SELECT farmer_id FROM farmers WHERE phone = '9876500003'),
        '2026-08-10',
        32.00,
        60.00,
        'Mehsana Dairy Cooperative'
    );

COMMIT;