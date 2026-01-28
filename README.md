Welcome to the Cryptocurrency Market Analysis GitHub ReadME. This repository contains an end-to-end data analytics project focused on understanding cryptocurrency market behavior using high frequency market data. The project emphasizes quality, business relevance, and analytical depth, following best practices used by industry data analysts.

# Project Background
The cryptocurrency market is a global, decentralized financial ecosystem that has been active since the early 2010s and operates 24/7 across multiple exchanges. The business model of crypto market data platforms revolves around aggregating price, volume, market capitalization, and liquidity metrics to support traders, investors, analysts, and institutions. From a data analyst’s perspective, the key business metrics include price movement, trading volume, market capitalization, dominance, volatility, and momentum indicators. This project simulates the role of a data analyst working on a crypto analytics platform, tasked with converting raw, high-frequency market data into actionable insights.

Insights and recommendations are provided on the following key areas:

Category 1: Price trend and momentum analysis

Category 2: Volume behavior and trading activity shifts

Category 3: Market dominance and capital concentration

Category 4: Outlier and anomaly detection using comparative analysis


The SQL queries used to inspect and clean the data for this analysis can be found here [link].

Targeted SQL queries regarding various analytical and business questions can be found here [link].

An interactive Power BI dashboard used to report and explore cryptocurrency market trends can be found here [link].


# Project Workflow

Step 1: Automated Data Ingestion
Built an automated Python pipeline that runs 24×7 at 5-minute intervals to fetch real-time cryptocurrency market data from the CoinMarketCap API and load it into a PostgreSQL database.

Step 2: Data Storage
Designed a relational schema in PostgreSQL and stored the ingested data across normalized dimension tables and a fact table to support scalable time-series and snapshot analytics.

Step 3: Data Cleaning and Validation
Cleaned and validated data using SQL in PostgreSQL and Power Query in Power BI by handling missing values, correcting data types, removing duplicates, and standardizing timestamps for analytical consistency.

Step 4: Data Modeling in Power BI
Modeled the dataset in Power BI by defining table relationships, creating DAX measures, and implementing time-aware logic for accurate analytical reporting.

Step 5: Dashboard Design and Visualization
Designed interactive Power BI dashboards using KPIs, trend lines, and comparative visuals to communicate cryptocurrency market insights effectively.

Step 6: Insight Interpretation
Analytical results are translated into business-relevant insights focused on momentum, liquidity, and capital concentration.


# Data Structure & Initial Checks

The PostgreSQL database follows a fact–dimension design optimized for high-frequency cryptocurrency market analysis. Data is ingested every 5 minutes from the CoinMarketCap API, with dimension tables maintained via upserts and the fact table growing continuously to support time-series analysis.

Table 1: Dim_Crypto
Stores core cryptocurrency identifiers and reference attributes such as name, symbol, slug, CMC rank, number of market pairs, date added, last updated timestamp, and tags.

Table 2: Dim_Supply
Stores supply-related metrics including max supply, circulating supply, total supply, infinite supply flag, self-reported circulating supply, self-reported market cap, and minted market cap.

Table 3: Dim_Platform
Stores blockchain platform information for token-based cryptocurrencies, including platform ID, name, symbol, slug, and token address, with one record per crypto_id.

Table 4: Dim_Crypto_Metadata
Stores extended descriptive metadata fetched from a separate API endpoint, including category, description, logo URL, website, subreddit, Twitter handle, date added, and last updated timestamp.

Table 5: Fact_Market_Metrics
Stores 5-minute market snapshots for each cryptocurrency, including price in USD, market capitalization, 24-hour volume, volume change, multi-horizon price change percentages, market cap dominance, fully diluted market cap, TVL, TVL ratio, and ingestion timestamp.

Initial checks include validation of numeric data types, deduplication of dimension records, enforcement of crypto_id-based relationships, and verification of timestamp consistency across ingestion cycles.

<img width="951" height="746" alt="image" src="https://github.com/user-attachments/assets/3340ec8f-3b1e-4a46-84b0-9d700f9458a2" />


Executive Summary
Overview of Findings
This analysis shows that cryptocurrency markets are highly skewed, with a small number of large-cap assets dominating total market value while smaller assets exhibit significantly higher volatility. Volume spikes often precede or accompany sharp price movements, providing early signals of momentum shifts. Scatter-based analysis reveals anomalies and speculative behavior that are not easily observable in traditional line charts.

[Visualization, including a snapshot of the Power BI dashboard]

Insights Deep Dive
Category 1: Price trend and momentum analysis
Main insight 1. Short-term price movements at 5-minute intervals are extremely noisy, but applying moving averages reveals clearer directional trends over intraday periods.

Main insight 2. Sustained upward price movement is often visible before major breakouts when viewed across rolling time windows rather than single intervals.

Main insight 3. Large-cap cryptocurrencies tend to show smoother price trends compared to small-cap assets, which experience abrupt spikes and reversals.

Main insight 4. Filtering visuals to the latest timestamp prevents misleading conclusions caused by historical aggregation.

[Visualization specific to category 1]

Category 2: Volume behavior and trading activity shifts
Main insight 1. Significant increases in trading volume often coincide with heightened market attention and precede sharp price changes.

Main insight 2. Assets with rising volume but flat price frequently indicate accumulation or distribution phases.

Main insight 3. Volume change metrics provide stronger short-term signals than absolute volume values alone.

Main insight 4. Comparing volume behavior across assets highlights disproportionate interest in specific cryptocurrencies.

[Visualization specific to category 2]

Category 3: Market dominance and capital concentration
Main insight 1. Market capitalization dominance remains heavily concentrated among a small set of large cryptocurrencies.

Main insight 2. Shifts in dominance reflect broader market sentiment changes between risk-on and risk-off phases.

Main insight 3. Dominance metrics calculated using latest snapshot logic provide a more accurate view than averaged historical values.

Main insight 4. Smaller assets rarely gain dominance without corresponding volume expansion.

[Visualization specific to category 3]

Category 4: Outlier and anomaly detection
Main insight 1. Scatter plots comparing price change and volume change effectively surface abnormal trading behavior.

Main insight 2. Large-cap outliers indicate systemic market events, while small-cap outliers often represent speculative spikes.

Main insight 3. Log-scaled axes are essential to visualize both large and small assets within the same analytical frame.

Main insight 4. Outlier detection supports early identification of potential trend reversals or market stress.

[Visualization specific to category 4]

Recommendations:
Based on the insights and findings above, we would recommend the analytics and strategy teams to consider the following:

High-frequency price data should be paired with trend smoothing techniques to avoid reacting to short-term noise.

Volume-based indicators should be monitored alongside price movements to identify early momentum signals.

Market dominance metrics should be tracked continuously to understand capital flow between major and minor assets.

Scatter-based comparative visuals should be used regularly to detect anomalies and unusual trading behavior.

Dashboards should emphasize latest snapshot metrics rather than aggregated historical values for decision-making.

Assumptions and Caveats:
Throughout the analysis, multiple assumptions were made to manage challenges with the data. These assumptions and caveats are noted below:

Assumption 1. Missing or delayed data points were assumed to be temporary ingestion gaps and excluded from snapshot calculations.

Assumption 2. Percentage change metrics were assumed to be computed consistently across assets using standardized time windows.

Assumption 3. Extreme outliers caused by data errors were filtered only after validation against volume and price consistency checks.
