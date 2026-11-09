# Agri-Horticultural Commodity Price Analysis

<p align="center">
  <strong>Explore Market Trends. Understand Price Patterns. Analyze the Future.</strong>
  <br/>
  An interactive agricultural commodity analytics platform for exploring historical market prices, comparing regional trends, identifying seasonal patterns and generating baseline price forecasts.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/Streamlit-Dashboard-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" />
  <img src="https://img.shields.io/badge/Pandas-Data%20Analysis-150458?style=for-the-badge&logo=pandas&logoColor=white" />
  <img src="https://img.shields.io/badge/Plotly-Visualization-3F4F75?style=for-the-badge&logo=plotly&logoColor=white" />
  <img src="https://img.shields.io/badge/Status-Active%20Development-success?style=for-the-badge" />
</p>

---

## Overview

**Agri-Horticultural Commodity Price Analysis** is a Python-based agricultural market analytics dashboard designed to make historical commodity price information easier to explore and interpret.

The application provides interactive visualizations for analyzing commodity price movements, comparing regional markets, examining seasonal variations and evaluating historical pricing patterns.

It also includes a baseline forecasting module that generates monthly price estimates for 2026–2027 using regression-based approaches.

By combining data processing, interactive analytics and statistical forecasting, the project provides a practical environment for exploring agricultural market behaviour.

## Key Features

| Feature | Description |
|---|---|
|  Price Trend Analysis | Explore historical commodity price movements |
|  Regional Analysis | Compare average prices across markets within a selected state |
|  Seasonal Analysis | Examine monthly and seasonal price variations |
|  Commodity Comparison | Compare average prices across agricultural commodities |
|  Price Forecasting | Generate monthly estimates from January 2026 to December 2027 |
|  Model Evaluation | Compare linear and seasonal regression approaches |
|  Validation Metrics | Evaluate models using held-out historical data and MAE |
|  CSV Export | Download filtered historical records and forecast results |
|  Interactive Filters | Explore data using available commodity and regional selections |

##  Technology Stack

| Layer | Technology |
|---|---|
| Programming Language | Python |
| Dashboard Framework | Streamlit |
| Data Processing | Pandas |
| Numerical Computing | NumPy |
| Data Visualization | Plotly |
| Forecasting | Regression-based statistical models |
| Data Source | `agri_dataset.csv` |

##  How It Works

```text
          Agricultural Dataset
             (CSV File)
                  |
                  ▼
           Data Loading
                  |
                  ▼
          Data Preparation
                  |
                  ▼
          Historical Analysis
                  |
        ┌─────────┼─────────┐
        ▼         ▼         ▼
    Price      Regional  Seasonal
    Trends     Analysis  Analysis
        |         |         |
        └─────────┼─────────┘
                  |
                  ▼
          Monthly Aggregation
                  |
                  ▼
          Regression Models
                  |
           ┌──────┴──────┐
           ▼             ▼
      Linear Trend   Seasonal Trend
         Model          Model
           |             |
           └──────┬──────┘
                  |
                  ▼
          Validation & MAE
                  |
                  ▼
          Model Selection
                  |
                  ▼
          2026–2027 Forecast
                  |
                  ▼
         Interactive Dashboard
                  |
                  ▼
             CSV Export
```

##  Dashboard Capabilities

### 1. Historical Price Trends

Explore how agricultural commodity prices have changed over time.

- Examine historical price movements.
- Filter available commodities.
- Explore price behaviour across markets.

### 2. Regional Market Analysis

Compare average commodity prices across different markets within a selected state.

This helps identify regional price differences and variations in market behaviour.

### 3. Seasonal Price Analysis

Analyze monthly price variations to identify recurring seasonal patterns in historical observations.

### 4. Commodity Comparison

Compare average prices across different agricultural commodities to understand differences in their historical market values.

### 5. Price Forecasting

Generate monthly price estimates covering:

- January 2026
- December 2026
- January 2027
- December 2027

The forecast module compares two regression-based approaches and selects a model based on historical validation performance when sufficient data is available.

### 6. CSV Export

Download analysis results for further exploration, reporting or external analysis.

## Getting Started

Follow these instructions to run the project locally.

### Prerequisites

- Python 3.10 or later
- pip
- Git

### 1. Clone the Repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
```

Navigate into the project folder:

```bash
cd agri-horticultural-commodity-price-analysis
```

### 2. Install Dependencies

```bash
python -m pip install -r requirements.txt
```

### 3. Verify Dataset Placement

Ensure the dataset is located in the same directory as `app.py`.

```text
project/
│
├── app.py
├── agri_dataset.csv
├── requirements.txt
├── README.md
└── ...
```

### 4. Start the Application

```bash
python -m streamlit run app.py
```

### 5. Open the Dashboard

Open the local URL displayed in your terminal.

Usually:

**http://localhost:8501**

##  Forecasting Methodology

The forecasting module uses historical agricultural commodity price observations to generate baseline monthly estimates.

### Data Preparation

Historical price records are aggregated into monthly average values.

### Model 1: Linear Trend Regression

Captures the general upward or downward movement in historical monthly prices.

### Model 2: Seasonal Trend Regression

Combines a time-based trend with seasonal information to represent recurring monthly variations.

### Model Evaluation

When sufficient historical observations are available:

1. Historical records are divided into training and validation periods.
2. Both models generate predictions for the held-out validation period.
3. Mean Absolute Error (MAE) is calculated for each model.
4. The model with the lower validation MAE is selected.

### Forecast Generation

The selected model generates monthly estimates covering January 2026 through December 2027.

**Important:** Forecasts are statistical estimates based on historical observations. They are not actual market prices, guaranteed predictions or financial advice. Accuracy can vary depending on commodity, location, data quality and forecast horizon.

## Project Structure

```text
Agri-Horticultural-Commodity-Price-Analysis/
│
├── app.py
├── agri_dataset.csv
├── requirements.txt
├── README.md
└── ...
```

*Update this structure to reflect the actual files and folders in your repository.*

## Data & Interpretation

The quality of analysis depends on the quality and coverage of the underlying agricultural dataset.

Consider the following when interpreting results:

- Historical observations may not represent every market.
- Missing records can affect monthly averages.
- Regional comparisons depend on available market coverage.
- Seasonal patterns may differ between commodities.
- Forecast reliability decreases when projecting further into the future.

## Future Enhancements

Potential improvements for future versions:

- **Advanced Time-Series Models:** Explore ARIMA, SARIMA and other forecasting approaches.
- **Weather Integration:** Include rainfall, temperature and weather-related features.
- **Supply & Demand Analysis:** Incorporate agricultural production and market supply information.
- **Forecast Uncertainty:** Display prediction intervals alongside estimated prices.
- **Expanded Model Evaluation:** Compare forecasting performance across individual commodities and states.
- **Interactive Market Maps:** Visualize regional price differences geographically.
- **Automated Data Updates:** Integrate reliable agricultural market data sources.
- **Advanced Analytics:** Add anomaly detection and commodity-specific trend analysis.

## Project Objectives

- Explore agricultural commodity price behaviour.
- Understand regional and seasonal market variations.
- Apply Python-based data processing and visualization.
- Implement baseline regression-based forecasting.
- Evaluate forecasting models using historical validation data.
- Present agricultural market information through an interactive dashboard.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

<p align="center">
  <strong> Agri-Horticultural Commodity Price Analysis</strong>
  <br/>
  <em>Turning Agricultural Data Into Meaningful Market Insights.</em>
  <br/><br/>
  Built with Python, Streamlit, Pandas, NumPy and Plotly.
</p>
