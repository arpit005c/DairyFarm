Step 9A — Database Design

We will use this relationship model:

                    ┌──────────────┐
                    │   farmers    │
                    └──────┬───────┘
                           │
                    1      │      N
                           ▼
                    ┌──────────────┐
                    │    cattle    │
                    └──────┬───────┘
                           │
                           │ 1:N
             ┌─────────────┴─────────────┐
             ▼                           ▼
     ┌────────────────┐         ┌────────────────┐
     │  milk_records  │         │  feed_records  │
     └────────────────┘         └────────────────┘


farmers ────────────────┬─────────────────────┐
                        │                     │
                        ▼                     ▼
                 ┌────────────┐        ┌────────────┐
                 │  expenses  │        │  revenue   │
                 └────────────┘        └────────────┘
Core principle

We will not repeat farmer information inside cattle or milk records.

Instead:

farmers.id
    ↓
cattle.farmer_id
    ↓
milk_records.cattle_id

This follows the Phase 3 normalization requirement to avoid duplicated farmer and cattle information.

Step 9B — Table Definitions
1. farmers

Purpose:

Store farmer/manager information.

Proposed fields:

Column	Type	Rule
farmer_id	BIGINT	PK
full_name	VARCHAR(120)	NOT NULL
phone	VARCHAR(20)	NOT NULL, UNIQUE
email	VARCHAR(255)	NULL
address	TEXT	NULL
created_at	TIMESTAMPTZ	DEFAULT CURRENT_TIMESTAMP
updated_at	TIMESTAMPTZ	DEFAULT CURRENT_TIMESTAMP
2. cattle

Purpose:

Store individual cattle associated with a farmer.

Column	Type	Rule
cattle_id	BIGINT	PK
farmer_id	BIGINT	FK → farmers
tag_number	VARCHAR(50)	NOT NULL, UNIQUE
name	VARCHAR(100)	NULL
breed	VARCHAR(100)	NULL
gender	VARCHAR(20)	NOT NULL
date_of_birth	DATE	NULL
status	VARCHAR(30)	DEFAULT 'active'
created_at	TIMESTAMPTZ	DEFAULT CURRENT_TIMESTAMP
updated_at	TIMESTAMPTZ	DEFAULT CURRENT_TIMESTAMP

The unique cattle tag is justified because the Phase 3 specification specifically identifies an appropriate cattle tag as a candidate for UNIQUE.

3. milk_records

Purpose:

Store milk production for individual cattle.

The requirements explicitly call for morning/evening production, daily totals, historical records, and filtering by date/animal/farmer.

Column	Type	Rule
milk_record_id	BIGINT	PK
cattle_id	BIGINT	FK → cattle
record_date	DATE	NOT NULL
session	VARCHAR(20)	NOT NULL
quantity_litres	NUMERIC(10,2)	NOT NULL
created_at	TIMESTAMPTZ	DEFAULT CURRENT_TIMESTAMP

Constraints:

quantity_litres >= 0
session IN ('morning', 'evening')

We will also prevent duplicate records for the same cattle/date/session.

4. feed_records

Purpose:

Store feed usage and feed cost.

The approved requirements specifically require feed type, quantity, cost, and feed history.

Column	Type	Rule
feed_record_id	BIGINT	PK
farmer_id	BIGINT	FK → farmers
cattle_id	BIGINT	FK → cattle, nullable
record_date	DATE	NOT NULL
feed_type	VARCHAR(100)	NOT NULL
quantity_kg	NUMERIC(10,2)	NOT NULL
cost	NUMERIC(12,2)	NOT NULL
created_at	TIMESTAMPTZ	DEFAULT CURRENT_TIMESTAMP

cattle_id is nullable because the system can record feed at farm level when a particular feed quantity is not assigned to one animal.

5. expenses

Purpose:

Store operational expenses.

The approved requirements include recording expenses, categorizing them, viewing them, and calculating total expenses.

Column	Type	Rule
expense_id	BIGINT	PK
farmer_id	BIGINT	FK → farmers
expense_date	DATE	NOT NULL
category	VARCHAR(80)	NOT NULL
description	TEXT	NULL
amount	NUMERIC(12,2)	NOT NULL
created_at	TIMESTAMPTZ	DEFAULT CURRENT_TIMESTAMP

Constraint:

amount >= 0
6. revenue

Purpose:

Store milk-sale revenue.

The requirements specifically call for milk sales, revenue calculation, profit calculation, and cost-per-litre analysis.

Column	Type	Rule
revenue_id	BIGINT	PK
farmer_id	BIGINT	FK → farmers
sale_date	DATE	NOT NULL
quantity_litres	NUMERIC(10,2)	NOT NULL
price_per_litre	NUMERIC(10,2)	NOT NULL
buyer_name	VARCHAR(120)	NULL
created_at	TIMESTAMPTZ	DEFAULT CURRENT_TIMESTAMP

Revenue can be calculated as:

quantity_litres × price_per_litre

We should not unnecessarily store a manually entered revenue amount, because that duplicates a value that can be derived from the two source fields.

Step 9C — Relationships
Farmer → Cattle
farmers.farmer_id
        ↓
cattle.farmer_id

One farmer can have many cattle.

1 : N
Cattle → Milk
cattle.cattle_id
        ↓
milk_records.cattle_id

One cattle can have many milk records.

1 : N
Farmer → Feed
farmers.farmer_id
        ↓
feed_records.farmer_id

One farmer can have many feed records.

Cattle → Feed
cattle.cattle_id
        ↓
feed_records.cattle_id

Optional association.

Farmer → Expenses
farmers.farmer_id
        ↓
expenses.farmer_id
Farmer → Revenue
farmers.farmer_id
        ↓
revenue.farmer_id
Step 9D — Normalization Decisions

The design intentionally avoids:

❌ storing farmer name in every cattle record

❌ storing farmer phone in every cattle record

❌ storing cattle name/breed inside every milk record

❌ storing multiple milk sessions in one column

❌ storing multiple feed types in one column

Instead:

Farmer
  ↓
Cattle
  ↓
Milk Record

This provides a clean relational structure without applying unnecessarily extreme normalization. The Phase 3 specification explicitly calls for this balance.

Step 9E — Constraints

The database will use:

Primary keys

Every core table gets a primary key, as required by the Phase 3 specification.

Foreign keys

All relationships will be enforced with foreign keys.

NOT NULL

Only genuinely required fields will be NOT NULL.

UNIQUE

At minimum:

farmers.phone
cattle.tag_number
CHECK

Examples:

quantity_litres >= 0
quantity_kg >= 0
cost >= 0
amount >= 0
price_per_litre >= 0

These are directly aligned with the Phase 3 constraint guidance.

Step 9F — Index Strategy

We will not index every column.

The Phase 3 specification explicitly says indexes should only be created where justified.

Initial candidates:

cattle.farmer_id
milk_records.cattle_id
milk_records.record_date
feed_records.farmer_id
feed_records.cattle_id
feed_records.record_date
expenses.farmer_id
expenses.expense_date
revenue.farmer_id
revenue.sale_date

These support the project's planned filtering, historical views, joins, and analytics.