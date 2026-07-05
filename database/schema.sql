PRAGMA foreign_keys = ON;

-- =====================================================
-- 1. COMPANY MASTER
-- =====================================================

CREATE TABLE IF NOT EXISTS stg_companies (
    id TEXT PRIMARY KEY,
    company_logo TEXT,
    company_name TEXT,
    chart_link TEXT,
    about_company TEXT,
    website TEXT,
    nse_profile TEXT,
    bse_profile TEXT,
    face_value REAL,
    book_value REAL,
    roce_percentage REAL,
    roe_percentage REAL
);

-- =====================================================
-- 2. ANALYSIS
-- =====================================================

CREATE TABLE IF NOT EXISTS stg_analysis (
    id INTEGER PRIMARY KEY,
    company_id TEXT,
    compounded_sales_growth REAL,
    compounded_profit_growth REAL,
    stock_price_cagr REAL,
    roe REAL
);

-- =====================================================
-- 3. BALANCE SHEET
-- =====================================================

CREATE TABLE IF NOT EXISTS stg_balancesheet (
    id INTEGER PRIMARY KEY,
    company_id TEXT,
    year INTEGER,
    equity_capital REAL,
    reserves REAL,
    borrowings REAL,
    other_liabilities REAL,
    total_liabilities REAL,
    fixed_assets REAL,
    cwip REAL,
    investments REAL,
    other_asset REAL,
    total_assets REAL
);


-- =====================================================
-- 4. CASHFLOW
-- =====================================================

CREATE TABLE IF NOT EXISTS stg_cashflow (
    id INTEGER PRIMARY KEY,
    company_id TEXT,
    year INTEGER,
    operating_activity REAL,
    investing_activity REAL,
    financing_activity REAL,
    net_cash_flow REAL
);


-- =====================================================
-- 5. PROFIT & LOSS
-- =====================================================

CREATE TABLE IF NOT EXISTS stg_profitandloss (
    id INTEGER PRIMARY KEY,
    company_id TEXT,
    year INTEGER,
    sales REAL,
    expenses REAL,
    operating_profit REAL,
    opm_percentage REAL,
    other_income REAL,
    interest REAL,
    depreciation REAL,
    profit_before_tax REAL,
    tax_percentage REAL,
    net_profit REAL,
    eps REAL,
    dividend_payout REAL
);

-- =====================================================
-- 6. DOCUMENTS
-- =====================================================

CREATE TABLE IF NOT EXISTS stg_documents (
    id INTEGER PRIMARY KEY,
    company_id TEXT,
    year INTEGER,
    annual_report TEXT
);
-- =====================================================
-- 7. PROS & CONS
-- =====================================================

CREATE TABLE IF NOT EXISTS stg_prosandcons (
    id INTEGER PRIMARY KEY,
    company_id TEXT,
    pros TEXT,
    cons TEXT
);

-- =====================================================
-- 8. VALIDATION LOG
-- =====================================================

CREATE TABLE IF NOT EXISTS validation_log (

    validation_id INTEGER PRIMARY KEY AUTOINCREMENT,

    dataset TEXT,

    rule TEXT,

    column_name TEXT,

    failed_rows INTEGER,

    severity TEXT,

    validation_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =====================================================
-- 9. ETL RUN LOG
-- =====================================================

CREATE TABLE IF NOT EXISTS etl_run_log (

    run_id INTEGER PRIMARY KEY AUTOINCREMENT,

    pipeline_name TEXT,

    status TEXT,

    rows_processed INTEGER,

    execution_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =====================================================
-- 10. DATA QUALITY SUMMARY
-- =====================================================

CREATE TABLE IF NOT EXISTS dq_summary (

    dq_id INTEGER PRIMARY KEY AUTOINCREMENT,

    dataset_name TEXT,

    total_rows INTEGER,

    failed_rows INTEGER,

    success_rate REAL,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =====================================================
-- 11. Financial Ratios
-- =====================================================

CREATE TABLE IF NOT EXISTS stg_financial_ratios (

    id INTEGER PRIMARY KEY,

    company_id TEXT,

    year INTEGER,

    net_profit_margin_pct REAL,
    operating_profit_margin_pct REAL,
    return_on_equity_pct REAL,

    debt_to_equity REAL,
    interest_coverage REAL,

    asset_turnover REAL,

    free_cash_flow_cr REAL,
    capex_cr REAL,

    earnings_per_share REAL,
    book_value_per_share REAL,

    dividend_payout_ratio_pct REAL,

    total_debt_cr REAL,

    cash_from_operations_cr REAL
);

-- =====================================================
-- 12. MARKET CAP
-- =====================================================

CREATE TABLE IF NOT EXISTS stg_market_cap (

    id INTEGER PRIMARY KEY,

    company_id TEXT,

    year INTEGER,

    market_cap_crore REAL,

    enterprise_value_crore REAL,

    pe_ratio REAL,

    pb_ratio REAL,

    ev_ebitda REAL,

    dividend_yield_pct REAL
);

-- =====================================================
-- 13. PEER GROUPS
-- =====================================================

CREATE TABLE IF NOT EXISTS stg_peer_groups (

    id INTEGER PRIMARY KEY,

    peer_group_name TEXT,

    company_id TEXT,

    is_benchmark INTEGER
);

-- =====================================================
-- 14. SECTORS
-- =====================================================

CREATE TABLE IF NOT EXISTS stg_sectors (

    id INTEGER PRIMARY KEY,

    company_id TEXT,

    broad_sector TEXT,

    sub_sector TEXT,

    index_weight_pct REAL,

    market_cap_category TEXT
);

-- =====================================================
-- 15. STOCK PRICES
-- =====================================================

CREATE TABLE IF NOT EXISTS stg_stock_prices (

    id INTEGER PRIMARY KEY,

    company_id TEXT,

    date TEXT,

    open_price REAL,

    high_price REAL,

    low_price REAL,

    close_price REAL,

    volume REAL,

    adjusted_close REAL
);

ALTER TABLE stg_financial_ratios
ADD COLUMN revenue_cagr_5yr REAL;

ALTER TABLE stg_financial_ratios
ADD COLUMN revenue_cagr_5yr_flag TEXT;

ALTER TABLE stg_financial_ratios
ADD COLUMN pat_cagr_5yr REAL;

ALTER TABLE stg_financial_ratios
ADD COLUMN pat_cagr_5yr_flag TEXT;

ALTER TABLE stg_financial_ratios
ADD COLUMN eps_cagr_5yr REAL;

ALTER TABLE stg_financial_ratios
ADD COLUMN eps_cagr_5yr_flag TEXT;

ALTER TABLE stg_financial_ratios
ADD COLUMN composite_quality_score REAL;