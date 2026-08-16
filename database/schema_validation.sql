-- ============================================================
-- DairyFarm Database Schema
-- PostgreSQL 18+
-- ============================================================

BEGIN;

-- ============================================================
-- 1. FARMERS
-- ============================================================

CREATE TABLE IF NOT EXISTS farmers (
    farmer_id BIGINT GENERATED ALWAYS AS IDENTITY,
    full_name VARCHAR(120) NOT NULL,
    phone VARCHAR(20) NOT NULL,
    email VARCHAR(255),
    address TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT pk_farmers
        PRIMARY KEY (farmer_id),

    CONSTRAINT uq_farmers_phone
        UNIQUE (phone)
);

-- ============================================================
-- 2. CATTLE
-- ============================================================

CREATE TABLE IF NOT EXISTS cattle (
    cattle_id BIGINT GENERATED ALWAYS AS IDENTITY,
    farmer_id BIGINT NOT NULL,
    tag_number VARCHAR(50) NOT NULL,
    name VARCHAR(100),
    breed VARCHAR(100),
    gender VARCHAR(20) NOT NULL,
    date_of_birth DATE,
    status VARCHAR(30) NOT NULL DEFAULT 'active',
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT pk_cattle
        PRIMARY KEY (cattle_id),

    CONSTRAINT fk_cattle_farmer
        FOREIGN KEY (farmer_id)
        REFERENCES farmers(farmer_id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,

    CONSTRAINT uq_cattle_tag_number
        UNIQUE (tag_number),

    CONSTRAINT chk_cattle_gender
        CHECK (gender IN ('male', 'female')),

    CONSTRAINT chk_cattle_status
    CHECK (status IN ('active', 'inactive', 'sold', 'deceased'))

);

-- ============================================================
-- 3. MILK RECORDS
-- ============================================================

CREATE TABLE IF NOT EXISTS milk_records (
    milk_record_id BIGINT GENERATED ALWAYS AS IDENTITY,
    cattle_id BIGINT NOT NULL,
    record_date DATE NOT NULL,
    session VARCHAR(20) NOT NULL,
    quantity_litres NUMERIC(10,2) NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT pk_milk_records
        PRIMARY KEY (milk_record_id),

    CONSTRAINT fk_milk_records_cattle
        FOREIGN KEY (cattle_id)
        REFERENCES cattle(cattle_id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,

    CONSTRAINT chk_milk_session
        CHECK (session IN ('morning', 'evening')),

    CONSTRAINT chk_milk_quantity
        CHECK (quantity_litres >= 0),

    CONSTRAINT uq_milk_cattle_date_session
        UNIQUE (cattle_id, record_date, session)
);

-- ============================================================
-- 4. FEED RECORDS
-- ============================================================

CREATE TABLE IF NOT EXISTS feed_records (
    feed_record_id BIGINT GENERATED ALWAYS AS IDENTITY,
    farmer_id BIGINT NOT NULL,
    cattle_id BIGINT,
    record_date DATE NOT NULL,
    feed_type VARCHAR(100) NOT NULL,
    quantity_kg NUMERIC(10,2) NOT NULL,
    cost NUMERIC(12,2) NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT pk_feed_records
        PRIMARY KEY (feed_record_id),

    CONSTRAINT fk_feed_records_farmer
        FOREIGN KEY (farmer_id)
        REFERENCES farmers(farmer_id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,

    CONSTRAINT fk_feed_records_cattle
        FOREIGN KEY (cattle_id)
        REFERENCES cattle(cattle_id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,

    CONSTRAINT chk_feed_quantity
        CHECK (quantity_kg >= 0),

    CONSTRAINT chk_feed_cost
        CHECK (cost >= 0)
);

-- ============================================================
-- 5. EXPENSES
-- ============================================================

CREATE TABLE IF NOT EXISTS expenses (
    expense_id BIGINT GENERATED ALWAYS AS IDENTITY,
    farmer_id BIGINT NOT NULL,
    expense_date DATE NOT NULL,
    category VARCHAR(80) NOT NULL,
    description TEXT,
    amount NUMERIC(12,2) NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT pk_expenses
        PRIMARY KEY (expense_id),

    CONSTRAINT fk_expenses_farmer
        FOREIGN KEY (farmer_id)
        REFERENCES farmers(farmer_id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,

    CONSTRAINT chk_expense_amount
        CHECK (amount >= 0)
);

-- ============================================================
-- 6. REVENUE
-- ============================================================

CREATE TABLE IF NOT EXISTS revenue (
    revenue_id BIGINT GENERATED ALWAYS AS IDENTITY,
    farmer_id BIGINT NOT NULL,
    sale_date DATE NOT NULL,
    quantity_litres NUMERIC(10,2) NOT NULL,
    price_per_litre NUMERIC(10,2) NOT NULL,
    buyer_name VARCHAR(120),
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT pk_revenue
        PRIMARY KEY (revenue_id),

    CONSTRAINT fk_revenue_farmer
        FOREIGN KEY (farmer_id)
        REFERENCES farmers(farmer_id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,

    CONSTRAINT chk_revenue_quantity
        CHECK (quantity_litres >= 0),

    CONSTRAINT chk_revenue_price
        CHECK (price_per_litre >= 0)
);

-- ============================================================
-- INDEXES
-- ============================================================

CREATE INDEX IF NOT EXISTS idx_cattle_farmer_id
    ON cattle(farmer_id);

CREATE INDEX IF NOT EXISTS idx_milk_records_cattle_id
    ON milk_records(cattle_id);

CREATE INDEX IF NOT EXISTS idx_milk_records_record_date
    ON milk_records(record_date);

CREATE INDEX IF NOT EXISTS idx_feed_records_farmer_id
    ON feed_records(farmer_id);

CREATE INDEX IF NOT EXISTS idx_feed_records_cattle_id
    ON feed_records(cattle_id);

CREATE INDEX IF NOT EXISTS idx_feed_records_record_date
    ON feed_records(record_date);

CREATE INDEX IF NOT EXISTS idx_expenses_farmer_id
    ON expenses(farmer_id);

CREATE INDEX IF NOT EXISTS idx_expenses_expense_date
    ON expenses(expense_date);

CREATE INDEX IF NOT EXISTS idx_revenue_farmer_id
    ON revenue(farmer_id);

CREATE INDEX IF NOT EXISTS idx_revenue_sale_date
    ON revenue(sale_date);

ROLLBACK;