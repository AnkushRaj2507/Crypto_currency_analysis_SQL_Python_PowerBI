CREATE TABLE dim_crypto (
    crypto_id INT PRIMARY KEY,
    name TEXT,
    symbol TEXT,
    slug TEXT,
    num_market_pairs INT,
    date_added DATE,
    cmc_rank INT,
    last_updated TIMESTAMP,
    tags TEXT[]
);


CREATE TABLE dim_supply (
    crypto_id INT PRIMARY KEY,
    max_supply NUMERIC,
    circulating_supply NUMERIC,
    total_supply NUMERIC,
    infinite_supply BOOLEAN,
    self_reported_circulating_supply NUMERIC,
    self_reported_market_cap NUMERIC,
    minted_market_cap NUMERIC,

    CONSTRAINT fk_supply_crypto
        FOREIGN KEY (crypto_id)
        REFERENCES dim_crypto (crypto_id)
);


CREATE TABLE dim_platform (
    crypto_id INT PRIMARY KEY,
    platform_id INT,
    platform_name TEXT,
    platform_symbol TEXT,
    platform_slug TEXT,
    token_address TEXT,

    CONSTRAINT fk_platform_crypto
        FOREIGN KEY (crypto_id)
        REFERENCES dim_crypto (crypto_id)
);


CREATE TABLE fact_market_metrics (
    crypto_id INT,
    timestamp TIMESTAMP,

    price_usd NUMERIC,
    market_cap NUMERIC,
    volume_24h NUMERIC,
    volume_change_24h NUMERIC,

    pct_change_1h NUMERIC,
    pct_change_24h NUMERIC,
    pct_change_7d NUMERIC,
    pct_change_30d NUMERIC,
    pct_change_60d NUMERIC,
    pct_change_90d NUMERIC,

    market_cap_dominance NUMERIC,
    fully_diluted_market_cap NUMERIC,
    tvl NUMERIC,
    tvl_ratio NUMERIC,

    PRIMARY KEY (crypto_id, timestamp),

    CONSTRAINT fk_fact_crypto
        FOREIGN KEY (crypto_id)
        REFERENCES dim_crypto (crypto_id)
);


CREATE INDEX idx_fact_timestamp
ON fact_market_metrics (timestamp);

CREATE INDEX idx_fact_crypto
ON fact_market_metrics (crypto_id);


INSERT INTO dim_crypto (
    crypto_id, name, symbol, slug,
    num_market_pairs, date_added,
    cmc_rank, last_updated, tags
)
VALUES (
    1, 'Bitcoin', 'BTC', 'bitcoin',
    500, '2013-04-28',
    1, NOW(), ARRAY['mineable', 'pow']
);

select * from dim_crypto;
select * from dim_platform;
select * from dim_supply;
select * from fact_market_metrics;



CREATE TABLE dim_crypto_metadata (
    crypto_id INT PRIMARY KEY,
    name TEXT,
    symbol TEXT,
    category TEXT,
    description TEXT,
    logo_url TEXT,
    website TEXT,
    subreddit TEXT,
    twitter TEXT,
    date_added TIMESTAMP,
    last_updated TIMESTAMP
);

SELECT * FROM dim_crypto_metadata;





# DATA CLEANING

in dim_crypto_metadata table

select count(*)
from dim_crypto_metadata
where subreddit='';

=0 so, this is good

select count(*)
from dim_crypto_metadata
where twitter='';

=0 so, this is also good

# i want to delete timestamp column as it is not required as per now

ALTER TABLE dim_crypto_metadata
DROP COLUMN last_updated;



in dim_supply table

select count (*),
	count(*) filter(where max_supply is  null),
	count(*) filter(where infinite_supply=  true)
from dim_supply

SELECT
    COUNT(*) FILTER (WHERE max_supply IS NULL) AS sql_nulls,
    COUNT(*) FILTER (WHERE max_supply = 0) AS zeros
FROM dim_supply;

UPDATE dim_supply
SET max_supply = NULL
WHERE max_supply <> max_supply;

SELECT
    COUNT(*) FILTER (WHERE max_supply IS NULL) AS nulls,
    COUNT(*) FILTER (WHERE max_supply <> max_supply) AS nans
FROM dim_supply;

UPDATE dim_supply
SET max_supply = NULL
WHERE infinite_supply = true;



