import pandas as pd
from requests import Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

from urllib.parse import quote_plus  # i have done this as my password has special character @

# DATABASE CONNECTION


DB_USER = "postgres"
DB_PASSWORD = quote_plus("Ankush@123")
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "Crypto_dataset"

engine = create_engine(
    f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

# FETCH DATA FROM API

def fetch_crypto_data():

    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    parameters = {
        'start': '1',
        'limit': '15',
        'convert': 'USD'
    }
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': '35088d3af70e49d8a4a109dbffea9999'
    }

    session = Session()
    session.headers.update(headers)

    response = session.get(url, params=parameters, timeout=10)
    response.raise_for_status()

    return pd.json_normalize(response.json()['data'])

# UPSERT FUNCTIONS (DIMENSIONS)

def upsert_dim_crypto(df):

    sql = text("""
        INSERT INTO dim_crypto (
            crypto_id, name, symbol, slug,
            num_market_pairs, date_added,
            cmc_rank, last_updated, tags
        )
        VALUES (
            :crypto_id, :name, :symbol, :slug,
            :num_market_pairs, :date_added,
            :cmc_rank, :last_updated, :tags
        )
        ON CONFLICT (crypto_id) DO UPDATE SET
            name = EXCLUDED.name,
            symbol = EXCLUDED.symbol,
            slug = EXCLUDED.slug,
            num_market_pairs = EXCLUDED.num_market_pairs,
            cmc_rank = EXCLUDED.cmc_rank,
            last_updated = EXCLUDED.last_updated,
            tags = EXCLUDED.tags;
    """)

    with engine.begin() as conn:
        conn.execute(sql, df.to_dict(orient="records"))

def upsert_dim_supply(df):

    sql = text("""
        INSERT INTO dim_supply (
            crypto_id, max_supply, circulating_supply,
            total_supply, infinite_supply,
            self_reported_circulating_supply,
            self_reported_market_cap, minted_market_cap
        )
        VALUES (
            :crypto_id, :max_supply, :circulating_supply,
            :total_supply, :infinite_supply,
            :self_reported_circulating_supply,
            :self_reported_market_cap, :minted_market_cap
        )
        ON CONFLICT (crypto_id) DO UPDATE SET
            max_supply = EXCLUDED.max_supply,
            circulating_supply = EXCLUDED.circulating_supply,
            total_supply = EXCLUDED.total_supply,
            infinite_supply = EXCLUDED.infinite_supply,
            self_reported_circulating_supply = EXCLUDED.self_reported_circulating_supply,
            self_reported_market_cap = EXCLUDED.self_reported_market_cap,
            minted_market_cap = EXCLUDED.minted_market_cap;
    """)

    with engine.begin() as conn:
        conn.execute(sql, df.to_dict(orient="records"))

def upsert_dim_platform(df):

    sql = text("""
        INSERT INTO dim_platform (
            crypto_id, platform_id, platform_name,
            platform_symbol, platform_slug, token_address
        )
        VALUES (
            :crypto_id, :platform_id, :platform_name,
            :platform_symbol, :platform_slug, :token_address
        )
        ON CONFLICT (crypto_id) DO UPDATE SET
            platform_id = EXCLUDED.platform_id,
            platform_name = EXCLUDED.platform_name,
            platform_symbol = EXCLUDED.platform_symbol,
            platform_slug = EXCLUDED.platform_slug,
            token_address = EXCLUDED.token_address;
    """)

    with engine.begin() as conn:
        conn.execute(sql, df.to_dict(orient="records"))

# INSERT FACT TABLE

def insert_fact_market_metrics(df):

    df.to_sql(
        'fact_market_metrics',
        engine,
        if_exists='append',
        index=False,
        method='multi'
    )

# MAIN PIPELINE

def run_pipeline():

    try:
        df = fetch_crypto_data()
        ingestion_time = pd.Timestamp.utcnow()


        # Convert list → comma-separated string
        df['tags'] = df['tags'].apply(
            lambda x: x if isinstance(x, list) else []
        )


        # DIM_CRYPTO 
        dim_crypto = (
            df[[
                'id', 'name', 'symbol', 'slug',
                'num_market_pairs', 'date_added',
                'cmc_rank', 'last_updated', 'tags'
            ]]
            .drop_duplicates(subset=['id'])
        )


        dim_crypto = dim_crypto.rename(columns={'id': 'crypto_id'})
        dim_crypto['date_added'] = pd.to_datetime(dim_crypto['date_added']).dt.date

        # DIM_SUPPLY 
        dim_supply = (
            df[[
                'id', 'max_supply', 'circulating_supply',
                'total_supply', 'infinite_supply',
                'self_reported_circulating_supply',
                'self_reported_market_cap', 'minted_market_cap'
            ]]
            .drop_duplicates(subset=['id'])
        )

        dim_supply = dim_supply.rename(columns={'id': 'crypto_id'})

        # DIM_PLATFORM
        dim_platform = (
            df[[
                'id', 'platform.id', 'platform.name',
                'platform.symbol', 'platform.slug',
                'platform.token_address'
            ]]
            .rename(columns={
                'id': 'crypto_id',
                'platform.id': 'platform_id',
                'platform.name': 'platform_name',
                'platform.symbol': 'platform_symbol',
                'platform.slug': 'platform_slug',
                'platform.token_address': 'token_address'
            })
        )

        # Keep ONLY rows that actually have a platform
        dim_platform = dim_platform[dim_platform['platform_id'].notna()]

        # Convert platform_id safely
        dim_platform['platform_id'] = dim_platform['platform_id'].astype(int)

        # Deduplicate by crypto_id
        dim_platform = dim_platform.drop_duplicates(subset=['crypto_id'])



        # FACT TABLE
        fact = df.rename(columns={
            'id': 'crypto_id',
            'quote.USD.price': 'price_usd',
            'quote.USD.market_cap': 'market_cap',
            'quote.USD.volume_24h': 'volume_24h',
            'quote.USD.volume_change_24h': 'volume_change_24h',
            'quote.USD.percent_change_1h': 'pct_change_1h',
            'quote.USD.percent_change_24h': 'pct_change_24h',
            'quote.USD.percent_change_7d': 'pct_change_7d',
            'quote.USD.percent_change_30d': 'pct_change_30d',
            'quote.USD.percent_change_60d': 'pct_change_60d',
            'quote.USD.percent_change_90d': 'pct_change_90d',
            'quote.USD.market_cap_dominance': 'market_cap_dominance',
            'quote.USD.fully_diluted_market_cap': 'fully_diluted_market_cap',
            'quote.USD.tvl': 'tvl',
            'quote.USD.tvl_ratio': 'tvl_ratio'
        })

        # SELECT ONLY FACT COLUMNS (THIS IS THE FIX)
        fact = fact[[
            'crypto_id',
            'price_usd',
            'market_cap',
            'volume_24h',
            'volume_change_24h',
            'pct_change_1h',
            'pct_change_24h',
            'pct_change_7d',
            'pct_change_30d',
            'pct_change_60d',
            'pct_change_90d',
            'market_cap_dominance',
            'fully_diluted_market_cap',
            'tvl',
            'tvl_ratio'
        ]]

        fact['timestamp'] = ingestion_time


        # LOAD ORDER 
        upsert_dim_crypto(dim_crypto)
        upsert_dim_supply(dim_supply)
        upsert_dim_platform(dim_platform)
        insert_fact_market_metrics(fact)

        print("Pipeline executed successfully")

    except (ConnectionError, Timeout, TooManyRedirects, SQLAlchemyError, ValueError) as e:
        print("Pipeline failed:", e)

# RUN

if __name__ == "__main__":
    run_pipeline()
