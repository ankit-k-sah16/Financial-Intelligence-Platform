-- Total companies
SELECT COUNT(*) AS total_companies
FROM stg_companies;

-- Companies by sector
SELECT
    broad_sector,
    COUNT(*) AS company_count
FROM stg_sectors
GROUP BY broad_sector
ORDER BY company_count DESC;

-- Top 10 companies by market cap
SELECT
    company_id,
    market_cap_crore
FROM stg_market_cap
ORDER BY market_cap_crore DESC
LIMIT 10;

-- Companies with highest ROE
SELECT
    company_id,
    return_on_equity_pct
FROM stg_financial_ratios
ORDER BY return_on_equity_pct DESC
LIMIT 10;

-- Average PE Ratio
SELECT
    AVG(pe_ratio) AS avg_pe_ratio
FROM stg_market_cap;

-- Stock price history count
SELECT
    company_id,
    COUNT(*) AS trading_days
FROM stg_stock_prices
GROUP BY company_id;

-- Companies with missing years
SELECT
    company_id,
    COUNT(DISTINCT year) AS year_count
FROM stg_profitandloss
GROUP BY company_id
HAVING year_count < 5;