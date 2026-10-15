# 🌾 Agri-Horticultural Commodity Price Analysis

An interactive agricultural price analytics dashboard built with Python and Streamlit. The application explores historical commodity prices, compares market trends, analyzes seasonal patterns, and generates model-based price forecasts for 2026–2027.

## Features

- **Price Trends:** Explore historical commodity prices across markets.
- **Regional Analysis:** Compare average prices across markets within a selected state.
- **Seasonal Patterns:** Examine monthly price variation.
- **Commodity Comparison:** Compare average prices across agricultural commodities.
- **Price Forecasting:** Generate monthly estimates from January 2026 through December 2027.
- **Model Evaluation:** Compare linear trend and seasonal trend regression using a held-out historical validation period when sufficient data is available.
- **CSV Export:** Download filtered historical records and forecast results.

## Technologies Used

- Python
- Streamlit
- Pandas
- NumPy
- Plotly

## Installation and Setup

1. Clone or download this repository.
2. Open the project folder in a terminal.
3. Install the required libraries:

   ```bash
   python -m pip install -r requirements.txt
   ```

4. Start the application:

   ```bash
   python -m streamlit run app.py
   ```

5. Open the local URL displayed in the terminal.

Ensure that `agri_dataset.csv` is located in the same directory as `app.py`.

## Forecasting Methodology

The dashboard aggregates historical prices into monthly averages and compares a linear trend with a seasonal trend regression model. When sufficient historical data is available, the models are compared using a held-out validation period, and the model with the lower validation mean absolute error (MAE) is selected.

Forecast results are estimates based on historical observations. They are not actual market prices or guaranteed predictions. Performance can vary by commodity, state, data quality, and forecast horizon.

## Project Objective

To make agricultural commodity price data easier to explore and interpret through interactive visualizations and baseline forecasting techniques.

## Future Improvements

- More robust time-series forecasting models
- Expanded model evaluation across commodities and states
- Weather and supply-related features
- Forecast uncertainty intervals
- Additional data-quality checks

## License

Add an appropriate license if you intend to distribute or reuse this project publicly.