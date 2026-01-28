Welcome to the Cryptocurrency Market Analysis GitHub ReadME. This repository contains one end-to-end data analytics project focused on understanding cryptocurrency market behavior using high-frequency market data. The project emphasizes quality, business relevance, and analytical depth, following best practices used by industry data analysts.

Project Background
The cryptocurrency market is a global, decentralized financial ecosystem that has been active since the early 2010s and operates 24/7 across multiple exchanges. The business model of crypto market data platforms revolves around aggregating price, volume, market capitalization, and liquidity metrics to support traders, investors, analysts, and institutions. From a data analyst’s perspective, the key business metrics include price movement, trading volume, market capitalization, dominance, volatility, and momentum indicators. This project simulates the role of a data analyst working on a crypto analytics platform, tasked with converting raw, high-frequency market data into actionable insights.

Insights and recommendations are provided on the following key areas:

Category 1: Price trend and momentum analysis
Category 2: Volume behavior and trading activity shifts
Category 3: Market dominance and capital concentration
Category 4: Outlier and anomaly detection using comparative analysis

The SQL queries used to inspect and clean the data for this analysis can be found here [link].

Targeted SQL queries regarding various analytical and business questions can be found here [link].

An interactive Power BI dashboard used to report and explore cryptocurrency market trends can be found here [link].

Data Structure & Initial Checks
The main analytical database consists of multiple fact and dimension tables designed to support time-series and snapshot analysis. The core structure includes high-frequency price data, market metrics, and cryptocurrency reference data, with a total row count scaling into the millions due to 5-minute interval granularity. A description of each table is as follows:

Table 1: Fact_Market_Prices – stores timestamped price and volume data for each cryptocurrency at 5-minute intervals.
Table 2: Fact_Market_Metrics – stores market capitalization, dominance, and percentage change metrics by timestamp and cryptocurrency.
Table 3: Dim_Crypto – contains cryptocurrency identifiers, symbols, and names.
Table 4: Date_Time – supports time-based slicing, filtering, and aggregation.

[Entity Relationship Diagram here]

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
